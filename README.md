# **do-function-tester** A small codebase to test DigitalOcean Function `blocking=false` functionality

> Code repository author: [Alexandre Harano](mailto:email@ayharano.dev)

This project provides a small [DigitalOcean Function](https://docs.digitalocean.com/products/functions/)
using Python to validate `blocking=false` functionality.

# Project Installation
First, clone this repo:

```shell
$ git clone https://github.com/ayharano/do-function-tester.git
```

After cloning the repository, change the directory to the project root.
All instructions below, including configuring the virtual environment and running the project,
depend on being in the project root directory.

## Consistency of contributions using `pre-commit`

To maintain consistency between individual commits,
this repo is adopting the use of [`pre-commit`](https://pre-commit.com/).

The recommended way to install it for this repo is by installing via [`pipx`](https://pipx.pypa.io/stable/).
After installing `pipx`, issue the following commands:

```shell
$ pipx install pre-commit
$ pre-commit install --install-hooks --overwrite
```

`pre-commit` is configured to also run per push and pull requests in GitHub workflow.

## Python Version and Virtual Environment Setup
This project was tested by using CPython 3.10. In order to keep multiple versions of the Python interpreter, we recommend the use of pyenv.

- pyenv (Linux, macOS): [link](https://github.com/pyenv/pyenv)
- pyenv for Windows (Windows): [link](https://pyenv-win.github.io/pyenv-win/)

Once it is installed, we can use the same version as the one used during this project development, which was CPython 3.12.1.

Run the following:
```shell
$ pyenv install 3.10.3  # install CPython 3.10.3
$ pyenv local 3.10.3    # select CPython 3.10.3 as the local interpreter
```

As a directory name for the virtual env, for this tutorial we will use it as `virtualenvironment`.
If you prefer another name, just replace all the occurrences from here.

To install a virtual env, run the following:

```shell
$ python -m venv virtualenvironment
```

This way, a directory named `virtualenvironment` will be created at the project root to store the Python project dependencies.

## Using the local virtual env

Regarding the installation and the use of virtual envs, more details can be found at [the `venv` module documentation](https://docs.python.org/3/library/venv.html).

To use the virutal env, the instructions depend on the target operating system:

- venv for Linux or macOS

```shell
$ source virtualenvironment/bin/activate
```

- venv for Windows (PowerShell)

```powershell
virtualenvironment\Scripts\Activate.ps1
```

## Installing the project dependencies in the virtual env

Once the virtual env is activated, run:

```shell
python -m pip install --upgrade pip && python -m pip install --editable '.[local]' && python -m pip install --upgrade tzdata
```

This command is a chained call of 3 executions, being
1. upgrading the local `pip` to its most recent version
2. installing all the project dependencies, including the ones for local dev use, and installing the project as [an editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), and
3. enforce the most recent version of `tzdata`, which is used by Python to manage timezone data without relying on the data from the target operating system (more details at [the `zoneinfo` module documentation](https://docs.python.org/3/library/zoneinfo.html))
