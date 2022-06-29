

import numpy as np
from astropy.table import Table, Column, vstack
import astropy.units as u
from flare.LF.literature import UV





redshifts = np.array([13,12,11,10,9,8])


def name(nm):
    if nm[:5] == 'log10':
        return nm[5:]
    else:
        return nm




d, xname, xunit, yname, yunit = np.loadtxt('original_data/GSMF.tex').T, 'log10Mstar', 'dex(Msun)', 'log10phi', 'dex(Mpc^-3/dex)'
d, xname, xunit, yname, yunit = np.loadtxt('original_data/SFRDF.tex').T, 'log10SFR', 'dex(Msun/yr)', 'log10phi', 'dex(Mpc^-3/dex)'

print(d[2:])


tables = []


X = 0.5*(d[0]+d[1])
print(X)

for z, Y in zip(redshifts,d[2:]):
    print(z, Y)

    Y = np.round(Y, 2)
    s = ~np.isnan(Y)

    t = Table()

    t.add_column(Column(data = z*np.ones(np.sum(s)), name = 'z'))
    t.add_column(Column(data = X[s], name = xname, unit = xunit))
    t.add_column(Column(data = Y[s], name = yname, unit = yunit))
    tables.append(t)

table = vstack(tables)

table.meta['x'] = xname
table.meta['y'] = yname
table.meta['name'] = 'Bluetides'
table.meta['redshifts'] = list(set(table['z'].data))
table.meta['references'] = ['2016MNRAS.455.2778F', '2017MNRAS.469.2517W']


filename = f'../data/{name(xname)}_DF.ecsv'

table.write(filename, format = 'ascii.ecsv', overwrite=True)
table.write(f'/Users/stephenwilkins/Dropbox/Research/modules/flare_data/flags_data/data/DistributionFunctions/{name(xname)}/models/binned/bluetides.ecsv', overwrite = True)
