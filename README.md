# JSON Portfolio Generator

**JSON Portfolio Generator** is a project to generate a portfolio from a JSON file.
The generated portfolio contains the following elements :

- an homepage with your photo and description
- a resume
- a page that lists your project
- a page for each of your project

The portfolio can be generated in two formats :
- **web format:** collection of web pages inter-connected
- **pdf format (*generated for the html files*):** 
    - a single document with the resume
    - the entire portfolio

Finally, **JSON Portfolio Generator** can automatically push the portfolio
to your remote as a Github Page repository for example to be published 
immediatly after the generation.


## Stack

**Python 3:** the core is written with Python
> Python is an interpreted, interactive, object-oriented programming language. 
> It incorporates modules, exceptions, dynamic typing, very high level dynamic 
> data types, and classes. It supports multiple programming paradigms beyond 
> object-oriented programming, such as procedural and functional programming. 
> Python combines remarkable power with very clear syntax. It has interfaces to 
> many system calls and libraries, as well as to various window systems, and is 
> extensible in C or C++. It is also usable as an extension language for 
> applications that need a programmable interface. Finally, Python is portable: 
> it runs on many Unix variants including Linux and macOS, and on Windows.  

**Jinja2** to define the html template pages
> Jinja is a modern and designer-friendly templating language for Python, 
> modelled after Django’s templates. It is fast, widely used and secure with the 
> optional sandboxed template execution environment.

**Sass:** to define the portfolio stylesheets
> Sass is a stylesheet language that’s compiled to CSS. It allows you to use 
> variables, nested rules, mixins, functions, and more, all with a fully 
> CSS-compatible syntax. Sass helps keep large stylesheets well-organized and 
> makes it easy to share design within and across projects.

**Headless Chromium** to generate the PDF files from the HTML files
> Headless Chromium allows running Chromium in a headless/server environment. 
> Expected use cases include loading web pages, extracting metadata (e.g., the DOM) 
> and generating bitmaps from page contents -- using all the modern web platform 
> features provided by Chromium and Blink.

## Utilisation

1. Download or clone the project
1. Go to the project directory
1. Install the requirements : `pip3 install -r requirements.txt`
1. Use `processor.py` to generate your portfolio 

Usage of `processor.py`: `python3 processor.py YOUR_DIRECTORY`

`YOUR_DIRECTORY` is te directory that contains your data, configuration and
assets such as your profile picture. The `example/` directory is an example of a 
such directory. This directory are to contains at least :
- `config.yml`: the configuration file
- `data.json`: your data (general personnal information, resume content, projects 
details)
- `assets/photo.jpg`: your photo

I recommend you to copy the `example` folder to begin.

**Note: before each generation, the build directory will be cleared except for
the hidden files or directories (the `.git/` folder will not be deleted for
example). So do not store anything in this folder, use your asset directory.**


## Example
The `example` folder contains the sources to create my portfolio published
on Github Page : [https://github.com/Romain-Guillot/Romain-Guillot.github.io](https://github.com/Romain-Guillot/Romain-Guillot.github.io)