import subprocess

# TODO: NOT STABLE - Work in progress (waiting fro chromium update)
class PDFService :

    def __init__(self, chromeBin):
        self.chromeBin = chromeBin

    def build(self, filenames):
        for file in filenames :
            inFile = file + ".html"
            outFile = file + ".pdf"
            command = '{} --headless --disable-gpu --print-to-pdf="{}" --print-to-pdf-no-header {}'.format(self.chromeBin, outFile, inFile)
            subprocess.run(command, shell=True, check=True)
        self._combine(filenames)

    def _combine(self, filenames) :
        pass