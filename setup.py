from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hurricane-loss-model",
    version="1.0.0",
    author="Anish Kothikar",
    description="A command-line utility tool to estimate average annual hurricane losses in Florida and the Gulf states using Monte Carlo Simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SkylordA/oasis_takehome_task",

    packages=find_packages(where="src"),
    package_dir={"": "src"},       

    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19',
    ],

    entry_points={
        'console_scripts': [
            'gethurricaneloss=hurricane_loss_model.gethurricaneloss:get_hurricane_loss',
        ],
    },
)
