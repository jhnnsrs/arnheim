import logging

import cv2
import numpy as np


def translateImageFromLine(image, line, scale) -> (np.array, list, list, list):
    ''' Translates the Image according to the Line and the Scale'''
    if len(image.shape) == 2:
        print(" X,Y ")
        newimage = image[:,:]
    elif len(image.shape) == 3:
        print(" X,Y C Image")
        newimage = image[:,:,:]
    elif len(image.shape) == 4:
        print(" X,Y C, Z Image")
        newimage = image[:,:,:,0]
    elif len(image.shape) == 5:
        print(" X,Y C, Z, T Image")
        newimage = image[:,:,:,0,0]
    else:
        print("ERROR FROM REP")
        newimage = np.zeros((1025,1025,3))

    # Automatic using the first for transformation
    boxes, boxeswidths = getBoxesFromLine(line,scale)
    outimage, pixelwidths = straightenImageFromBoxes(newimage,boxes,scale)

    return outimage, boxeswidths, pixelwidths, boxes


def getScaledOrtho(vertices, scale):
    '''Gets the 2D Orthogonal do the vertices provided'''
    perp = np.empty_like(vertices)
    perp[0] = -vertices[1]
    perp[1] = vertices[0]

    perpnorm = perp / np.linalg.norm(perp)
    perpscaled = perpnorm * scale
    return perpscaled

def getBoxesFromLine(line, scale):
    '''Index 0 Box is between 0 and 1 Vector'''
    line = np.array(line)
    boxes = []
    boxeswidths = []
    for pos in range(len(line)-1):
        a = line[pos]
        b = line[pos+1]

        if a[0] != b[0] or a[1] != b[1]:
            perpnew = getScaledOrtho(a - b, scale=scale)

            c1 = a + perpnew
            c2 = a - perpnew
            c3 = b - perpnew
            c4 = b + perpnew
            width = np.linalg.norm(a - b)
            verts = [c1, c2, c3, c4]

            boxes.append(verts)
            boxeswidths.append(width)

    return boxes,boxeswidths


def straightenImageFromBoxes(image, boxes, scale) ->(np.array, float):
    images = []
    widths = []
    for box in boxes:
        partimage, pixelwidth = translateImageFromBox(image,box,scale)
        images.append(partimage)
        widths.append(pixelwidth)


    total_height = scale * 2
    total_width = np.sum(widths)
    if len(image.shape) > 2:
        total_channels = image.shape[2]
        if total_channels == 1:
            straigtened_image = np.zeros(shape=(total_height, total_width), dtype=np.float64)
        else:
            print("Straightened Multichannelimage has shape {0},".format(str(image.shape)))
            straigtened_image = np.zeros(shape=(total_height, total_width, total_channels), dtype=np.float64)
    else:
        print("Straightened SingleChannelImage has shape ({0},{1})".format(total_height, total_width))
        straigtened_image = np.zeros(shape=(total_height, total_width), dtype=np.float64)

    widthincrement = 0
    for index, nanaimage in enumerate(images):
        width = widths[index]
        straigtened_image[:total_height, widthincrement:widthincrement+width] = nanaimage
        widthincrement += width

    print("Straightened Image has shape of {0}".format(straigtened_image.shape))
    return straigtened_image, widthincrement





def translateImageFromBox(image, box, scale) -> (np.array, int):
    height = scale * 2
    width = np.linalg.norm(box[1] - box[2])

    pts1 = np.float32(box)
    pts2 = np.float32([[0, height], [0, 0], [width, 0], [width, height]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    pixelwidth = int(round(width))
    dst = cv2.warpPerspective(image, M, (pixelwidth, int(height)))

    return dst, pixelwidth