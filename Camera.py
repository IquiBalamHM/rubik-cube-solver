import cv2
import numpy as np
class Camera:
    def stop(self):
        if self.camera == 'WebCam':
            self.cap.release()
        elif self.camera =='Intel':
            self.pipeline.stop()
    def getFrame(self):
        if self.camera == 'WebCam':
            success, image = self.cap.read()
            return success,image

        elif self.camera =='Intel':
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                success = False
            else:
                success = True
            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            return success,color_image

    def __init__(self,selection = "WebCam"):
        if selection== 'Intel':
            self.camera = 'Intel'
            import pyrealsense2 as rs
            # Configure depth and color streams
            self.pipeline = rs.pipeline()
            config = rs.config()

            # Get device product line for setting a supporting resolution
            pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
            pipeline_profile = config.resolve(pipeline_wrapper)
            device = pipeline_profile.get_device()
            device_product_line = str(device.get_info(rs.camera_info.product_line))

            #config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

            if device_product_line == 'L500':
                config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
            else:
                config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

            # Start streaming
            self.pipeline.start(config)

        else:
            self.cap = cv2.VideoCapture(0)
            self.camera = 'WebCam'
        