

import numpy as np
from astropy.table import Table, Column, vstack
import astropy.units as u
from flare.LF.literature import UV





X = np.array([8.125,  8.325, 8.625,  8.825,  9.125,  9.325,  9.625,  9.825, 10.125])


def name(nm):
    if nm[:5] == 'log10':
        return nm[5:]
    else:
        return nm




d, xname, yname, unit, conversion = np.loadtxt('original_data/sSFR.tex'), 'log10Mstar', 'log10sSFR', 'dex(Gyr^-1)', 9
# d, xname, yname, unit, conversion = np.loadtxt('original_data/age.tex'), 'log10Mstar', 'age', 'Myr', 0
# d, xname, yname, unit, conversion = np.loadtxt('original_data/Zstar.tex'), 'log10Mstar', 'log10Zstar', 'dex', 0
# d, xname, yname, unit, conversion = np.loadtxt('original_data/Zgas_young.tex'), 'log10Mstar', 'log10Zgas_young', 'dex', 0

tables = []

for row in d:
    z = row[0]
    Y = np.array(row[1:]) + conversion
    Y = np.round(Y, 2)
    s = ~np.isnan(Y)

    t = Table()

    t.add_column(Column(data = z*np.ones(np.sum(s)), name = 'z'))
    t.add_column(Column(data = X[s], name = xname, unit = 'dex(Msun)'))
    t.add_column(Column(data = Y[s], name = yname, unit = unit))
    tables.append(t)

table = vstack(tables)

table.meta['x'] = xname
table.meta['y'] = yname
table.meta['name'] = 'Bluetides'
table.meta['redshifts'] = list(set(table['z'].data))
table.meta['references'] = ['2016MNRAS.455.2778F', '2017MNRAS.469.2517W']


filename = f'../data/{name(xname)}_{name(yname)}.ecsv'

table.write(filename, format = 'ascii.ecsv', overwrite=True)
table.write(f'/Users/stephenwilkins/Dropbox/Research/modules/flare_data/flags_data/data/ScalingRelations/{name(xname)}/{name(yname)}/models/bluetides.ecsv', overwrite = True)
