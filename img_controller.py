import numpy as np
import math
from scipy import ndimage

class img_controller:

    @staticmethod
    def img_straighten(img):
        img_binary = (img > 0).astype(np.uint8)
        # avoid that corner is right on the edge of image
        img_binary = np.pad(img_binary, pad_width=5, mode='constant', constant_values=0) 
        # harris corner detection or you can replace by any corner detection algo.
        corners = img_controller.harris_corner_detection(img_binary,max_corners=4)
        # find sortest edge to lay on x-axis
        edge_point1,edge_point2 = img_controller.find_sortest_edge(corners) 
        # calculate roation angle and rotate
        angle = img_controller.get_ratation_angle(edge_point1,edge_point2)
        img_rotated = img_controller.img_rotation(img, angle*180/math.pi)
        # remove zero edge
        return img_controller.img_crop(img_rotated)

    @staticmethod
    def harris_corner_detection(img, k=0.04, threshold=0.8, window_size=10, max_corners=4, sigma=1):
        # calculate first derivative
        img = img.astype(np.uint8)
        Ix = np.gradient(img)[1]
        Iy = np.gradient(img)[0]
        # calculate Hessian Matrix
        Ix2 = ndimage.filters.gaussian_filter(Ix**2, sigma=sigma)
        Iy2 = ndimage.filters.gaussian_filter(Iy**2, sigma=sigma)
        Ixy = ndimage.filters.gaussian_filter(Ix*Iy, sigma=sigma)
        det = Ix2*Iy2 - Ixy**2
        trace = Ix2 + Iy2
        R = det - k*trace**2
        # find corner coordinate with NMS
        corners = img_controller.NMS(R,threshold,window_size)
        # find Nth largest value
        corners = sorted(corners, key=lambda x: x[2], reverse=True)[:max_corners]
        for pt in corners: pt.pop() # remove Harris value
        return sorted(corners, key=lambda x: x[0])

    @staticmethod
    def NMS(R,threshold=0.8,window_size=10):
        corners = []
        for r, c in np.argwhere(R > threshold*R.max()):
            if r < window_size//2 or r >= R.shape[0]-window_size//2 \
               or c < window_size//2 or c >= R.shape[1]-window_size//2:
                continue
            window = R[r-window_size//2:r+window_size//2+1, c-window_size//2:c+window_size//2+1]
            if R[r,c] == window.max():
                corners.append([r, c, R[r,c]])
        return corners

    @staticmethod
    def find_sortest_edge(points):
        points = sorted(points, key=lambda x: x[1])
        # pick one point
        first_point = points.pop(0)
        # calculate distance with respect to other three points
        dis = [img_controller.distance(first_point,point) for point in points]
        return first_point, points[min(enumerate(dis), key=lambda x: x[1])[0]]

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    @staticmethod
    def get_ratation_angle(edge_point1, edge_point2):
        angle = math.atan2(edge_point2[0]-edge_point1[0],edge_point2[1]-edge_point1[1])
        if angle > math.pi/2:
            angle = math.pi-angle
        elif angle < -math.pi/2:
            angle = math.pi+angle
        return angle

    @staticmethod
    def img_rotation(image, angle):
        # Rotate image
        rotated_image = ndimage.rotate(image, angle, reshape=False, cval=0)
        return rotated_image

    @staticmethod
    def img_crop(image,box=''):
        if box:
            return image[box[2]:box[3], box[0]:box[1]]
        else:
            nonzero_pixels = np.nonzero(image)
            min_y = np.min(nonzero_pixels[0])
            min_x = np.min(nonzero_pixels[1])
            max_y = np.max(nonzero_pixels[0])
            max_x = np.max(nonzero_pixels[1])
            return image[min_y:max_y, min_x:max_x]