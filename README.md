# BeetsPlugins

## Description
Beets is a music library manager and MusicBrainz tagger http://beets.radbox.org/
This is a plugin to auto generate and tag a mp3 file with the tempo of the track during the beets import process.
it is using the Aubio tool http://aubio.org


## Installation
Currently this is only tested on Ubuntu 14.10 and 15.04 64bit

1. Make sure you've installed all requirements
2. Clone this repository:
  `git clone https://github.com/madmouser1/BeetsPlugins.git`
   into a directory and set the PYTHONPATH to the parent directory of the beetsplug folder e.g. /home/username/beetsplug/

### PYTHONPATH
  `export PYTHONPATH="$PYTHONPATH:/home/username/"`

   add it to .profile to be persistent

### Install Aubio:
```shell
sudo apt-get install aubio-tools
```

## Usage

Here's a short explanation how to use `madmousetempo`:

Add 
```
plugins: madmousetempo

madmousetempo:
        auto: yes
```
to `config.yaml`

then run `beet import /folder/of/music/to/import/`

## Contributing

Any contributions or suggestions welcome.

## Requirements / Dependencies

* Aubio 
* Python
* Beets

## Version

1.0.0