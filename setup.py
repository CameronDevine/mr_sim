from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="mr_sim",
    version="0.0.1",
    author="Cameron Devine",
    author_email="camdev@uw.edu",
    description="A package for the simulation of abrasive material removal processes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
)
