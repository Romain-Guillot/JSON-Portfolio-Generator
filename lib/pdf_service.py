import subprocess

# TODO: NOT STABLE - Work in progress (waiting fro chromium update)
class PDFService :

    def __init__(self, chromeBin, outputFile):
        self.chromeBin = chromeBin
        self.outputFile = outputFile

    def build(self):
        subprocess.run(self.chromeBin + " --headless --disable-gpu --print-to-pdf-no-header --print-to-pdf " + self.outputFile, shell=True, check=True)
