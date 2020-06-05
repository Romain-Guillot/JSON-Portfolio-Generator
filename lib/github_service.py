import subprocess

class GithubService:
    """
    Service to publish updates in a git repository
    """
    def __init__(self, dirPath) :
        self.dirPath = dirPath

    def publish(self) :
        gitStatusResult = subprocess.run(["git", "status"], cwd=self.dirPath)
        if gitStatusResult.returncode != 0 :
            raise Exception("Repo doesn't exist")
        subprocess.run(["git", "add", "--all"], cwd=self.dirPath)
        subprocess.run(["git", "commit", "-m", "Automatically add generated file"], cwd=self.dirPath)
        subprocess.run(["git", "push", "origin", "master"], cwd=self.dirPath)
        