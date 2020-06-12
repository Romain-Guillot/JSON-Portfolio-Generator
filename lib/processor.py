import os, sys

import json
from distutils.dir_util import copy_tree
import subprocess
import logging
import shutil
import webbrowser

from lib.github_service import GithubService
from lib.sass_service import SassService
from lib.pdf_service import PDFService
from lib.jinja_service import JinjaService
from lib.config_yaml import ConfigYAML


class Processor :
    """
    Manage all process to generate the portfolio
    Baiscally a sequence of calls to the different services

    Note: the current directory has to be the directory where the build folder
    will be created
    """
    def __init__(self):
        self.config = ConfigYAML("config.yml")
        self.data = self.loadData()
        SRC_DIR = sys.path[0]  # the directory with the templates and static assets like images
        self.OUTPUT_DIR = self.config['output']
        self.STATIC_DIR = os.path.join(SRC_DIR, "static")
        self.TEMPLATE_DIR = os.path.join(SRC_DIR, "templates")
        self.process()
        # self.open()


    def process(self):
        """
        Sequence of process
        """
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
        clear the output directory excpet the hidden folder / files
        copy the static dir into the output dir
        copy the user assets dir into the output dir
        """
        # Create the build dir if not exists
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        # Clear the build dir except the hidden files / folder as .git  folder
        for filename in os.listdir(self.OUTPUT_DIR):
            file_path = os.path.join(self.OUTPUT_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path) and filename[0] != ".":
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        # Copy the static dir
        OUTPUT_STATIC_DIR = os.path.join(self.OUTPUT_DIR, "static")
        os.makedirs(OUTPUT_STATIC_DIR)
        copy_tree(self.STATIC_DIR, OUTPUT_STATIC_DIR)

        # Copyt the assets dir
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
        """
        Build / compile the stylesheets files
        """
        SassService(self.STATIC_DIR, self.OUTPUT_DIR).compile()


    def buildPDF(self) :
        """
        Generate the portfolio PDF (the portfolio "book" and the resume)
        """
        pdfGenerationRequired = self.config['pdf_generation']
        if pdfGenerationRequired :
            pdfService = PDFService(self.config['chromium'])
            filenames = [
                os.path.join(os.getcwd(), self.OUTPUT_DIR, "index"),
                os.path.join(os.getcwd(), self.OUTPUT_DIR, "resume"),
                os.path.join(os.getcwd(), self.OUTPUT_DIR, "projects"),
            ]
            filenames.extend(os.path.join(os.getcwd(), self.OUTPUT_DIR, project['id']) for project in self.data['projects'])
            pdfService.build(filenames)


    def open(self):
        webbrowser.open_new_tab(os.path.join(self.OUTPUT_DIR, "index.html"))
