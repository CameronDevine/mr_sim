from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="mr_sim",
    version="1.0.1",
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
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.4",
    install_requires=["numpy", "scipy"],
    url="https://github.com/CameronDevine/mr_sim",
)
