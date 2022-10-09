import cv2 as cv
import numpy as np




class Vision:

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None
    map_coords_start = (0, 0)
    map_coords_end = (0, 0)
    arr_places = []

    # constructor
    def __init__(self, needle_img_path, coords_start, coords_end, places, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method
        self.map_coords_start = coords_start
        self.map_coords_end = coords_end
        self.arr_places = places

    def map(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    def drawRect(self, haystack_img, criminals_recognized):
        for c in criminals_recognized:
            size = 15
            cv.rectangle(haystack_img, (int(c[0] - size/2), int(c[1] - size/2)), (int(c[0] + size/2), int(c[1] + size/2)), color=(255, 0, 255),
                     lineType=cv.LINE_4, thickness=1)
        #cv.imshow('Matches', haystack_img)

        # win32gui.SetWindowPos(win32gui.FindWindow(None, "Matches"), win32con.HWND_TOPMOST, 0, 0, 0, 0,
        #                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def find(self, haystack_img, threshold=0.5, debug_mode=None):
        # run the OpenCV algorithm
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)
        debug_mode = "kek"
        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        #print(locations)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        #print(rectangles)

        points = []
        if len(rectangles):
            #print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

           # cv.rectangle(haystack_img, (self.map_coords_start[0], self.map_coords_start[1]), (self.map_coords_end[0], self.map_coords_end[1]), color=(0, 0, 255),
           #              lineType=line_type, thickness=2)

            for p in self.arr_places:
                x1 = int(self.map(p.x - p.size/2, 0, 651, self.map_coords_start[0], self.map_coords_end[0]))
                y1 = int(self.map(p.y - p.size/2, 0, 651, self.map_coords_start[1], self.map_coords_end[1]))
                x2 = int(self.map(p.x + p.size/2, 0, 651, self.map_coords_start[0], self.map_coords_end[0]))
                y2 = int(self.map(p.y + p.size/2, 0, 651, self.map_coords_start[1], self.map_coords_end[1]))
                cv.rectangle(haystack_img, (x1, y1), (x2, y2), color=(0, 255, 255),
                             lineType=line_type, thickness=2)

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the points
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                                lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y),
                                color=marker_color, markerType=marker_type,
                                markerSize=40, thickness=2)

        if debug_mode:
            #cv.imshow('Matches', haystack_img)
            #cv.waitKey()
            #cv.imwrite('result_click_point.jpg', haystack_img)

            #win32gui.SetWindowPos(win32gui.FindWindow(None, "Matches"), win32con.HWND_TOPMOST, 0, 0, 0, 0,
            #                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            pass

        return points