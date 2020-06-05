import os
import chevron

import json
from distutils.dir_util import copy_tree
import subprocess
import logging

from lib.github_service import GithubService
from lib.sass_service import SassService
from lib.pdf_service import PDFService

OUTPUT_DIR = "build"
TEMPLATE_DIR = "templates"
PARTIALS_DIR = os.path.join(TEMPLATE_DIR, "partials")
ASSETS_DIR = "static"


def loadData() :
    with open('data.json', 'r') as data_file :
        data = json.loads(data_file.read())
        return data


def renderPage(config) :
    with open(os.path.join(TEMPLATE_DIR, 'body.mustache'), 'r') as body_file, \
         open(os.path.join(PARTIALS_DIR, 'header.mustache'), 'r') as header_file :
        header_html = chevron.render(header_file, {config['page']: True, **config})
        args = {
            'template': body_file.read(), 
            'partials_path': "templates/partials/",
            'data': {
                'header': header_html,
                **config
            },
        }
        return chevron.render(**args)


def buildPage(page, name, data) :
    with open(os.path.join(TEMPLATE_DIR, page + ".mustache"), 'r') as template_file, \
         open(os.path.join(OUTPUT_DIR, page + ".html"), 'w') as output_file :
        args = {'template': template_file.read(), 'partials_path': "templates/partials/", 'data': data}
        config = {
            'page': name,
            'is-'+page: True,
            'body': chevron.render(**args),
            'description-page': data["meta"]["description-" + page],
            **data,
        }
        page = renderPage(config)
        output_file.write(page)


# WIP: not yet stable



def prepareOutputDir() :
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    copy_tree(ASSETS_DIR, os.path.join(OUTPUT_DIR, ASSETS_DIR))




with open(os.path.join(TEMPLATE_DIR, 'body.mustache'), 'r') as body_file  :
    logging.getLogger().setLevel(logging.INFO)
    prepareOutputDir()
    data = loadData()
    homepage_html = buildPage("index", None, data)
    resume_html = buildPage("resume", "Résumé", data)
    projects_html = buildPage("projects", "Projects", data)
    SassService(ASSETS_DIR, OUTPUT_DIR).compile()
    GithubService(OUTPUT_DIR).publish()
    PDFService("/usr/bin/google-chrome", "file:///home/ob/Documents/projects/Active/Portfolio/build/resume.html").build()
    
    logging.info("Protfolio created. See the " + OUTPUT_DIR + " directory.")
