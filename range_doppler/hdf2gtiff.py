from osgeo import gdal
import os
import zipfile
from zipfile import ZipFile
import glob


def findH5file(h5loc):
    # Search for HDF5 file in directory `h5loc`
    h5files_files = glob.glob(h5loc + "/**/*.h5", recursive = True)
    return h5files_files[0]


def findH5zip2(h5loc):
    # Search for HDF5 file in zip archive `h5loc`
    h5file = None
    with ZipFile(h5loc, 'r') as zip_ref:
        for info in zip_ref.infolist():
            if info.filename.endswith('.h5'):
                h5file = os.path.join(h5loc, info.filename)
                h5file = "/vsizip/{}".format(h5file.replace('\\', '/'))
                break
    return h5file

def findH5zip(h5loc):
    tmpdir = os.environ['TEMP']
    bname, ext = os.path.splitext(os.path.basename(h5loc))
    
    extdir = os.path.join(tmpdir, bname)
    
    with ZipFile(h5loc, 'r') as zip_ref:
        zip_ref.extractall(extdir)
    
    #if extracted_dir.endswith('.zip'):
    #    extracted_dir = extracted_dir[:-4]
    #zip_ref.extractall(extracted_dir)
    
    h5file = findH5file(extdir)
    h5file = h5file.replace('\\', '/')
    return h5file , extdir
    
def hdf2gtiff(h5loc):
    h5loc = h5loc.replace('\\', '/')
    if h5loc.endswith(".zip"):
        h5file , extdir  = findH5zip(h5loc)
    else:
        h5file = findH5file(h5loc)

    h5ds = gdal.Open(h5file)
    if h5ds == None:
        return None

    fstr = h5ds.GetSubDatasets()

    s_i = gdal.Open(fstr[2][0])
    s_q = gdal.Open(fstr[3][0])

    ## Output format
    opFormat = 'Gtiff'
    opExt = '.tiff'

    ## Write to TIFF file
    # dstfile = h5file + opExt
    tmpdir = os.environ['TEMP']
    pname = os.path.basename(h5file)
    dstfile = os.path.join(tmpdir, pname + opExt)
    driver = gdal.GetDriverByName(opFormat)

    # Get band information
    xSize = s_i.RasterXSize
    ySize = s_i.RasterYSize
    dType = s_i.GetRasterBand(1).DataType
    nBand = s_i.RasterCount + s_q.RasterCount

    ods = driver.Create(dstfile, xSize, ySize, nBand, dType)

    # Getting & Setting geotransform and projection information...
    geoTrans = h5ds.GetGeoTransform()
    ods.SetGeoTransform(geoTrans)

    wktProjection = h5ds.GetProjection() # Well-Known Text.
    ods.SetProjection(wktProjection)

    # Write band data to output dataset
    for i in range(1, s_i.RasterCount + 1):
        ib = s_i.GetRasterBand(i).ReadAsArray()
        ob = ods.GetRasterBand(i)
        ob.WriteArray(ib)

    offset = s_i.RasterCount
    for i in range(1, s_q.RasterCount + 1):
        ib = s_q.GetRasterBand(i).ReadAsArray()
        ob = ods.GetRasterBand(i + offset)
        ob.WriteArray(ib)

    del ods
    return dstfile , extdir
    