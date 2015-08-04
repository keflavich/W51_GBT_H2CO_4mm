import os
import numpy as np
import paths
from astroquery.splatalogue import Splatalogue, utils
from astropy import units as u
from astropy.table import Table
from astropy.io import ascii
import pyspeckit
import pylab as pl
import sys
sys.path.insert(0,'/Users/adam/work/w51/2014_wband_h2co/')
import constants

#lines = np.array([
#    [0.2149341106057569, 71.896161015668554, 0.0014511482007719477],
#    [0.22788574968934153, 73.066409138506103, 0.0021882332706945943],
#    [2.0162930696496608, 72.976486264338803, 0.00092203336511135548],
#    [0.29134384083210135, 72.961225426576917, 0.0015330159037659971],
#    [7.2803653494901308, 72.837950261968629, 0.00084101598640314598],
#    [4.511150570541635, 72.783605091668974, 0.00085822102355550081],
#    [1.8565196995180351, 72.757886093049166, 0.00099707046877037806],
#    [0.46678036176304516, 72.685388073309397, 0.00089497103883943475],
#    [0.48624798934652402, 72.680687220498157, 0.0013943731217438882],
#    [0.29866711440415428, 72.667119296077601, 0.0012183077784501117],
#    [0.74288601746400962, 72.414651262545263, 0.0012311701657571265],
#    [1.121774291166191, 72.408824913522508, 0.00096381348268900757],
#    [0.39541870191691986, 72.29987538627573, 0.0011069578799877031],
#    [0.18514198677346486, 72.108075998903203, 0.00076178329967597483],
#    [7.2785864710099135, 72.824466442169168, 0.00084061778089557855],
#])

def make_table(restfreqs):
    main_table = utils.minimize_table(Splatalogue.query_lines(constants.restfreq*(1-1/3e5)*u.Hz,
                                                              constants.restfreq*(1+1/3e5)*u.Hz,
                                                              show_nrao_recommended=True,
                                                              top20='top20'))
    main_table = Table(main_table,
                       names=('Species', 'ChemicalName', 'QNs', 'Freq', 'log10_Aij', 'EU_K'),
                       dtype=('S30', 'S30', 'S30', '<f8', '<f8', '<f8'))
    tables = []
    for freq in restfreqs:
        t = Splatalogue.query_lines(freq*(1-1/3e5)*u.GHz, freq*(1+1/3e5)*u.GHz)
        if len(t) > 0:
            utils.minimize_table(t).pprint()
        else:
            main_table.add_row(['Unknown','Unknown','Unknown',freq,0,0])
            continue
            print(freq)
            dv = 3
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
    return tbl


import os
import paths
import pyspeckit
import constants
#log.setLevel('DEBUG')

x,y = np.loadtxt(os.path.join(paths.root, 'orion_wband', 'table2.dat.gz')).T
sp_ori = pyspeckit.Spectrum(xarr=x*u.GHz* (1+8.8/3e5), data=y)
tbl4 = ascii.read(os.path.join(paths.root, 'orion_wband', 'table4.dat'))
xmol = tbl4['col1']/1e3 * (1+8.8/3e5)
mol = tbl4['col7']
                 

x,y = np.loadtxt(os.path.join(paths.root, 'spectra',
                              'W51_Feed1_scan72_session4'), skiprows=3).T
sp = pyspeckit.Spectrum(xarr=x*u.GHz, data=y)
sp.plotter(xmin=72.8, xmax=72.86)
sp.baseline(xmin=72.80*u.GHz, xmax=72.8577*u.GHz,
            exclude=[72.82, 72.8285], highlight_fitregion=True)
sp.specfit(guesses=[7.5147510594924318, 72.824387096774188, 0.0010958990971448343])
shift = sp.specfit.parinfo.SHIFT0.value

sp_rest = pyspeckit.Spectrum(xarr=(x+(constants.restfreq/1e9 - shift))*u.GHz, data=y)
sp_rest.plotter()

sp_rest.baseline(exclude=[0, 323, 5608, 394, 5397, 6360,
                          7158, 7698, 9953, 10376, 10893, 12701, 13077, 13782,
                          15496, 16384], xtype='pixel', highlight_fitregion=True,
                subtract=False, order=5)
guesses = [0.38275449060392736, 72.299933783072774, 0.0015505555871994407,
           0.959736586471446, 72.408962696167208, 0.00076874329827206038,
           0.57736860190897443, 72.414643092919221, 0.0010425993327333744,
           0.10925832536795378, 72.667112108348761, 0.00065447950402915296,
           0.35689149375761736, 72.685451542775724, 0.00043486332077850474,
           3.47373127848791, 72.783628405080634, 0.00082976167862874352,
           5.8393958460894622, 72.837950161208312, 0.00084478046981569411,
           1.6451193825490333, 72.976526359125216, 0.00092659699398358654,
           0.19000543390032168, 72.961564632805249, 0.001440868292119257,
           1.430905897761948, 72.757897214271239, 0.0009882621507225609,
           0.34999051170564027, 72.680951704416898, 0.00059676211957333314,
          ]
print(sp_rest.specfit.parinfo)
sp_rest.specfit(guesses=guesses, limited=[(True,True)]*len(guesses),
                limits=[(0.05,10), (72,73), (0.0001, 0.01)]*(len(guesses)/3),
                xmin=72.289, xmax=72.985)
sp_rest.plotter(xmin=72.29*u.GHz, xmax=73.0*u.GHz)
sp_rest.specfit.plot_fit(annotate=False)
sp_rest.plotter.savefig(os.path.join(paths.root, 'spectra',
                                     "W51_72GHz_fitted.png"))

tbl = make_table(sp_rest.specfit.parinfo.values[1::3])

sp_rest.plotter.line_ids(tbl['Species'], tbl['Freq']*u.GHz)
sp_rest.plotter.savefig(os.path.join(paths.root, 'spectra',
                                     "W51_LineIDs_72GHz.png"))
sp_rest.plotter.savefig(os.path.join(paths.root, 'spectra',
                                     "W51_LineIDs_72GHz.pdf"))

sp_rest.plotter(xmin=72.29*u.GHz, xmax=73.0*u.GHz)
sp_rest.specfit.plot_fit(annotate=False)
molok = (xmol > 72.29) & (xmol < 73.0)
sp_rest.plotter.line_ids(mol[molok], xmol[molok]*u.GHz)
sp_rest.plotter.savefig(os.path.join(paths.root, 'spectra',
                                     "W51_LineIDs_72GHz_Orion.pdf"))
sp_rest.plotter.savefig(os.path.join(paths.root, 'spectra',
                                     "W51_LineIDs_72GHz_Orion.png"))

sp_ori.plotter(xmin=72.29*u.GHz, xmax=73.0*u.GHz)
sp_ori.plotter.line_ids(mol[molok], xmol[molok]*u.GHz)
sp_ori.plotter.savefig(os.path.join(paths.root, 'spectra',
                                     "Orion_72GHz_LineIDs.png"))

x,y = np.loadtxt(os.path.join(paths.root, 'spectra', 'W49N_IF1_scan120'),
                 skiprows=3).T
spw49 = pyspeckit.Spectrum(xarr=x*u.GHz, data=y)
spw49.plotter(xmin=72.8,xmax=72.86)
spw49.baseline(xmin=72.80*u.GHz, xmax=72.8577, exclude=[72.8332, 72.8406], highlight_fitregion=True)
spw49.specfit(guesses=[7.5147510594924318, 72.836, 0.0010958990971448343])
shift = spw49.specfit.parinfo.SHIFT0.value

spw49_rest = pyspeckit.Spectrum(xarr=(x+(constants.restfreq/1e9 - shift))*u.GHz, data=y)
spw49_rest.plotter()
spw49_rest.plotter.line_ids(tbl['Species'], tbl['Freq']*u.GHz)
spw49_rest.plotter.savefig(os.path.join(paths.root, 'spectra',
                                        "W49N_LineIDs_72GHz.png"))

spectra_files = [
'W51_scan202_session2',
'W51_scan24_session2',
'W51_scan24_session4',
'W51_scan63_session3',
'W51_scan72_session4',
'W51_scan74_session3',
'W51_scan98_session2',
'W49N_scan120_session3',
'W49N_scan132_session3',
'W49N_scan76_session3',
]

for fn in spectra_files:
    ffn = os.path.join(paths.root, 'spectra', fn)

    x,y = np.loadtxt(ffn, skiprows=3).T
    sp = pyspeckit.Spectrum(xarr=x*u.GHz, data=y)

    sp.specname = fn
    sp.plotter(figure=pl.figure(1))
    sp.plotter.savefig(ffn+".png")
