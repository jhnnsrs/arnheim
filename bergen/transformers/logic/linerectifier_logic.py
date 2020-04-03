import cv2
import numpy as np
import xarray as xr

def translateImageFromLine(image: xr.DataArray, line, scale) -> (np.array, list, list, list):
    ''' Translates the Image according to the Line and the Scale'''
    if "z" in image.dims:
        raise NotImplementedError("We cannot yet Rectififie in 3D")
    if "t" in image.dims:
        image = image.sel(t=0) # TODO: Maybe raise warning here
    if "c" not in image.dims:
        raise NotImplementedError("Please provide image with Channels")

    # Automatic using the first for transformation
    boxes, boxeswidths = getBoxesFromLine(line, scale)
    outimage, pixelwidths = straightenImageFromBoxes(image, boxes, scale)

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


def straightenImageFromBoxes(image: xr.DataArray, boxes, scale) ->(np.array, float):
    images = []
    widths = []
    _image = np.float64(image.compute())
    for box in boxes:
        partimage, pixelwidth = translateImageFromBox(_image,box,scale)
        images.append(partimage)
        widths.append(pixelwidth)


    total_height = scale * 2
    total_width = np.sum(widths)

    newshape = (total_height, total_width, image.c.size)
    straigtened_image = np.zeros(shape=newshape, dtype=np.float64)

    widthincrement = 0
    for index, nanaimage in enumerate(images):
        width = widths[index]
        straigtened_image[:total_height, widthincrement:widthincrement+width,:] = nanaimage.reshape((total_height, width, image.c.size))
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