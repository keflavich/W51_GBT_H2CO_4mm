import numpy as np
import paths
from astroquery.splatalogue import Splatalogue, utils
from astropy import units as u
from astropy.table import Table
import pyspeckit
import sys
sys.path.insert(0,'/Users/adam/work/w51/2014_wband_h2co/')
import constants

lines = np.array([
    [0.2149341106057569, 71.896161015668554, 0.0014511482007719477],
    [0.22788574968934153, 73.066409138506103, 0.0021882332706945943],
    [2.0162930696496608, 72.976486264338803, 0.00092203336511135548],
    [0.29134384083210135, 72.961225426576917, 0.0015330159037659971],
    [7.2803653494901308, 72.837950261968629, 0.00084101598640314598],
    [4.511150570541635, 72.783605091668974, 0.00085822102355550081],
    [1.8565196995180351, 72.757886093049166, 0.00099707046877037806],
    [0.46678036176304516, 72.685388073309397, 0.00089497103883943475],
    [0.48624798934652402, 72.680687220498157, 0.0013943731217438882],
    [0.29866711440415428, 72.667119296077601, 0.0012183077784501117],
    [0.74288601746400962, 72.414651262545263, 0.0012311701657571265],
    [1.121774291166191, 72.408824913522508, 0.00096381348268900757],
    [0.39541870191691986, 72.29987538627573, 0.0011069578799877031],
    [0.18514198677346486, 72.108075998903203, 0.00076178329967597483],
    [7.2785864710099135, 72.824466442169168, 0.00084061778089557855],
])

main_table = utils.minimize_table(Splatalogue.query_lines(constants.restfreq*(1-1/3e5)*u.Hz,
                                                          constants.restfreq*(1+1/3e5)*u.Hz,
                                                          show_nrao_recommended=True,
                                                          top20='top20'))
main_table = Table(main_table,
                   names=('Species', 'ChemicalName', 'QNs', 'Freq', 'log10_Aij', 'EU_K'),
                   dtype=('S30', 'S30', 'S30', '<f8', '<f8', '<f8'))
tables = []
for freq in lines[:,1]:
    t = Splatalogue.query_lines(freq*(1-1/3e5)*u.GHz, freq*(1+1/3e5)*u.GHz)
    if len(t) > 0:
        utils.minimize_table(t).pprint()
    else:
        main_table.add_row(['Unknown','Unknown','Unknown',freq,0,0])
        continue
        print(freq)
        dv = 1
        while len(t) == 0:
            dv = dv + 1
            print(dv)
            t = Splatalogue.query_lines(freq*(1-dv/3e5)*u.GHz, freq*(1+dv/3e5)*u.GHz)
        utils.minimize_table(t).pprint()
    tables.append(utils.minimize_table(t))

tbl = main_table
for t in tables:
    for row in t:
        tbl.add_row(row)


x,y = np.loadtxt(os.path.join(paths.rootpath, 'spectra',
                              'W51_Feed1_scan72_session4'), skiprows=3).T
sp = pyspeckit.Spectrum(xarr=x*u.GHz, data=y)
sp.plotter(xmin=72.8,xmax=72.86)
sp.baseline(xmin=72.80*u.GHz, xmax=72.8577, exclude=[72.82, 72.8285], highlight_fitregion=True)
sp.specfit(guesses=[7.5147510594924318, 72.824387096774188, 0.0010958990971448343])
shift = sp.specfit.parinfo.SHIFT0.value

sp_rest = pyspeckit.Spectrum(xarr=(x+(constants.restfreq/1e9 - shift))*u.GHz, data=y)
sp_rest.plotter()
sp_rest.plotter.line_ids(tbl['Species'], tbl['Freq']*u.GHz)
sp_rest.plotter.savefig(os.path.join(paths.rootpath, 'spectra',
                                     "W51_LineIDs_72GHz.png"))

x,y = np.loadtxt(os.path.join(paths.rootpath, 'spectra', 'W49N_IF1_scan120'),
                 skiprows=3).T
spw49 = pyspeckit.Spectrum(xarr=x*u.GHz, data=y)
spw49.plotter(xmin=72.8,xmax=72.86)
spw49.baseline(xmin=72.80*u.GHz, xmax=72.8577, exclude=[72.8332, 72.8406], highlight_fitregion=True)
spw49.specfit(guesses=[7.5147510594924318, 72.836, 0.0010958990971448343])
shift = spw49.specfit.parinfo.SHIFT0.value

spw49_rest = pyspeckit.Spectrum(xarr=(x+(constants.restfreq/1e9 - shift))*u.GHz, data=y)
spw49_rest.plotter()
spw49_rest.plotter.line_ids(tbl['Species'], tbl['Freq']*u.GHz)
spw49_rest.plotter.savefig(os.path.join(paths.rootpath, 'spectra',
                                        "W49N_LineIDs_72GHz.png"))


#In [76]: sp_rest.specfit.parinfo
#Out[76]:
#[Param #0   AMPLITUDE0 =     0.227886 +/-       0.0147992 ,
# Param #1       SHIFT0 =      73.0664 +/-     0.000164093 ,
# Param #2       WIDTH0 =   0.00218823 +/-     0.000164093   Range:   [0,inf)]
#
#
# In [89]: sp_rest.specfit.parinfo
#Out[89]:
#[Param #0   AMPLITUDE0 =      2.01629 +/-       0.0232214 ,
# Param #1       SHIFT0 =      72.9765 +/-     1.22617e-05 ,
# Param #2       WIDTH0 =  0.000922033 +/-     1.22617e-05   Range:   [0,inf)]
#
#
# In [94]: sp_rest.specfit.parinfo
#Out[94]:
#[Param #0   AMPLITUDE0 =     0.291344 +/-       0.0173444 ,
# Param #1       SHIFT0 =      72.9612 +/-     0.000105383 ,
# Param #2       WIDTH0 =   0.00153302 +/-     0.000105383   Range:   [0,inf)]
#
#
# sp_rest.specfit.parinfo
#Out[96]:
#[Param #0   AMPLITUDE0 =      7.28037 +/-       0.0216984 ,
# Param #1       SHIFT0 =       72.838 +/-     2.89434e-06 ,
# Param #2       WIDTH0 =  0.000841016 +/-     2.89434e-06   Range:   [0,inf)]
#
#
# In [98]: sp_rest.specfit.parinfo
#Out[98]:
#[Param #0   AMPLITUDE0 =      4.51115 +/-       0.0350352 ,
# Param #1       SHIFT0 =      72.7836 +/-     7.69639e-06 ,
# Param #2       WIDTH0 =  0.000858221 +/-     7.69639e-06   Range:   [0,inf)]
#
#
#
# Out[100]:
#[Param #0   AMPLITUDE0 =      1.85652 +/-       0.0442006 ,
# Param #1       SHIFT0 =      72.7579 +/-     2.74109e-05 ,
# Param #2       WIDTH0 =   0.00099707 +/-     2.74108e-05   Range:   [0,inf)]
#
#
#
# sp_rest.specfit.parinfo
#Out[102]:
#[Param #0   AMPLITUDE0 =      0.46678 +/-       0.0346399 ,
# Param #1       SHIFT0 =      72.6854 +/-     7.66487e-05 ,
# Param #2       WIDTH0 =  0.000894971 +/-     7.69117e-05   Range:   [0,inf)]
#
#
#
# In [104]: sp_rest.specfit.parinfo
#Out[104]:
#[Param #0   AMPLITUDE0 =     0.486248 +/-       0.0216138 ,
# Param #1       SHIFT0 =      72.6807 +/-     7.17535e-05 ,
# Param #2       WIDTH0 =   0.00139437 +/-     7.47794e-05   Range:   [0,inf)]
#
# sp_rest.specfit.parinfo
#Out[106]:
#[Param #0   AMPLITUDE0 =     0.298667 +/-       0.0234146 ,
# Param #1       SHIFT0 =      72.6671 +/-     0.000110286 ,
# Param #2       WIDTH0 =   0.00121831 +/-     0.000110286   Range:   [0,inf)]
#
#
#
# In [108]: sp_rest.specfit.parinfo
#Out[108]:
#[Param #0   AMPLITUDE0 =     0.742886 +/-       0.0640006 ,
# Param #1       SHIFT0 =      72.4147 +/-     0.000122437 ,
# Param #2       WIDTH0 =   0.00123117 +/-     0.000122685   Range:   [0,inf)]
#
#
#In [110]: sp_rest.specfit.parinfo
#Out[110]:
#[Param #0   AMPLITUDE0 =      1.12177 +/-       0.0251667 ,
# Param #1       SHIFT0 =      72.4088 +/-     2.49676e-05 ,
# Param #2       WIDTH0 =  0.000963813 +/-     2.49692e-05   Range:   [0,inf)]
#
# 
#In [112]: sp_rest.specfit.parinfo
#Out[112]:
#[Param #0   AMPLITUDE0 =     0.395419 +/-       0.0213164 ,
# Param #1       SHIFT0 =      72.2999 +/-     6.89063e-05 ,
# Param #2       WIDTH0 =   0.00110696 +/-     6.89063e-05   Range:   [0,inf)]
#
# 
# In [114]: sp_rest.specfit.parinfo
#Out[114]:
#[Param #0   AMPLITUDE0 =     0.185142 +/-        0.023971 ,
# Param #1       SHIFT0 =      72.1081 +/-      0.00011389 ,
# Param #2       WIDTH0 =  0.000761783 +/-      0.00011389   Range:   [0,inf)]
#
