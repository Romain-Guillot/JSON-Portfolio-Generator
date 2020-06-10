import yaml

class ConfigYAML :
    """
    Load a yaml file to get a directionnay
    Simply use the yaml python package
    """
    def __init__(self, filename) :
        self.config = self._loadConfigFile(filename)
    
    def __getitem__(self, key):
        return self.config[key]

    def _loadConfigFile(self, filename) :
        with open(filename) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
            