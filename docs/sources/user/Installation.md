# Installing the Tool

There are two ways to install the tool:

1. Use pip
2. Source from github

Let's cover both ways. But the first recommended step is to setup a virtualenv
environment.

Follow the instructions
[here](Setting-Up-Virtualenv.md) or a quick method:

```
$ virtualenv -p /usr/bin/python3 scaffolder
$ source scaffolder/bin/activate
```

Once the virtual environment is setup you can move on to the next step, either
using pip or source installation.

## Pip Install

To install the latest release of the scaffolder, use:

```
$ pip3 install --upgrade l2tscaffolder
```

## Install From Sources

First fetch the latest source code from github:

```
$ git clone https://github.com/log2timeline/l2tscaffolder.git
```

Then install dependencies and compile and install the tool:

```
$ cd l2tscaffolder
$ pip3 install -r requirements.txt
$ python3 setup.py build && python3 setup.py install
```

