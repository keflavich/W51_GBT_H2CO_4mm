import os
from spectral_cube import SpectralCube
import astropy.io.fits as pyfits
from astropy.io import fits
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

log.setLevel(11)

line_table = Table.read(os.path.join(paths.spectra, 'bright_lines.ipac'),
                        format='ascii.ipac')

center = coordinates.SkyCoord('19:23:41.935   +14:30:47.49', unit=('hour','deg'))


for row in line_table:

    #files = ['/Volumes/passport/gbt/AGBT15A_446_02.raw.vegas/AGBT15A_446_02.raw.vegas.G.fits'
    #         ]
    files = ([os.path.join(paths.AGBT15A_446_2_path, fn) for fn in
              (#'15A_446_2_29to52_G1_0_F2.fits', bad baselines
               '15A_446_2_106to136_G1_0_F2.fits',
               '15A_446_2_62to92_G1_0_F2.fits',
               #'15A_446_2_29to52_G2_0_F2.fits', bad baselines
               '15A_446_2_106to136_G2_0_F2.fits',
               '15A_446_2_62to92_G2_0_F2.fits',
              ) ] +
             [os.path.join(paths.AGBT15A_446_3_path, fn) for fn in
              ('15A_446_3_27to57_G1_0_F2.fits',
               '15A_446_3_27to57_G2_0_F2.fits',
              )] +
             [os.path.join(paths.AGBT15A_446_4_path, fn) for fn in
              ('15A_446_4_27to57_G1_0_F2.fits',
               '15A_446_4_27to57_G2_0_F2.fits',
               '15A_446_4_75to89_G1_0_F2.fits',
               '15A_446_4_75to89_G2_0_F2.fits',
              )]
            )
    
    # Determine the extent of the 'main' maps
    crval2=[]
    crval3=[]
    for fn in files:
        d = fits.getdata(fn)
        ok = (d.OBJECT == 'W51M_IRS2') | (d.OBJECT == 'W51M_SE')
        crval2 += d.CRVAL2[ok].tolist()
        crval3 += d.CRVAL3[ok].tolist()
    crval2 = np.array(crval2)
    crval3 = np.array(crval3)
    xr = crval2.min(), crval2.max()
    yr = crval3.min(), crval3.max()
    pixsize=3#arcsec
    naxis1 = np.ceil((xr[1]-xr[0])*3600/pixsize*1.02)
    naxis2 = np.ceil((yr[1]-yr[0])*3600/pixsize*1.02)

    cubename='W51_{line}_cube'.format(line=row['Species'])
    sdpy.makecube.generate_header(np.mean(xr), np.mean(yr), coordsys='radec',
                                  naxis1=naxis1, naxis2=naxis2,
                                  pixsize=pixsize, naxis3=800, cd3=0.4,
                                  clobber=True, restfreq=row['Freq']*1e9)
    sdpy.makecube.make_blank_images(cubename,clobber=True)
    # old version:
    # sdpy.makecube.generate_header(center.ra.deg, center.dec.deg, coordsys='radec',
    #                          naxis1=40, naxis2=40, pixsize=3, naxis3=800, cd3=0.4,
    #                          clobber=True, restfreq=row['Freq']*1e9)
    # sdpy.makecube.make_blank_images(cubename,clobber=True)



    for fn in files:
        sdpy.makecube.add_file_to_cube(fn,
                                       cubename+'.fits',
                                       nhits=cubename+'_nhits.fits',
                                       add_with_kernel=True,
                                       kernel_fwhm=3./3600.,
                                       velocityrange=[-160,160],
                                       excludefitrange=[40*u.km/u.s,70*u.km/u.s],
                                       diagnostic_plot_name=fn.replace('.fits','_data_scrubbed.png'),
                                       coordsys='radec',
                                       progressbar=True,
                                       linefreq=row['Freq']*1e9,
                                       varweight=True,
                                      )
                                       #smoothto=0.5)

    # EXTENDED REGION

    files = ([os.path.join(paths.AGBT15A_446_2_path, fn) for fn in
              ('15A_446_2_29to52_C1_0_F1.fits',
               '15A_446_2_106to136_C1_0_F1.fits',
               '15A_446_2_62to92_C1_0_F1.fits',
               '15A_446_2_29to52_C2_0_F1.fits',
               '15A_446_2_106to136_C2_0_F1.fits',
               '15A_446_2_62to92_C2_0_F1.fits',
              ) ] +
             [os.path.join(paths.AGBT15A_446_3_path, fn) for fn in
              ('15A_446_3_27to57_C1_0_F1.fits',
               '15A_446_3_27to57_C2_0_F1.fits',
              )] + 
             [os.path.join(paths.AGBT15A_446_4_path, fn) for fn in
              ('15A_446_4_27to57_C1_0_F1.fits',
               '15A_446_4_27to57_C2_0_F1.fits',
               '15A_446_4_75to89_C1_0_F1.fits',
               '15A_446_4_75to89_C2_0_F1.fits',
              )]
            )

    # Determine the extent of the 'extra' maps
    crval2=[]
    crval3=[]
    for fn in files:
        d = fits.getdata(fn)
        ok = d.OBJECT == 'W51M_IRS2'
        crval2 += d.CRVAL2[ok].tolist()
        crval3 += d.CRVAL3[ok].tolist()
    crval2 = np.array(crval2)
    crval3 = np.array(crval3)
    xr = crval2.min(), crval2.max()
    yr = crval3.min(), crval3.max()
    pixsize=3#arcsec
    naxis1 = np.ceil((xr[1]-xr[0])*3600/pixsize*1.02)
    naxis2 = np.ceil((yr[1]-yr[0])*3600/pixsize*1.02)

    cubename='W51_ExtraFeed_{line}_cube'.format(line=row['Species'])
    sdpy.makecube.generate_header(np.mean(xr), np.mean(yr), coordsys='radec',
                                  naxis1=naxis1, naxis2=naxis2,
                                  pixsize=pixsize, naxis3=800, cd3=0.4,
                                  clobber=True, restfreq=row['Freq']*1e9)
    sdpy.makecube.make_blank_images(cubename,clobber=True)


    for fn in files:
        sdpy.makecube.add_file_to_cube(fn,
                                       cubename+'.fits',
                                       nhits=cubename+'_nhits.fits',
                                       add_with_kernel=True,
                                       kernel_fwhm=3./3600.,
                                       velocityrange=[-160,160],
                                       excludefitrange=[40*u.km/u.s,70*u.km/u.s],
                                       diagnostic_plot_name=fn.replace('.fits','_data_scrubbed.png'),
                                       coordsys='radec',
                                       progressbar=True,
                                       linefreq=row['Freq']*1e9,
                                       varweight=True,
                                      )

for row in line_table:
    for prefix in ("W51", "W51_ExtraFeed"):
        cubename='{prefix}_{line}_cube'.format(line=row['Species'], prefix=prefix)
        cube = SpectralCube.read(cubename+".fits")
        med = cube.median(axis=0)
        cubesub = cube-med*u.K
        mask = np.zeros(cubesub.shape, dtype='bool')
        mask[((cubesub.spectral_axis > 42*u.km/u.s) &
              (cubesub.spectral_axis < 70*u.km/u.s)),:,:] = True
        bcube = pyspeckit.cubes.baseline_cube(cubesub.filled_data[:], polyorder=5,
                                              cubemask=mask)
        f = fits.open(cubename+".fits")
        f[0].data = bcube
        f.writeto(cubename+"_bpoly5.fits", clobber=True)
