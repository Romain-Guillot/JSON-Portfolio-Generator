import os

import json
from distutils.dir_util import copy_tree
import subprocess
import logging
import shutil

from lib.github_service import GithubService
from lib.sass_service import SassService
from lib.pdf_service import PDFService
from lib.jinja_service import JinjaService
from lib.config import Config


def loadData(config) :
    """.
    return the data dictionnary from the json file.
    append the config dictionnary to the result, available through the `config`
    key
    """
    dataFilename = config['data']
    with open(dataFilename, 'r') as data_file :
        data = json.loads(data_file.read())
        return {'config': config.config, **data}


def prepareOutputDir(config) :
    """
    (re)create the output directories
    copy the assets dir into the output dir
    """
    OUTPUT_DIR = config['output']
    ASSETS_DIR = config['src']['static']
    
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    OUTPUT_ASSET_DIR = os.path.join(OUTPUT_DIR, ASSETS_DIR)
    if os.path.exists(OUTPUT_ASSET_DIR):
        shutil.rmtree(OUTPUT_ASSET_DIR)
    os.makedirs(OUTPUT_ASSET_DIR)
    copy_tree(ASSETS_DIR, OUTPUT_ASSET_DIR)


def publishOnGithub(config) :
    """
    Publish the output directory in the default git remote
    """
    publicationRequired = config['git_publish']
    if publicationRequired :
        GithubService(OUTPUT_DIR).publish()


def renderPages(config, data) :
    """
    Built the html of all pages : index, resume, projects and one page for
    each project
    """
    OUTPUT_DIR = config['output']
    TEMPLATE_DIR = config['src']['templates']

    jinjaService = JinjaService(TEMPLATE_DIR, OUTPUT_DIR)
    jinjaService.renderPage("index", None, data, data["meta"]["description-index"])
    jinjaService.renderPage("resume", "Résumé", data, data["meta"]["description-index"])
    jinjaService.renderPage("projects", "Projects", data, data["meta"]["description-index"])

    for project in data['projects'] :
        project_data = {'project': project, **data}
        jinjaService.renderPage('project_details', project['title'], project_data, project['description'], project['id'])



def buildStyle(config) :
    ASSETS_DIR = config['src']['static']
    OUTPUT_DIR = config['output']
    SassService(ASSETS_DIR, OUTPUT_DIR).compile()


if __name__ == '__main__' :
    # logging.getLogger().setLevel(logging.INFO)
    config = Config("config.yml")
    prepareOutputDir(config)
    data = loadData(config)
    renderPages(config, data)
    buildStyle(config)
    
    # PDFService("/usr/bin/google-chrome", "file:///home/ob/Documents/projects/Active/Portfolio/build/resume.html").build()
    
