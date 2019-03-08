from pointcloud.render.pointcloudrenderengine import PointCloudRenderEngine
import sys
import os

POINT_CLOUD_FILE_NAME = "ply-data/person1.ply"
DESTINATION_DIR = "/Users/jacobsewell/Desktop/area0/cross-sections/person1/"

class CrossSectionGenArgs:
    def __init__(self, argv: list):
        self.inputFile = str(argv[1])
        self.destinationDir = str(argv[2])
        self.perspective = str(argv[3])
        self.csThickness = int(argv[4])     

def main():
    args = CrossSectionGenArgs(sys.argv)

    renderEngine = PointCloudRenderEngine(args.inputFile, args.destinationDir, args.perspective, args.csThickness)
    renderEngine.render()

if __name__ == '__main__':
    main()