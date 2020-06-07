import os
from jinja2 import Environment, FileSystemLoader

class JinjaService :
    def __init__(self, templateDir, outputDir) :
        file_loader = FileSystemLoader(templateDir)
        self.env = Environment(loader=file_loader)
        self.OUTPUT_DIR = outputDir;

    
    def renderPage(self, filename, pageTitle, data) :
        template = self.env.get_template(filename + ".j2")
        with open(os.path.join(self.OUTPUT_DIR, filename + ".html"), 'w') as output_file :
            config = {
                'page': pageTitle,
                'is_'+filename: True,
                'description_page': data["meta"]["description-" + filename],
                **data,
            }
            page = template.render(config)
            output_file.write(page)
