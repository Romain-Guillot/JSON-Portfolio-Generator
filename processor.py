import os
import chevron
import sass
import json
from distutils.dir_util import copy_tree
import subprocess
import logging


OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"
PARTIALS_DIR = os.path.join(TEMPLATE_DIR, "partials")
ASSETS_DIR = "assets"


def loadData() :
    with open('data.json', 'r') as data_file :
        data = json.loads(data_file.read())
        return data


def renderPage(config) :
    with open(os.path.join(TEMPLATE_DIR, 'body.mustache'), 'r') as body_file, \
         open(os.path.join(PARTIALS_DIR, 'header.ms'), 'r') as header_file :
        header_html = chevron.render(header_file, {config['page']: True, **config})
        args = {
            'template': body_file.read(), 
            'partials_path': "partials/",
            'partials_ext': 'ms',
            'data': {
                'header': header_html,
                **config
            },
        }
        return chevron.render(**args)


def buildPage(page, name, data) :
    with open(os.path.join(TEMPLATE_DIR, page + ".mustache"), 'r') as template_file, \
         open(os.path.join(OUTPUT_DIR, page + ".html"), 'w') as output_file :
        config = {
            'page': name,
            'body': chevron.render(template_file, data),
            **data,
        }
        page = renderPage(config)
        output_file.write(page)


# WIP: not yet stable
def buildPDF():
    subprocess.run("/usr/bin/google-chrome-unstable --headless --disable-gpu --print-to-pdf-no-header --print-to-pdf file:///home/ob/Documents/projects/Done/Portfolio/output/resume.html", shell=True, check=True)


def buildStyle() :
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
    logging.getLogger().setLevel(logging.INFO)
    prepareOutputDir()
    data = loadData()
    homepage_html = buildPage("index", None, data)
    resume_html = buildPage("resume", "Résumé", data)
    projects_html = buildPage("projects", "Projects", data)
    syle_css = buildStyle()
    logging.info("Protfolio created. See the " + OUTPUT_DIR + " directory.")
    # TODO: makePDF()
















# eof
