from pointcloud.pointmap import PointMap

END_HEADER_VALUE = "end_header"
POINT_CLOUD_HEADER_PREFIX = "element vertex"
class FileDataExtractor:
    def __init__(self, fileName, perspective):
        self.fileName = fileName
        self.perspective = perspective

    def extractPointCloud(self):
        f = open(self.fileName, "r")
        pointCount = self.getPointCount(f)
        zPointMap = self.getPointDict(f, pointCount)
        return zPointMap

    def getPointDict(self, f, numCoords):
        currLine = f.readline()
        while not currLine.startswith(END_HEADER_VALUE):
            currLine = f.readline()
        
        pointMap = PointMap(self.perspective)

        for i in range(0, int(numCoords)):
            coordList = f.readline().split(" ")
            pointMap.addPoint(coordList)

        pointMap.computeMinMaxKeys()
        return pointMap

    def getPointCount(self, f):
        currLine = f.readline()
        while not currLine.startswith(POINT_CLOUD_HEADER_PREFIX):
            currLine = f.readline()
        
        splitLine = currLine.split(" ")

        return splitLine[2]

