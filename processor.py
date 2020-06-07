import os

import json
from distutils.dir_util import copy_tree
import subprocess
import logging

from lib.github_service import GithubService
from lib.sass_service import SassService
from lib.pdf_service import PDFService
from lib.jinja_service import JinjaService
from lib.config import Config


def loadData(config) :
    dataFilename = config['data']
    logging.info("Data file : " + dataFilename)
    with open(dataFilename, 'r') as data_file :
        data = json.loads(data_file.read())
        return {'config': config.config, **data}


def prepareOutputDir(config) :
    OUTPUT_DIR = config['output']
    ASSETS_DIR = config['src']['static']['dir']
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(os.path.join(OUTPUT_DIR, "projects")):
        os.makedirs(os.path.join(OUTPUT_DIR, "projects"))
    copy_tree(ASSETS_DIR, os.path.join(OUTPUT_DIR, ASSETS_DIR))


def publishOnGithub(config) :
    publicationRequired = config['git_publish']
    if publicationRequired :
        logging.info("Github publication enable")
        GithubService(OUTPUT_DIR).publish()
    else :
        logging.info("Github publication disable")


def renderPages(config, data) :
    OUTPUT_DIR = config['output']
    jinjaService = JinjaService("templates", OUTPUT_DIR)
    jinjaService.renderPage("index", None, data, data["meta"]["description-index"])
    jinjaService.renderPage("resume", "Résumé", data, data["meta"]["description-index"])
    jinjaService.renderPage("projects", "Projects", data, data["meta"]["description-index"])

    for project in data['projects'] :
        data = {'project': project, **data}
        jinjaService.renderPage('project_details', project['title'], data, project['description'], project['id'])



def buildStyle(config) :
    ASSETS_DIR = config['src']['static']['dir']
    OUTPUT_DIR = config['output']
    SassService(ASSETS_DIR, OUTPUT_DIR).compile()


if __name__ == '__main__' :
    logging.getLogger().setLevel(logging.INFO)

    config = Config("config.yml")
    prepareOutputDir(config)
    data = loadData(config)
    renderPages(config, data)
    buildStyle(config)
    
    # PDFService("/usr/bin/google-chrome", "file:///home/ob/Documents/projects/Active/Portfolio/build/resume.html").build()
    
    # logging.info("Protfolio created. See the " + OUTPUT_DIR + " directory.")
