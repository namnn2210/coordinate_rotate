import numpy as np
import xml.etree.ElementTree as ET
from scipy.ndimage import rotate
import cv2
import glob
import os
from pathlib import Path


def rot(image, im_rot, xy, angle):
    org_center = (np.array(image.shape[:2][::-1]) - 1) / 2.
    rot_center = (np.array(im_rot.shape[:2][::-1]) - 1) / 2.
    org = xy - org_center
    a = np.deg2rad(angle)
    new = np.array([org[0] * np.cos(a) + org[1] * np.sin(a),
                    -org[0] * np.sin(a) + org[1] * np.cos(a)])
    return new + rot_center


def ex_rotate(input, angle, limit):
    file_names = glob.glob(input + '/*.png')
    output_path = os.path.join(input, 'output_' + str(limit))
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    for i in range(limit):
        basename = Path(os.path.basename(file_names[i])).stem
        print(basename)
        try:
            data_orig = cv2.imread(file_names[i])
            im_rot = rotate(data_orig, angle)

            tree = ET.parse(os.path.join(input, f"{basename}.xml"))

            ann = tree.getroot()
            size = tree.find("size")
            objs = tree.findall('object')
            path = ann.find('path')

            size.find('width').text = str(im_rot.shape[1])
            size.find('height').text = str(im_rot.shape[0])
            ann.find("filename").text = f"{angle}_{basename}.png"
            path.text = 'img/' + f"{angle}_{basename}.png"

            for obj in objs:
                obj_bnd = obj.find('bndbox')
                obj_xmin = obj_bnd.find('xmin')
                obj_ymin = obj_bnd.find('ymin')
                obj_xmax = obj_bnd.find('xmax')
                obj_ymax = obj_bnd.find('ymax')
                xmin = float(obj_xmin.text)
                ymin = float(obj_ymin.text)
                xmax = float(obj_xmax.text)
                ymax = float(obj_ymax.text)

                xmin_1, ymin_1 = rot(data_orig, im_rot, np.array([xmin, ymin]), angle)
                xmax_2, ymax_2 = rot(data_orig, im_rot, np.array([xmax, ymax]), angle)
                print(xmin_1, ymin_1, xmax_2, ymax_2)
                obj_xmin.text = str(int(min(xmin_1, xmax_2)))
                obj_ymin.text = str(int(min(ymin_1, ymax_2)))
                obj_xmax.text = str(int(max(xmin_1, xmax_2)))
                obj_ymax.text = str(int(max(ymin_1, ymax_2)))

            cv2.imwrite(os.path.join(output_path, f"{angle}_{basename}.png"), im_rot)
            tree.write(os.path.join(output_path, f"{angle}_{basename}.xml"))
        except Exception as ex:
            print(ex)
    return True
