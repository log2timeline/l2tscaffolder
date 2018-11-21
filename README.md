# L2tScaffolder
L2tScaffolder is a tool that provides scaffolders for various open source projects. It can be used to bootstrap plugin or parser generation for tools like plaso, to make development work easier.

### Project status
[Travis-CI](https://travis-ci.org/) | [Codecov](https://codecov.io/)
--- | --- | ---
[![Build Status](https://travis-ci.org/log2timeline/PlasoScaffolder.svg?branch=master)](https://travis-ci.org/log2timeline/PlasoScaffolder) | [![codecov](https://codecov.io/gh/log2timeline/PlasoScaffolder/branch/master/graph/badge.svg)](https://codecov.io/gh/log2timeline/PlasoScaffolder)

### Documentation
In essence the tool can be simply run as:

```
$ l2t_scaffolder.py
```

The tool will then guide you towards creating all the necessary files to generate a parser, plugin or a module for the given tool. Another way to run the tool is:

```
$ l2t_scaffolder.py <PROJECT>
```
  
eg:

```
$ l2t_scaffolder.py plaso 
```

This will run the scaffolder tool to generate a plugin or a parser for plaso.

Also see:

+ http://l2tscaffolder.readthedocs.io

### Requirements
Python 3.6+, Python 2 is not supported.

### Installation
pip install l2tscaffolder

### Background
The original PlasoScaffolder was written by [Claudia Saxer](https://github.com/ClaudiaSaxer)
as part of her BSc and integrated into the log2timeline organization for
purpose of maintenance.

The original version of the tool was then rewritten to l2t_scaffolder and the tool
extended to support other projects than plaso SQlite plugin generation.
