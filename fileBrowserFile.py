import os
import math
from pathlib import Path

fileExtensions = {
    ".exe" : "Application",
    ".docx" : "Microsoft Word Document",
    ".mp3" : "Audio File",
    ".jpeg" : "JPEG File",
    ".png" : "PNG File",
    ".jpg" : "JPG File",
    ".txt" : "Text Document",
    ".zip" : "Zip File",
    ".html" : "HTML File",
    ".py" : "Python File",
    ".dat" : "DAT File",
    ".ini" : "Configuration File"
}

class FileBrowserFile():
    def __init__(self, path):
        self.Name = os.path.basename(path)
        self.Type = self.getFileType(path)
        self.Size = str(math.ceil(os.path.getsize(path) / 1024)) + " kb"

    def getFileType(self, path):
        placeHolderString = ""
        if Path(path).suffix in fileExtensions:
            return fileExtensions.get(Path(path).suffix, False)
        elif os.path.isdir(path) == True:
            return "Directory"
        else:
            placeHolderString = os.path.splitext(path)[1] + " File" 
            return placeHolderString