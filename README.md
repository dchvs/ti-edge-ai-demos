# TI EdgeAI Demos
> Demos to show the powerful capabilities of TI Edge AI SDK on Jacinto 7 platform

This demo shows how to create a multi-channel AI server with capabilities to detect user-specific objects and trigger actions based on inference results, which is a system that is typically found at "Smart City" applications.  It receives multiple RTSP video streams and detects objects based on the user's needs, and triggers actions such as video recordings and event logging. This demo could become a base system in "Smart City" applications like surveillance, traffic congestion control, smart parking use cases and more.

## Platform
To get started with the Jacinto 7 platform setup, please visit: https://www.ti.com/lit/ml/spruis8/spruis8.pdf

## Building the Project

### 1. User mode
To build the project, run the following commands:
```bash
python3 setup.py test
sudo python3 setup.py install
``` 

### 2. Developer mode
If you are a project maintainer or just want to contribute to the project, we recommend building the project as:
```bash
sudo -H pip3 install pre-commit
python3 setup.py test
sudo python3 setup.py develop
```

## Run the Demo
```bash
python3 main.py
```

## Customize the Demo configuration

### Open up the configuration file to set:
* Streams: URIs links out of 1-to-8 supported, and its Triggers
* Triggers: That may contain Actions & Filters
* Actions: Video recording & logging to file
* Filters: That specifies what to detect in the inference

```bash
editor config.yaml
```

![demo_config_file](demo_config_file.gif)


In order to create RTSTP URIs from a YouTube server for example, the following commands will help:
```bash
LINK="https://www.youtube.com/watch?v=faUNhaRLpMc&ab_channel=ProwalkTours"
youtube-dl --format "18[ext=mp4][protocol=https]" --get-url "$LINK"
```

The output link can be used in the `config.yaml` stream's URI as showed in the GIF above.
