#!/usr/bin/python
# Warp all *.png to *.tif from RD to WGS84
import subprocess
import os
import sys
import shutil

print 'argv1: dir, argv2: pgw_template (copies over all the existing)'
dirtocheck = sys.argv[1]
pgw_template = None
try:
    pgw_template = sys.argv[2]
    print 'pgw template: %s' % pgw_template
except:
    print 'no pgw template'
print 'dir: %s' % dirtocheck

for root, dirs, files in os.walk(dirtocheck):
    if pgw_template:
        for f in files:
            if f.endswith('.pgw'):
                fullpath = os.path.join(root, f)
                print 'copying pgw template %s -> %s...' % (pgw_template, f)
                shutil.copyfile(pgw_template, fullpath)

    for f in files:
        if not f.endswith('.png'):
            continue
        fullpath = os.path.join(root, f)
        filename_in = fullpath
        try:
            os.makedirs(root+'_warped')
        except:
            pass
        try:
            os.makedirs(root+'_png')
        except:
            pass
        fullpath_dest = os.path.join(root+'_warped', f)
        filename_out = fullpath_dest.replace('.png', '.tif')

        print '%s -> %s' % (filename_in, filename_out)
        subprocess.call([
                'gdalwarp', 
                filename_in,
                filename_out,
                '-t_srs',
                "+proj=latlong +datum=WGS83",
                '-s_srs',
                "+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.999908 +x_0=155000 +y_0=463000 +ellps=bessel +towgs84=565.237,50.0087,465.658,-0.406857,0.350733,-1.87035,4.0812 +units=m +no_defs"])

        filename_out2 = os.path.join(root+'_png', f).replace('.tif', '.png')

        subprocess.call([
                'convert', 
                filename_out,
                filename_out2,])
