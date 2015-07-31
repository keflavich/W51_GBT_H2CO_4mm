import os
import astropy.io.fits as pyfits
import itertools
import sys
import sdpy
#sys.path.append('/Users/adam/repos/casaradio/branches/python/ginsburg/')
#from gbtpy import makecube,make_off_template,calibrate_map_scans
import numpy as np
np.seterr(all='ignore')
from astropy import coordinates
from astropy import log
from astropy.table import Table
from astropy import units as u
import constants
import paths
import pyspeckit

line_table = Table.read(os.path.join(paths.spectra, 'bright_lines.ipac'),
                        format='ascii.ipac')

center = coordinates.SkyCoord('19:23:41.935   +14:30:47.49', unit=('hour','deg'))


for row in line_table:
    cubename='W51_{line}_cube'.format(line=row['Species'])
    # 1.5 x 1.5 '
    sdpy.makecube.generate_header(center.ra.deg, center.dec.deg, coordsys='radec',
                             naxis1=40, naxis2=40, pixsize=3, naxis3=800, cd3=0.4,
                             clobber=True, restfreq=row['Freq']*1e9)
    sdpy.makecube.make_blank_images(cubename,clobber=True)

    #files = ['/Volumes/passport/gbt/AGBT15A_446_02.raw.vegas/AGBT15A_446_02.raw.vegas.G.fits'
    #         ]
    files = [
        '15A_446_2_29to52_G1_0_F2.fits',
        '15A_446_2_106to136_G1_0_F2.fits',
        '15A_446_2_62to92_G1_0_F2.fits',
    ]

    log.setLevel(11)

    for fn in files:
        sdpy.makecube.add_file_to_cube(os.path.join(paths.AGBT15A_446_2_path, fn),
                                       cubename+'.fits',
                                       nhits=cubename+'_nhits.fits',
                                       add_with_kernel=True,
                                       kernel_fwhm=3./3600.,
                                       velocityrange=[-160,160],
                                       excludefitrange=[40,70],
                                       diagnostic_plot_name=fn.replace('.fits','_data_scrubbed.png'),
                                       coordsys='radec',
                                       progressbar=True,
                                       linefreq=row['Freq']*1e9,
                                      )
                                       #smoothto=0.5)

for row in line_table:
    cubename='W51_{line}_cube'.format(line=row['Species'])
    cube = SpectralCube.read(cubename+".fits")
    med = cube.median(axis=0)
    cubesub = cube-med*u.K
    mask = np.zeros(cubesub.shape, dtype='bool')
    mask[((cubesub.spectral_axis > 35*u.km/u.s) &
          (cubesub.spectral_axis < 60*u.km/u.s)),:,:] = True
    bcube = pyspeckit.cubes.baseline_cube(cubesub.filled_data[:], polyorder=5,
                                          cubemask=mask)
    f = fits.open(cubename+".fits")
    f[0].data = bcube
    f.writeto(cubename+"_bpoly5.fits")

#import os
#
#makecube.make_flats(cubename,vrange=[-20,60],noisevrange=[250,300])
#
#
#sampler_feeds = {'A10': 1,
#                 'A13': 1,
#                 'A14': 1,
#                 'A9': 1,
#                 'B17': 1,
#                 'B18': 1,
#                 'B21': 1,
#                 'B22': 1,
#                 'C25': 2,
#                 'C26': 2,
#                 'C29': 2,
#                 'C30': 2,
#                 'D33': 2,
#                 'D34': 2,
#                 'D37': 2,
#                 'D38': 2}
#
#for cubename,restfreq,samplers in (
#        #('LimaBean_H113a_cube', 4.497776e9, ('D34','D38')),
#        #('LimaBean_H110a_cube', 4.874157e9, ('D33','D37')),
#        ('LimaBean_H213CO22_cube', 13.7788, ["B17","B21","D33","D37"]),
#        ('LimaBean_H2C18O22_cube', 13.16596, ["B18","B22","D34","D38"]),
#        #('LimaBean_H109a_cube', 5.008922e9, ('B18','B22')),
#        #('LimaBean_H112a_cube', 4.61879e9, ('C26','C30')),
#        #('LimaBean_OHF44_cube', 5.52344e9, ('A10','A14')),
#        #('LimaBean_CH3NH2_cube', 5.19543e9, ('B21','B17'))
#            ):
#
#    makecube.generate_header(0.256, 0.0220, naxis1=100, naxis2=100, pixsize=15,
#            naxis3=800, cd3=1.0, clobber=True, restfreq=restfreq)
#    makecube.make_blank_images(cubename,clobber=True)
#
#    files = [x for scan1,scan2 in ([9,54],[62,98],[108,140]) for x in
#             ['/Users/adam/observations/gbt/LimaBeanmap/14A_110_%ito%i_%s_F%i.fits' % (scan1,scan2,samplers[ii],sampler_feeds[samplers[ii]])
#              for ii in xrange(len(samplers))]]
#    for fn in files:
#        makecube.add_file_to_cube(fn,
#            cubename+'.fits',nhits=cubename+'_nhits.fits',wcstype='V',
#            add_with_kernel=True,
#            kernel_fwhm=20./3600.,
#            velocityrange=[-400,400],excludefitrange=[-150,225],
#            smoothto=2)
#
#    os.system('chmod +x %s_starlink.sh' % cubename)
#    os.system('./%s_starlink.sh' % cubename)
#    makecube.make_flats(cubename,vrange=[-20,60],noisevrange=[250,300])
#
#
##import FITS_tools
#import FITS_tools.cube_regrid
#from astropy.io import fits
#from agpy.cubes import smooth_cube
#
#for cubename in ('LimaBean_H2CO22_cube', 'LimaBean_H213CO22_cube', 'LimaBean_H2C18O22_cube'):
#
#    cube = fits.open(cubename+"_sub.fits")
#    # kernel = ((2.5*60)**2 -  50.**2)**0.5 / sqrt(8*log(2)) = 60 arcsec
#    # 60 arcsec / 15 "/pixel = 4
#    cubesm2 = FITS_tools.cube_regrid.gsmooth_cube(cube[0].data, [5,4,4], use_fft=True, psf_pad=False, fft_pad=False)
#    cubesm = smooth_cube(cube[0].data, kernelwidth=4, interpolate_nan=True)
#    cube[0].data = cubesm
#    cube.writeto(cubename+"_sub_smoothtoCband.fits",clobber=True)
#    cube[0].data = cubesm2
#    cube.writeto(cubename+"_sub_smoothtoCband_vsmooth.fits",clobber=True)
#
#    #makecube.make_taucube(cubename,cubename+"_continuum.fits",etamb=0.886)
#    #makecube.make_taucube(cubename,cubename+"_continuum.fits",etamb=0.886, suffix="_sub_smoothtoCband.fits")
#    # -0.4 is the most negative point in the continuum map...
#    makecube.make_taucube(cubename,
#                          cubename+"_continuum.fits",
#                          etamb=0.886,
#                          suffix="_sub_smoothtoCband_vsmooth.fits",
#                          outsuffix="_smoothtoCband_vsmooth.fits",
#                          TCMB=2.7315+0.4)
#
#    makecube.make_taucube(cubename,
#                          cubename+"_continuum.fits",
#                          etamb=0.886,
#                          suffix="_sub_smoothtoCband.fits",
#                          outsuffix="_smoothtoCband.fits",
#                          TCMB=2.7315+0.4)
#
#    makecube.make_taucube(cubename,
#                          cubename+"_continuum.fits",
#                          etamb=0.886,
#                          suffix="_sub.fits",
#                          outsuffix=".fits",
#                          TCMB=2.7315+0.4)
#
