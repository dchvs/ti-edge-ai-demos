# TI EdgeAI Demos
> Demos to show the powerful capabilities of TI Edge AI SDK on J7 platform
## Building the Project
To build the project, run the following commands:
```bash
./setup.py test
sudo -H ./setup.py install
``` 
### Building for Development
If you are a project maintainer or just with to contribute to the project, we recommend building the project as:
```bash
sudo -H pip3 install pre-commit
./setup.py test
sudo -H ./setup.py develop
```