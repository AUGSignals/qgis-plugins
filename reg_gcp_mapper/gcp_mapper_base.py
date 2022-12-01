from osgeo import gdal
import numpy as np
import cv2

def quantize(img):
    m = np.amin(img)
    M = np.amax(img)
    tmp = 0.5 + 255.0 * (img - m) / (M - m)
    img = tmp.astype('uint8')
    return img

def loadimage(path, band_index=1):
    raster = gdal.Open(path) # GDAL Dataset
    band = raster.GetRasterBand(band_index) # GDAL Band
    data = band.ReadAsArray() # numpy.ndarray
    data = quantize(data)
    return data

def getDMatch(count):
    good = []
    for i in range(count):
        temp_dmatch = cv2.DMatch(i,i,0,0)
        good.append(temp_dmatch)
    return good

def array2keypoints(kplist):
    keypoints = []
    marker_diameter = 10
    nrows, ncols = kplist.shape
    for i in range(nrows):
        # x,y = kplist[i,:] # untested
        # keypoints.append(cv2.KeyPoint(y, x, marker_diameter)) # untested
        keypoints.append(cv2.KeyPoint(kplist[i,1], kplist[i,0], marker_diameter))
    return keypoints

def mapgcp(infile_left, gcpfile, outfile, infile_right, band_right=1, band_left=1):
    img_ref = loadimage(infile_left, band_left)
    img_warp = loadimage(infile_right, band_right)
    kplist = np.loadtxt(gcpfile, dtype=float, delimiter=',', skiprows=1)
    nrows, ncols = kplist.shape
    assert nrows > 0
    assert ncols == 4
    kp_ref = array2keypoints(kplist[:,[0,1]]) 
    kp_warp =array2keypoints(kplist[:,[2,3]])
    good = getDMatch(nrows)
    img_map = cv2.drawMatches(img_ref, kp_ref, img_warp, kp_warp, good, None, flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    """
    if cv2.imwrite(outfilename, img_map):
        print('Output file is saved at: ' + outfilename)
    else:
        print('Error while saving the output file ' + outfilename)
    """
    return cv2.imwrite(outfile, img_map)