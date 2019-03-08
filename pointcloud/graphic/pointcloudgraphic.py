from pointcloud.pointmap import PointMap
from graphic.circle import Circle
from tkinter import *
from image.imagedrawing import ImageDrawing

class PointCloudGraphic:
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    POINT_RADIUS = 1
    FILE_NAME_PREFIX = "cross-section-"
    SCALE_FACTOR = 0.66666

    def __init__(self, pointMap, csThickness, destinationFile, imageWidth, imageHeight, xOffset = None, yOffset = None):
        if xOffset is None:
            self.xOffset = 0
        
        if yOffset is None:
            self.yOffset = 0

        self.pointMap = pointMap
        self.csThickness = csThickness
        self.csIteratorIndex = 0
        self.destinationFile = destinationFile
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight

        self.__computeGraphicProperties()
        self.__precomputeCrossSections()

    def __computeGraphicProperties(self):
        self.__computeAxisLabels()
        self.__computeWidth()
        self.__computeHeight()
        self.__computeScale()
        self.__computeScaledBounds()
        self.__computeScaledCenter()
        self.__computeScaledHeight()
        self.__computeScaledWidth()
        self.__computeOrientation()

    def __computeWidth(self):
        self.width = self.pointMap.maxComps[self.axisLabels[0]] - self.pointMap.minComps[self.axisLabels[0]]
    
    def __computeHeight(self):
        self.height = self.pointMap.maxComps[self.axisLabels[1]] - self.pointMap.minComps[self.axisLabels[1]]

    def __computeScale(self):
        self.scale = self.imageWidth * self.SCALE_FACTOR / self.width
        if (self.height * self.scale) > self.imageHeight:
            self.scale = self.imageHeight * self.SCALE_FACTOR / self.height

    def __computeOrientation(self):
        self.orientation = self.LANDSCAPE if self.width > self.height else self.PORTRAIT

    def __computeAxisLabels(self):
        self.axisLabels = self.pointMap.perspective.getComplementValues()

    def __computeScaledWidth(self):
        self.width = self.rightBound - self.leftBound 

    def __computeScaledHeight(self):
        self.height = self.bottomBound - self.topBound

    def __computeScaledBounds(self):
        self.__computeRightBound()
        self.__computeBottomBound()
        self.__computeTopBound()
        self.__computeLeftBound()

    def __computeRightBound(self):
        self.rightBound = self.pointMap.maxComps[self.axisLabels[0]] * self.scale

    def __computeBottomBound(self):
        self.bottomBound = self.pointMap.maxComps[self.axisLabels[1]] * self.scale

    def __computeLeftBound(self):
        self.leftBound = self.pointMap.minComps[self.axisLabels[0]] * self.scale

    def __computeTopBound(self):
        self.topBound = self.pointMap.minComps[self.axisLabels[1]] * self.scale

    def __computeScaledCenter(self):
        self.centerX = (self.rightBound + self.leftBound)/2
        self.centerY = (self.bottomBound + self.topBound)/2

    def __precomputeCrossSections(self):
        minKey = self.pointMap.getMinKey()
        maxKey = self.pointMap.getMaxKey()
        self.crossSections = []
        self.imageDrawingList = []

        while minKey <= maxKey:
            startLayer = minKey
            endLayer = minKey + self.csThickness
            endLayer = maxKey if endLayer > maxKey else (minKey + self.csThickness)

            self.crossSections.append(self.__aggregateLayers(startLayer, endLayer))
            self.imageDrawingList.append(ImageDrawing(self.destinationFile, self.imageWidth, self.imageHeight))
            minKey = endLayer + 1
        
        self.numCrossSections = len(self.crossSections)

    def __aggregateLayers(self, startLayer, endLayer):
        aggregatedLayers = []
        for i in range(startLayer, endLayer + 1):
            aggregatedLayers.extend(self.pointMap.getOrEmpty(i))
        
        return aggregatedLayers

    # Draws current cross section of the point cloud.  Automatically advances into
    # the next one after printing the current one.
    def drawCrossSection(self, targetCanvas, xTranslate = 0, yTranslate = 0):
        csCurrent = self.crossSections[self.csIteratorIndex]
        imageDrawingCurrent = self.imageDrawingList[self.csIteratorIndex]
        for i in range(0, len(csCurrent)):
            xPos = csCurrent[i][self.axisLabels[0]] * self.scale + xTranslate + self.xOffset
            yPos = csCurrent[i][self.axisLabels[1]] * self.scale + yTranslate + self.yOffset
            p = Circle(xPos, yPos, self.POINT_RADIUS)
            p.draw(targetCanvas)
            imageDrawingCurrent.addPoint(p)

        imageDrawingCurrent.saveImage(self.__generateCrossSectionFileName())
        self.csIteratorIndex = self.csIteratorIndex + 1

    def __generateCrossSectionFileName(self):
        return self.FILE_NAME_PREFIX + str(self.csIteratorIndex)

