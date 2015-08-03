import os
import numpy as np
from spectral_cube import SpectralCube
import paths
from astropy import units as u

files = [
'{region}_H2CO1-0_cube_bpoly5.fits',
'{region}_CH3CH213CN_cube_bpoly5.fits',
'{region}_EthyleneGlycol_cube_bpoly5.fits',
'{region}_H2CO5-5_cube_bpoly5.fits',
'{region}_HC3N8-7_cube_bpoly5.fits',
]

for region, vrange in (
                       ('W51', (30,80)),
                       ('W49', (-10,80)),
                       ('W51_ExtraFeed', (30,80)),
                       ('W49_ExtraFeed', (-10,80)),
                      ):
    h2cocube = SpectralCube.read(os.path.join(paths.projpath,
                                              files[0].format(region=region)))

    noise = h2cocube.spectral_slab(-200*u.km/u.s, 0*u.km/u.s).std(axis=0)

    h2coslab = h2cocube.spectral_slab(vrange[0]*u.km/u.s, vrange[1]*u.km/u.s)
    mask = h2coslab > 3*noise

    for fn in files:
        ffn = os.path.join(paths.projpath, fn)
        cube = SpectralCube.read(ffn.format(region=region))
        slab = cube.spectral_slab(vrange[0]*u.km/u.s, vrange[1]*u.km/u.s)

        m0 = slab.with_mask(mask).moment0(axis=0)
        m1 = slab.with_mask(mask).moment1(axis=0)
        m2 = slab.with_mask(mask).moment2(axis=0)
        mx = slab.with_mask(mask).max(axis=0)

        m0.hdu.writeto(os.path.join(paths.projpath,'mom0',
                                    fn.format(region=region).replace(".fits","_mom0.fits")),
                      clobber=True)
        m1.hdu.writeto(os.path.join(paths.projpath,'mom1',
                                    fn.format(region=region).replace(".fits","_mom1.fits")),
                      clobber=True)
        m2.hdu.writeto(os.path.join(paths.projpath,'mom2',
                                    fn.format(region=region).replace(".fits","_mom2.fits")),
                      clobber=True)
        mx.hdu.writeto(os.path.join(paths.projpath,'max',
                                    fn.format(region=region).replace(".fits","_max.fits")),
                      clobber=True)
