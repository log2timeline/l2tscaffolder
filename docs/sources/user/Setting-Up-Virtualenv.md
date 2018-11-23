# Setting up L2t scaffolder in a virtualenv

For development purposes, l2t\_scaffolder can be installed using virtualenv
(preferred method).

## Fedora Core

### Install virtualenv

To install virtualenv on Fedora Core (or equivalent) run:
```
$ sudo dnf install python3-virtualenv
```

### Installing build dependencies

**TODO add more text**

## Ubuntu

### Installing virtualenv

To install virtualenv on Ubuntu (or equivalent) run:
```
$ sudo apt-get install python-virtualenv python3-virtualenv
```

### Installing build dependencies

**TODO add more text**

```
$ sudo apt-get install libyaml-dev liblzma-dev
```

## Setting up l2t\_scaffolder in virtualenv

To create a virtualenv:
```
virtualenv -p PATH_TO_PYTHON3 scaffolderoenv
```
eg:

```
$ virtualenv -p /usr/bin/python3 scaffolderoenv
```

To activate the virtualenv:

```
$ source ./scaffolderenv/bin/activate
```

**Note that using pip outside virtualenv is not recommended since it ignores
your systems package manager.**

Make sure that pip is up-to-date:

```
$ pip3 install --upgrade pip
```

## Deactivate Virtualenv

To deactivate the virtualenv run:

```
$ deactivate
```

