> **Warning**  
> This repo is work in progress.

# MX MIDI KEYBOARD

This is project is highly inspired by [MIDI88](https://www.printables.com/model/1168638-midi88-88-key-mx-based-midi-keyboard), shout out to the author!

The main problem with it is a fact, that is full dimension keyboard and I don't have the 
space or switches to handle it. So I decided to develop my own, parametrisable model, which
could handle exactly the amount of keys I have. Currently, it's designed to handle 45 keys - single pack
of gateron MX switches, minus two for octave up and down.

Currently the default configuration work well with classic, full sized MX switches, but I'm sure that after minor
tweaks it is possible to use this model with low profile switches. I'm planning to build the config from them,
but currently I'm focused on full sized MX switches.

# Configuration

TODO

# Models

For the default configs models are available packed in .zip file as a release. There are a few options to generate models
for modified config.

## Github actions

This repo already accomodate the github action to generate and release files, based on the default config.
Step by step:
- Clone the repo
- Modify the default config file
- commit and add tag starting with `v` letter
  - Github Actions should run automatically
- Download release file

## Locally

### Docker

You can generate models using `Dockerfile.generate`. Modify the default config and run the commands:
```bash
docker build -f Dockerfile.generate -t generate:latest .
docker run --rm -v "$(pwd)/build":"/app/build" generate:latest
```

You will find all the STL files at `build/` directory.

### Python

System requirements: install `uv` and `openscad` libraries.


UV [installation guide](https://docs.astral.sh/uv/getting-started/installation/).

OpenSCAD [installation guide](https://openscad.org/downloads.html).


Next clone the repo and move to the directory:
```bash
git clone https://github.com/AIn0n/2Mkb && cd 2Mkb
```


Create UV virtual environment:
```bash
uv venv
```


Activate the environment:
```bash
source .venv/bin/activate
```


Install project requirements:
```bash
uv sync
```


Run the script:
```bash
uv run generate
```

All STLs can be found at `build/` directory.

## Printing config

### Models Orientation

Freshly generated models are already in the best orientation to print. I *DO NOT* recommend changing it,
the whole project was made with assumption it will be printed exactly in this way.


# LICENSE

License found at [this repo](https://github.com/non-ai-licenses/non-ai-licenses/blob/main/NON-AI-APACHE2).
It's just a Apache 2.0 license, with small disclaimer to not use it as a training data in any form of AI
models.