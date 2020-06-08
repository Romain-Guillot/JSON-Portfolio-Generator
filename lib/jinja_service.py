import os
from jinja2 import Environment, FileSystemLoader, Markup
import markdown


class JinjaService :
    def __init__(self, templateDir, outputDir) :
        file_loader = FileSystemLoader(templateDir)
        self.env = Environment(loader=file_loader)
        md = markdown.Markdown(extensions=['meta'])
        self.env.filters['markdown'] = lambda text: Markup(md.convert(text))
        self.OUTPUT_DIR = outputDir;

    
    def renderPage(self, filename, page_title, data, description, output_file=None) :
        if output_file is None :
            output_file = filename
        template = self.env.get_template(filename + ".j2")
        with open(os.path.join(self.OUTPUT_DIR, output_file + ".html"), 'w') as output_file :
            config = {
                'page': page_title,
                'is_'+filename: True,
                'description_page': description,
                **data,
            }
            page = template.render(config)
            output_file.write(page)
