import os
import sass

class SassService:
    """
    Service to compile .scss files
    """
    def __init__(self, workingDir, outputDir, filename="style"):
        self.workingDir = workingDir
        self.outputDir = outputDir
        self.filename = filename

    def compile(self) :
        with open(os.path.join(self.workingDir, self.filename + '.scss'), 'r') as style_file, \
             open(os.path.join(self.outputDir, self.filename + '.css'), 'w') as style_output_file :
            style = sass.compile(string=style_file.read(), include_paths=[self.workingDir], output_style="expanded")
            style_output_file.write(style)
            return style