from tkinter import *
from pointcloud.filedataextractor import FileDataExtractor 
from pointcloud.pointmap import PointMap
from render.renderengine import RenderEngine

class PointCloudRenderEngine(RenderEngine):
    DEFAULT_PADDING = 100
    POINT_RADIUS = 2.5
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"

    def __init__(self, targetFileName, perspective, scale, width = None, height = None):
        super().__init__(width, height)
        self.targetFileName = targetFileName
        self.perspective = perspective
        self.pointMap = (FileDataExtractor(self.targetFileName, self.perspective)).extractPointCloud()
        self.scale = scale
        self.width = self.pointMap.computeWidth() * self.scale
        self.height = self.pointMap.computeHeight() * self.scale
        self.orientation = self.__computeOrientation()

    def __computeOrientation(self):
        if self.width > self.height:
            return self.LANDSCAPE
        
        return self.PORTRAIT

    def render(self):
        self.drawCrossSections()
        super().render()

    def aggregateCrossSections(self, aggregateAmount, startInd):
        crossSections = []
        for i in range(startInd, startInd + aggregateAmount):
            crossSections.extend(self.pointMap.getOrEmpty(i))
        return crossSections

    def xTransform(self, val, isSecond):
        tVal = val * self.scale + self.DEFAULT_PADDING + self.width
        if isSecond and self.orientation is self.PORTRAIT:
            tVal = tVal + self.DEFAULT_PADDING * 2 + self.width

        return tVal

    def yTransform(self, val, isSecond):
        tVal = val * self.scale + self.DEFAULT_PADDING + self.height
        if isSecond and self.orientation is self.LANDSCAPE:
            tVal = tVal + self.DEFAULT_PADDING * 2 + self.height

        return tVal

    def drawCrossSections(self):
        pComplements = self.pointMap.perspective.getComplementValues()
        isSecond = 0
        aggregateCount = 15
        i = self.pointMap.getMinKey()

        while i <= self.pointMap.getMaxKey():
            crossSectionPoints = self.aggregateCrossSections(17, i)
            i += aggregateCount
            for j in range(0, len(crossSectionPoints)):
                centerX = self.xTransform(crossSectionPoints[j][pComplements[0]], isSecond)
                centerY = self.yTransform(crossSectionPoints[j][pComplements[1]], isSecond)
                x0 = centerX - self.POINT_RADIUS
                y0 = centerY - self.POINT_RADIUS
                x1 = centerX + self.POINT_RADIUS
                y1 = centerY + self.POINT_RADIUS
                self.canvas.create_oval(
                            x0, 
                            y0, 
                            x1, 
                            y1, 
                            fill="#476042"
                        )
            isSecond = 1 if not isSecond else 0

