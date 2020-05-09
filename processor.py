import os
import chevron
import sass
import json
from distutils.dir_util import copy_tree
import subprocess


OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"
ASSETS_DIR = "assets"


def loadData() :
    with open('data.json', 'r') as data_file :
        data = json.loads(data_file.read())
        return data


def renderPage(config) :
    with open(os.path.join(TEMPLATE_DIR, 'body.mustache'), 'r') as body_file, \
         open(os.path.join(TEMPLATE_DIR, 'header.mustache'), 'r') as header_file :
        header_html = chevron.render(header_file, {config['page']: True})
        return chevron.render(body_file, {'header': header_html, **config})


def makeHomepage(data) :
    with open(os.path.join(TEMPLATE_DIR, 'home.mustache'), 'r') as homepage_file, \
         open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as output_file :
        config = {
            'page': 'homepage',
            'title': "Romain Guillot",
            'body': chevron.render(homepage_file, data)
        }
        page = renderPage(config)
        output_file.write(page)
        return page


def makeResume(data) :
    with open(os.path.join(TEMPLATE_DIR, 'resume.mustache'), 'r') as homepage_file, \
         open(os.path.join(OUTPUT_DIR, 'resume.html'), 'w') as output_file :
        config = {
            'page': 'resume',
            'title': "Romain Guillot - Resumé",
            'body': chevron.render(homepage_file, data)
        }
        page = renderPage(config)
        output_file.write(page)
        return page


def makeProjects() :
    with open(os.path.join(TEMPLATE_DIR, 'projects.mustache'), 'r') as homepage_file, \
         open(os.path.join(OUTPUT_DIR, 'projects.html'), 'w') as output_file :
        config = {
            'page': 'projects',
            'title': "Romain Guillot - Projects",
            'body': chevron.render(homepage_file, data)
        }
        page = renderPage(config)
        output_file.write(page)


def makePDF():
    subprocess.run("/usr/bin/google-chrome-unstable --headless --disable-gpu --print-to-pdf-no-header --print-to-pdf file:///home/ob/Documents/projects/Done/Portfolio/output/resume.html", shell=True, check=True)


def makeStyle() :
    with open(os.path.join(ASSETS_DIR, 'style.scss'), 'r') as style_file, \
         open(os.path.join(OUTPUT_DIR, 'style.css'), 'w') as style_output_file :
        style = sass.compile(string=style_file.read(), include_paths=["assets"], output_style="expanded")
        style_output_file.write(style)
        return style

def prepareOutputDir() :
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    copy_tree("assets/", "output/assets/")


with open(os.path.join(TEMPLATE_DIR, 'body.mustache'), 'r') as body_file  :
    prepareOutputDir()
    data = loadData()
    homepage_html = makeHomepage(data)
    resume_html = makeResume(data)
    syle_css = makeStyle()
    projects_html = makeProjects()
    makePDF()

















# eof
