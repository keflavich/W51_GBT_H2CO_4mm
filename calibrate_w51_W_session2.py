import os
import astropy.io.fits as pyfits
from sdpy import makecube,make_off_template,calibrate_map_scans
import numpy as np
from astropy import units as u
import paths
import constants

sourcename = "W51M_IRS2"
mapname = 'W51'

sampler_letter = {0: 'G',
                  1: 'C'}

samplers = {
        0: ["G1_0","G2_0", ],
        1: ["C1_0","C2_0", ],
        }

feeds = {
        0: [2],
        1: [1],
        }


for ifnum in samplers:
    for sampler,feednum in zip(samplers[ifnum],feeds[ifnum]):


        filename = paths.AGBT15A_446_2_fullpath.format(sampler_letter[ifnum])
        filepyfits = pyfits.open(filename,memmap=True)
        datapfits = filepyfits[1].data
        dataarr = datapfits.DATA

        gain_dict = calibrate_map_scans.compute_gains_highfreq(datapfits,
                                                               feednum=feednum,
                                                               sampler=sampler)
        gain_dict = {k:v for k,v in gain_dict.iteritems() if v[1] > 0}
        gaintimes = np.array(gain_dict.keys())
        gains = np.array([v[0] for v in gain_dict.values()])
        tsys = np.array([v[1] for v in gain_dict.values()])
        gainsOK = gains > 0
        gaintimes = gaintimes[gainsOK]
        gains = gains[gainsOK]
        gain = np.median(gains)
        datapfits['TSYS'] = np.median(tsys[gainsOK])


        #for obsmode,refscans,scanrange in zip(('DecLatMap','RALongMap','DecLatMap'),([9,54],[62,98],[108,140]),([9,54],[62,98],[108,140])):
        for obsmode,refscans,scanrange in zip(('DecLatMap',
                                               'DecLatMap',
                                               'RALongMap'),
                                              ([29,52],
                                               [105, 109, 113, 117, 121, 125, 129, 133],
                                               [61, 65, 69, 73, 77, 81, 85, 89,]),
                                              ([29,52],
                                               [106,136],
                                               [62,92])
                                              ):

            s1,s2 = scanrange

            savefile = os.path.join(paths.AGBT15A_446_2_path,
                                    "AGBT15A_446_02_{0}_fd{1}_if{2}_sr{3}-{4}"
                                    .format(sampler,feednum,ifnum,s1,s2))
            log.info(savefile)

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

            outfn = paths.AGBT15A_446_2_path+'15A_446_2_%ito%i_%s_F%i.fits' % (s1,s2,sampler,feednum)
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


