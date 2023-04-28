import os
import numpy as np
from pydicom import dcmread
import matplotlib.pyplot as plt
from img_controller import img_controller

class data_loader(object):
    def __init__(self,file_path=''):
        if file_path:
            self.read(file_path)
        else:
            pass # wheather raise error or not

    def read(self,file_path):
        # extetion check
        if os.path.splitext(file_path)[-1] not in ['.dcm']:
            raise ValueError("Invalid file extension. Must be '.dcm'.")

        self.file_path = file_path
        self.dcm = dcmread(self.file_path)
        self.image = self.dcm.pixel_array.copy()
        # extend other attributes here

    def dcmwrite(self,output_path=''):
        os.makedirs(output_path, exist_ok=True)
        self.dcm.PixelData = self.image.tobytes()
        self.dcm.Rows, self.dcm.Columns = self.image.shape
        if output_path:
            self.dcm.save_as(os.path.join(output_path,os.path.split(self.file_path)[-1]))
        else:
            self.dcm.save_as(self.file_path)

    def img_straighten(self):
        self.image = img_controller.img_straighten(self.image)

    def img_rotation(self,angle):
        self.image = img_controller.img_rotation(self.image,angle)

    def img_crop(self,min_x,max_x,min_y,max_y):
        box = min_x,max_x,min_y,max_y
        self.image = img_controller.img_crop(self.image,box)

    def img_show(self):
        fig = plt.figure()
        fig.canvas.set_window_title(os.path.basename(self.file_path))
        plt.subplot(1,2,1)
        plt.title('Original image')
        plt.imshow(self.dcm.pixel_array,cmap='gray', vmin=self.dcm.pixel_array.min(), vmax=self.dcm.pixel_array.max())
        plt.axis('off')
        plt.subplot(1,2,2)
        plt.title('Processed image')
        plt.imshow(self.image,cmap='gray', vmin=self.image.min(), vmax=self.image.max())
        plt.axis('off')
        plt.show()