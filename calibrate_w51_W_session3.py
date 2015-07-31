import os
import astropy.io.fits as pyfits
from sdpy import makecube,make_off_template,calibrate_map_scans
import numpy as np
from astropy import units as u
import paths
import constants

filename = paths.AGBT15A_446_3_fullpath
filepyfits = pyfits.open(filename,memmap=True)
datapfits = filepyfits[1].data
dataarr = datapfits.DATA


samplers = {
        0: ["G1_0","G2_0", ],
        }

feeds = {
        0: [2],
        }

gain_dict = calibrate_map_scans.compute_gains_highfreq(datapfits, feednum=2, sampler='G1_0')
gaintimes = np.array(gain_dict.keys())#, dtype=np.datetime64)
gains = np.array([v[0] for v in gain_dict.values()])
tsys = np.array([v[1] for v in gain_dict.values()])
gainsOK = gains > 0
gaintimes = gaintimes[gainsOK]
gains = gains[gainsOK]
gain = np.median(gains)
datapfits['TSYS'] = np.median(tsys[gainsOK])

#for obsmode,refscans,scanrange in zip(('DecLatMap','RALongMap','DecLatMap'),([9,54],[62,98],[108,140]),([9,54],[62,98],[108,140])):
for obsmode,refscans,scanrange,sourcename,mapname in zip(('RALongMap',
                                                          'DecLatMap',
                                                          'RALongMap'),
                                                         ([26,30,34,38,42,46,50,54,58],
                                                          [83,87,91,95,99,103,107,111,115],
                                                          [139,143,151,155,159,163,167,]),
                                                         ([27,57],
                                                          [84,114],
                                                          [140,166]),
                                                         ("W51M_IRS2","W49_Center","W49_Center"),
                                                         ("W51","W49","W49"),
                                                        ):

    s1,s2 = scanrange

    for ifnum in samplers:
        for sampler,feednum in zip(samplers[ifnum],feeds[ifnum]):

            savefile = os.path.join(paths.AGBT15A_446_3_path,
                                    "AGBT15A_446_03_{0}_fd{1}_if{2}_sr{3}-{4}"
                                    .format(sampler,feednum,ifnum,s1,s2))

            #if sampler in ('A1_0','A2_0'):
            #    off_template,off_template_in = make_off_template.make_off(filename, scanrange=scanrange,
            #            #exclude_velo=[-10,70], interp_vrange=[-150,250],
            #            interp_polyorder=10, sampler=sampler, return_uninterp=True,
            #            feednum=feednum,
            #            percentile=50,
            #            sourcename=sourcename,
            #            savefile=savefile,
            #            clobber=True,
            #            #debug=True,
            #            linefreq=constants.restfreq, # needed to get velo right...
            #            extension=1, exclude_spectral_ends=10)

            outfn = paths.AGBT15A_446_3_path+'15A_446_3_%ito%i_%s_F%i.fits' % (s1,s2,sampler,feednum)
            calibrate_map_scans.calibrate_cube_data(filename,
                                                    outfn,
                                                    scanrange=scanrange,
                                                    #min_scale_reference=10,
                                                    feednum=feednum,
                                                    refscans=refscans,
                                                    sampler=sampler,
                                                    filepyfits=filepyfits,
                                                    datapfits=datapfits,
                                                    # ignored b/c gain tau=0.50,
                                                    tsys=np.median(tsys[gainsOK]),
                                                    gain=gain_dict,
                                                    dataarr=dataarr,
                                                    obsmode=obsmode,
                                                    sourcename=sourcename,
                                                    highfreq=True,
                                                   )
                                                    #off_template=off_template)


