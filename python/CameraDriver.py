__version__ = '0.1.0'

import sys
import time
import os
import cv2
import math
from PIL import Image
import atexit
import Config as cfg
import numpy as np
import subprocess as sp


class Camera(object):
    def __init__(self, resolution=cfg.video_resolution):
        self.cameraProcess = None
        self.resolution = resolution
        self.is_enabled = False

        # pic dump stuff
        self.frame_n = 0
        self.pic_type = ''

        self.empty_scene = None
        self.reddit_template = cv2.imread(cfg.reddit_path,0)
        self.reddit_template = cv2.Canny(self.reddit_template, cfg.canny_min, cfg.canny_max)


    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)


    @staticmethod
    def _save_image(img, impath):
        im = Image.fromarray(img)
        im.save(os.path.join(cfg.saveimg_path, impath))


    def start(self):
        self.cap = cv2.VideoCapture(0)

        # Set resolution
        w, h = self.resolution
        self.cap.set(3,w)
        self.cap.set(4,h)
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, 40)
        # self.cap.set(cv2.CAP_PROP_FPS, 40)


    def stop(self):
        self.cap.release()


    def get_frame(self):
        _, img = self.cap.read()
        img[:,:,2] = np.zeros([img.shape[0], img.shape[1]])  # Remove red channel so laser can stay on
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        r_gray = gray
        # r_gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rblur_gray = cv2.GaussianBlur(r_gray, (21, 21), 0)

        # crop width
        rblur_gray = rblur_gray[:, cfg.crop_w_lower:cfg.crop_w_upper]

        if cfg.SAVE_FRAMES:
            self.frame_n += 1
            self._save_image(rblur_gray, '{}.jpg'.format(self.frame_n))

        return rblur_gray

    def save_empty_scene(self):
        self.empty_scene = self.get_frame()

    def calc_scene_percent_change(self, img1, img2):
        diff_img = cv2.absdiff(img1, img2)
        img_shape = np.shape(diff_img)
        n_pixels = img_shape[0] * img_shape[1]
        return np.sum(diff_img) / n_pixels

    def wait_for_object(self):
        """ Waits until motion is detected then stops """
        start_frame = self.get_frame()
        nextframe_time = time.time() + (1 / cfg.check_video_fps)
        consecutive_diff_frames = 0

        # Wait for motion start
        while True:
            # Wait before capturing next frame
            while time.time() < nextframe_time:
                pass
            nextframe_time += (1 / cfg.check_video_fps)

            # Capture frame and compare to start frame
            next_frame = self.get_frame()
            change = self.calc_scene_percent_change(next_frame, start_frame)
            if cfg.DEBUG_MODE:
                print(change)

            if change > cfg.motion_start_min_percent:
                consecutive_diff_frames += 1
            else:
            	consecutive_diff_frames = 0

            if consecutive_diff_frames >= 2:
            	break

        last_frame = self.get_frame()
        consecutive_still_frames = 0

        # Wait for motion end
        while True:
            # Wait before capturing next frame
            while time.time() < nextframe_time:
                pass
            nextframe_time += (1 / cfg.check_video_fps)

            # Capture frame and compare to previous frame
            next_frame = self.get_frame()
            change = self.calc_scene_percent_change(next_frame, last_frame)
            last_frame = next_frame
            if change > cfg.motion_stop_max_percent:
                consecutive_still_frames = 0
            else:
                consecutive_still_frames += 1

            if cfg.DEBUG_MODE:
                print(consecutive_still_frames, change)

            if consecutive_still_frames >= (cfg.check_video_fps * cfg.motion_stop_time) - 1:
                break

    def find_first_move(self):
        start_frame = self.get_frame()
        nextframe_time = time.time() + (1 / cfg.check_video_fps)

        # Wait for motion start
        while True:
            # Wait before capturing next frame
            while time.time() < nextframe_time:
                pass
            nextframe_time += (1 / cfg.check_video_fps)

            # Capture frame and compare to start frame
            next_frame = self.get_frame()
            change = self.calc_scene_percent_change(next_frame, start_frame)
            if cfg.DEBUG_MODE:
                print(change)

            if change > cfg.motion_start_min_percent:
                break

        # Find and return where most x change has occured to chop 
        diff_img = cv2.absdiff(next_frame, start_frame)
        slice_sums = [sum(diff_img[:,k]) for k in range(len(diff_img))]
        (x, y) = cfg.turntable_center
        return (slice_sums.index(max(slice_sums)) - x) / cfg.pix_per_mm


    def locate_object(self):
        img = self.get_frame()
        diff_img = cv2.absdiff(self.empty_scene, img)
        _, thresh_img = cv2.threshold(diff_img, cfg.pixel_threshold, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_sorted = sorted(contours, key=cv2.contourArea, reverse=True)

        # Convert largest contour to bounding box
        largest_bbox = cv2.minAreaRect(contours_sorted[0])

        # Convert pixel space to mm
        (x, y) = cfg.turntable_center
        mult = 1 / cfg.pix_per_mm
        ((c_x, c_y), (w, h), r) = largest_bbox
        bbox_mm = ((c_x - x) * mult, (c_y - y) * mult, w * mult, h * mult, r * math.pi / 180)

        if cfg.DEBUG_MODE:
            self._save_image(diff_img, 'samich_diff_{}.jpg'.format(self.frame_n))
            self._save_image(thresh_img, 'samich_thresh_{}.jpg'.format(self.frame_n))

            print(contours_sorted)
            print('largest bbox: ', largest_bbox)

        if cfg.DEBUG_MODE:
            print(bbox_mm)

            # Save bbox area of image
            width = int(largest_bbox[1][0])
            height = int(largest_bbox[1][1])
            box = cv2.boxPoints(largest_bbox)
            box = np.int0(box)
            src_pts = box.astype("float32")
            dst_pts = np.array([[0, height-1], [0, 0], [width-1, 0], [width-1, height-1]], dtype="float32")

            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(img, M, (width, height))
            self._save_image(warped, 'samich_{}.jpg'.format(self.frame_n))
        
        return bbox_mm


    def find_face(self):
        frame = self.get_frame()
        faces = self.face_cascade.detectMultiScale(frame, 1.2, 6)

        tnow = time.time()
        if cfg.DEBUG_MODE:
            print("Face Detection - {} fps".format(1 / (tnow - self.tlast)))
            self.tlast = tnow

        if len(faces) > 0:
            [a, b, c, d] = faces[0]
            return (a, b, c, d)
        return None

    def is_reddit_there(self):
        method = cv2.TM_CCOEFF
        frame_edged = cv2.Canny(self.get_frame(), cfg.canny_min, cfg.canny_max)
        res = cv2.matchTemplate(frame_edged, self.reddit_template, method)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(res)
        if cfg.DEBUG_MODE:
            print(maxVal)
            # for pt in zip(*loc[::-1]):
            #     print(pt[0], pt[1])


        if maxVal > cfg.template_thresh:
            return True
        return False

    def show_frame(self, frame):
        (w,h) = self.resolution
        frame.shape = (h,w) # set the correct dimensions for the numpy array
        cv2.imshow("skrrt", frame)


if __name__=='__main__':
    c = Camera()
    c.start()
    try:
        print('Camera started')
        # while True:
        #     _ = c.get_frame()

        c.lock_on()
        print('Locked on')

        while True:
            h, w = c.get_location()
    
    finally:
        c.stop()
