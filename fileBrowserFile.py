import os
import math
from pathlib import Path

fileExtensions = {
    ".exe": ("Application", "application-terminal.png"),
    ".docx": ("Microsoft Word Document", "document-word-text.png"),
    ".mp3": ("Audio File", "music.png"),
    ".jpeg": ("JPEG File", "picture.png"),
    ".png": ("PNG File", "picture.png"),
    ".jpg": ("JPG File", "picture.png"),
    ".txt": ("Text Document", "paper-clip.png"),
    ".zip": ("Zip File", "folder-zipper.png"),
    ".html": ("HTML File", "json.png"),
    ".py": ("Python File", "bin-metal-full­.png"),
    ".ini": ("Configuration File", "wheel.png")
}

class FileBrowserFile():
    def __init__(self, path):
        self.Path = path
        self.Size = str(math.ceil(os.path.getsize(path) / 1024)) + " kb"
        self.Name = os.path.basename(path)
        self.Type = self.getFileType(path)

        if self.Type == 'Directory':
            self.IconPath = os.path.join(os.getcwd(), 'fileIcons', 'icons', "folder.png")
        elif Path(path).suffix in fileExtensions:
            iconName = fileExtensions.get(Path(path).suffix.lower(), False)[1]
            self.IconPath = os.path.join(os.getcwd(), 'fileIcons', 'icons', iconName)
        else:
            self.IconPath = os.path.join(os.getcwd(), 'fileIcons', 'icons', "application-blue.png")

    def getFileType(self, path):
        if Path(path).suffix in fileExtensions:
            return fileExtensions.get(Path(path).suffix.lower(), False)[0]
        elif os.path.isdir(path) == True:
            return "Directory"
        else:
            return os.path.splitext(path)[1] + " File" 
