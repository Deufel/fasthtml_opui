# fasthtml_opui


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This Libary is designed as an educational project to make using the Open
Props UI Library easy to set up with a fast HTML Web App.

The first part of this app will build “vendor” the required css
structure for setting up the appplication to use; - [Open Props CSS
Custom Variables](https://open-props.style/) - [Open Props
UI](https://open-props-ui.netlify.app/)

## Developer Guide

If you are new to using `nbdev` here are some useful pointers to get you
started.

### Install fasthtml_opui in Development mode

``` sh
# make sure fasthtml_opui package is installed in development mode
$ pip install -e .

# make changes under nbs/ directory
# ...

# compile to have changes apply to fasthtml_opui
$ nbdev_prepare
```

## Usage

### Installation

Install latest from from [pypi](https://pypi.org/project/fasthtml_opui/)

``` sh
$ pip install fasthtml_opui
```

### Documentation

Documentation can be found hosted on this GitHub
[repository](https://github.com/Deufel/fasthtml_opui)’s
[pages](https://Deufel.github.io/fasthtml_opui/). Additionally you can
find package manager specific guidelines on
[conda](https://anaconda.org/Deufel/fasthtml_opui) and
[pypi](https://pypi.org/project/fasthtml_opui/) respectively.

## How to use

``` python
    from fasthtml.common import *
    # Import specific classes from fasthtml_opui
    from fasthtml_opui.core import OpenProps, OpenPropsSync
    
    # Initialize OpenProps syncer and sync files
    syncer = OpenPropsSync()
    syncer.sync_all()
    
    # Create FastHTML app
    app, rt = fast_app(hdrs=OpenProps('dark', 'cyan'), pico=False)
    
    @rt('/')
    def get():
        return Titled("Welcome",
            Article(
                H2("Hello World"),
                P("This is a FastHTML app using OpenProps UI"),
                Button("Click me!", cls="button")
            )
        )
    
    serve()
```
