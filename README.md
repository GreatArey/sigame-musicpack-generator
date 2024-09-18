# SiGame MusicPack Generator
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

A simple utility for generating music packets for SiGame

## Requirements
### ffmpeg
Installation guide:
- [Windows](https://www.wikihow.com/Install-FFmpeg-on-Windows)
- [Linux](https://www.tecmint.com/install-ffmpeg-in-linux/)

### Python requirements
In the main directory, open the terminal and run
```commandline
pip install -r requirements.txt
```

## Usage
Run
```commandline
python src/main.py
```
### Params description
- Source directory: stores unprocessed tracks in mp3 format
- Tracks found: track count in source directory
- Target directory: stores trimmed tracks and the output yaml file
- Number of rounds: that's literally what it is
- Number of topics per round: that's literally what it is
- Number of questions in the topic: that's literally what it is
- Required number of tracks: product of the previous three parameters
- Choice of option:
  - Fixed interval (seconds from/to): cut a part from N seconds to M seconds for all tracks
  - Center part (length in seconds): cut a part center of all tracks
- Status: displays the current status
