import os, sys

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


class Processor :
    """
    Manage all process to generate the portfolio
    Baiscally a sequence of calls to the different services (see lib/)
    """
    def __init__(self):
        self.config = Config("config.yml")
        self.data = self.loadData()
        SRC_DIR = sys.path[0]
        self.OUTPUT_DIR = self.config['output']
        self.STATIC_DIR = os.path.join(SRC_DIR, "static")
        self.TEMPLATE_DIR = os.path.join(SRC_DIR, "templates")
        self.process()


    def process(self):
        self.prepareOutputDir()
        self.renderPages()
        self.buildStyle()
        self.publishOnGithub()
        self.buildPDF()


    def loadData(self) :
        """.
        return the data dictionnary from the json file.
        append the config dictionnary to the result, available through the `config`
        key
        """
        dataFilename = self.config['data']
        with open(dataFilename, 'r') as data_file :
            data = json.loads(data_file.read())
            return {'config': self.config.config, **data}


    def prepareOutputDir(self) :
        """
        (re)create the output directories
        copy the STATIC dir into the output dir
        """
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        for filename in os.listdir(self.OUTPUT_DIR):
            file_path = os.path.join(self.OUTPUT_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path) and filename != ".git":
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        OUTPUT_STATIC_DIR = os.path.join(self.OUTPUT_DIR, "static")
        os.makedirs(OUTPUT_STATIC_DIR)
        copy_tree(self.STATIC_DIR, OUTPUT_STATIC_DIR)

        USER_ASSET_DIR = self.config['assets_dir']
        OUTPUT_USER_ASSET_DIR = os.path.join(self.OUTPUT_DIR, USER_ASSET_DIR)
        os.makedirs(OUTPUT_USER_ASSET_DIR)
        copy_tree(USER_ASSET_DIR, OUTPUT_USER_ASSET_DIR)


    def publishOnGithub(self) :
        """
        Publish the output directory in the default git remote
        """
        publicationRequired = self.config['git_publish']
        if publicationRequired :
            GithubService(self.OUTPUT_DIR).publish()


    def renderPages(self) :
        """
        Built the html of all pages : index, resume, projects and one page for
        each project
        """
        jinjaService = JinjaService(self.TEMPLATE_DIR, self.OUTPUT_DIR)
        jinjaService.renderPage("index", None, self.data, self.data["meta"]["description-index"])
        jinjaService.renderPage("resume", "Résumé", self.data, self.data["meta"]["description-resume"])
        jinjaService.renderPage("projects", "Projects", self.data, self.data["meta"]["description-projects"])
        for project in self.data['projects'] :
            project_data = {'project': project, **self.data}
            jinjaService.renderPage('project_details', project['title'], project_data, project['description'], project['id'])


    def buildStyle(self) :
        SassService(self.STATIC_DIR, self.OUTPUT_DIR).compile()


    def buildPDF(self) :
        PDFService("/usr/bin/google-chrome", "file:///home/ob/Documents/projects/Active/Portfolio/build/resume.html").build()



if __name__ == '__main__' :
    logging.getLogger().setLevel(logging.INFO)
    base_directory = sys.argv[1];
    os.chdir(base_directory)
    if len(sys.argv) < 2 :
        logging.error("Usage : preprocessor YOUR_DIRECTORY\nwith YOUT_DIRECTORY: the directory that contains the config file, your data file, your STATIC, etc.")
        sys.exit(1)
    Processor()
    
