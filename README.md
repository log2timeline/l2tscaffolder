# L2tScaffolder
L2tScaffolder is a tool that provides scaffolders for various open source projects. It can be used to bootstrap plugin or parser generation for tools like plaso, to make development work easier.

### Project status
[Travis-CI](https://travis-ci.org/) | [Codecov](https://codecov.io/)
--- | ---
[![Build Status](https://travis-ci.org/log2timeline/PlasoScaffolder.svg?branch=master)](https://travis-ci.org/log2timeline/PlasoScaffolder) | [![codecov](https://codecov.io/gh/log2timeline/PlasoScaffolder/branch/master/graph/badge.svg)](https://codecov.io/gh/log2timeline/PlasoScaffolder)

### Documentation

The purpose of the l2t scaffolder tool is to simplify development of various
open source forensics tools, eg. plaso, timesketch, turbinia, etc.

The tool simply provides a UI prompting the user to answer few questions, and
then generates templates for all files needed to write a parser or a plugin for
the appropriate tool, that is it provides scaffolding for the necessary boiler
plate code that is sometimes associated with creating new plugins or parsers.

### Usage

In essence the tool can be simply run as:

```
$ l2t_scaffolder.py
```

The tool will then guide you towards creating all the necessary files to
generate a parser, plugin or a module for the given tool. Another way to run
the tool is:

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

### Background
The original tool was called PlasoScaffolder, which was written by
[Claudia Saxer](https://github.com/ClaudiaSaxer) as part of her BSc and
integrated into the log2timeline organization for purpose of maintenance.

L2tScaffolder is a rewrite of the original PlasoScaffolder tool, reusing parts
of it, and rewriting other parts to make the tool easier to extend to other
open source projects and scaffolders, the original tool was written for plaso
and only supported SQLite plugins.
