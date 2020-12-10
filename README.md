# Cyberpunk-2077-archive-extractor
Rough CP2077 archive extractor written in Python.

- It doesn't use hardcoded offsets so it'll work with different versions of archives.
- **Reading of extracted files isn't chunked yet.**

[Windows binaries](https://github.com/Sorrow446/Cyberpunk-2077-archive-extractor/releases)

### Usage
Drag archive onto script / exe.

### Supported Archives
|Archive|Output|
|---|---|
|audio_1_general|WEM audio|
|audio_2_soundbanks|WEM audio|
|basegame_5_video|Bink Video 2|
|lang_(lang)_voice|WEM audio|

### WEM to OGG
```
FOR %%a IN ("cp2077 extractor out\audio_1_general\*.wem") DO (ww2ogg "%%a" --pcb packed_codebooks_aoTuV_603.bin & DEL "%%a")
```
