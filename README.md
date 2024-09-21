# Oasis technical test – Python
See Oasis_tech_test_Python.pdf for task details

## Installation
### Python
Make sure you have a local python environment already installed for development.
See setup.py for important required dependencies
#### Optional
I personally use conda to manage multiple environments, to create the environment I used, have conda already installed and run the following:
```bash
conda env create -f environment.yml
```

### CLI
To install the and use the CLI, run the following:
```bash
git clone <this-repository>
cd <this-repository>
pip install .
gethurricaneloss -h #To test it works and find out the arguments
```

### Benchmarking
If you want to generate the benchmark.png image run the following:
```bash
python3 scripts/benchmark.py
```