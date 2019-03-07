from tkinter import *
from pointcloud.filedataextractor import FileDataExtractor 
from pointcloud.pointmap import PointMap

class RenderEngine:
    DEFAULT_CANVAS_WIDTH = 1500
    DEFAULT_CANVAS_HEIGHT = 1500 

    def __init__(self, width = None, height = None):
        if width is None:
            self.width = self.DEFAULT_CANVAS_WIDTH
        if height is None:
            self.height = self.DEFAULT_CANVAS_HEIGHT
        self.tkMaster = Tk()
        self.canvas = Canvas(self.tkMaster, 
                width=self.width,
                height=self.height)
        self.canvas.pack()

    def render(self):
        mainloop()