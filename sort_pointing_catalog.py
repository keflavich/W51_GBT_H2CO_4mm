import numpy as np
from astropy.io import ascii
from astropy.table import Table,Column
from astropy import coordinates

header = 'NAME      RA           DEC            S0.3 OFFSET Gold'.split()
t = ascii.read('4mm_gb/wband_pointing.cat', format='no_header', data_start=3)
t = Table([Column(data=t[data], name=name) for data,name in zip(t.columns, header)])
tblcoords = coordinates.SkyCoord(t['RA'], t['DEC'], frame='fk5', unit=('hour','deg'))

w51 = coordinates.SkyCoord.from_name('W51')
distance = w51.separation(tblcoords)
t.add_column(Column(name='Separation', data=distance))
t.sort('Separation')
t.pprint()
