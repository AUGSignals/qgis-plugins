from osgeo import gdal
from os import path
from zipfile import ZipFile
import glob


def findH5file(h5loc):
    # Search for HDF5 file in directory `h5loc`
    h5files_files = glob.glob(h5loc + "/**/*.h5", recursive = True)
    return h5files_files[0]


def findH5zip(h5loc):
    # Search for HDF5 file in zip archive `h5loc`
    h5file = '..'
    with ZipFile(h5loc, 'r') as zip:
        for info in zip.infolist():
            if info.filename.endswith('.h5'):
                h5file = info.filename
                break
                
    return h5file
            
    
def hdf2gtiff(h5loc):
    
    if h5loc.endswith(".zip"):
        h5file = findH5zip(h5loc)
    else:
        h5file = findH5file(h5loc)
    
    ## Output format
    opFormat = 'Gtiff'
    opExt = '.tiff'

    h5ds = gdal.Open(h5file)
    fstr = h5ds.GetSubDatasets()

    s_i = gdal.Open(fstr[2][0])
    s_q = gdal.Open(fstr[3][0])

    # Write to TIFF file
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
    return dstfile
