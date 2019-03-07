from pointcloud.render.pointcloudrenderengine import PointCloudRenderEngine

POINT_CLOUD_FILE_NAME = "humancloud.ply"

def main():
    renderEngine = PointCloudRenderEngine(POINT_CLOUD_FILE_NAME, "X", 4.5)
    renderEngine.render()

if __name__ == '__main__':
    main()