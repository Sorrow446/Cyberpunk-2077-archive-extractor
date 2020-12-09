import os
import sys


def dir_setup(path):
	if not os.path.isdir(path):
		os.makedirs(path)	

def find(sig):
	prev = b''
	decimals = []
	with open(sys.argv[1], 'rb') as f:
		if f.read(4) != b'\x52\x44\x41\x52':
			raise Exception('Not a valid archive file.')
		f.seek(0)
		while True:
			concat_pos = 0
			buf = f.read(2048 ** 2)
			if not buf:
				break
			concat = prev + buf
			while True:
				concat_pos = concat.find(sig, concat_pos)
				if concat_pos == -1:
					break
				pos = f.tell() + concat_pos - len(concat)
				if sig == b'\x52\x49\x46\x46':
					cur_pos = f.tell()
					f.seek(pos + 16)
					_byte = f.read(1)
					f.seek(cur_pos)
					if _byte != b'\x42':
						concat_pos += len(sig)
						continue
				decimals.append(pos)
				concat_pos += len(sig)
			prev = buf[-len(sig) + 1:]
	return decimals

def main(sig, path):
	print("Searching archive...")
	decimals = find(sig[0])
	print("Found {} files.".format(len(decimals)))
	with open(os.path.join(path, sys.argv[1]), 'rb') as f:
		for num, dec in enumerate(decimals, 1):
			print("File {0} of {1}: {0}{2}".format(num, len(decimals), sig[1]))
			f.seek(dec + len(sig[0]))
			size = int.from_bytes(f.read(4), 'little') + 8
			f.seek(dec)
			with open(os.path.join(path, str(num) + sig[1]), 'wb') as f2:
				f2.write(f.read(size))

if __name__ == '__main__':
	try:
		if hasattr(sys, 'frozen'):
			os.chdir(os.path.dirname(sys.executable))
		else:
			os.chdir(os.path.dirname(__file__))
	except OSError:
		pass
	signatures = {
		'audio_1_general': (b'\x52\x49\x46\x46', '.wem'),
		'audio_2_soundbanks': (b'\x52\x49\x46\x46', '.wem'),
		'basegame_5_video': (b'\x4b\x42\x32\x6a', '.bk2'),
		'lang_de_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_en_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_es-es_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_fr_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_it_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_ja_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_ko_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_pl_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_pt_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_ru_voice': (b'\x52\x49\x46\x46', '.wem'),
		'lang_zh-cn_voice': (b'\x52\x49\x46\x46', '.wem')
	}
	base_fname = os.path.basename(sys.argv[1]).split('.')[0]
	path = os.path.join('cp2077 extractor out', base_fname)
	dir_setup(path)
	try:
		sig = signatures[base_fname]
	except KeyError:
		raise Exception('Unsupported archive.')
	try:
		main(sig, path)
	except KeyboardInterrupt:
		pass
	input('Press enter to exit.')