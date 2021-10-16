from pycbc import catalog
from pycbc import filter
from pycbc import psd
import matplotlib.pyplot as plt

def make_q_from_raw(merger):
    strain = merger.strain('H1')
    strain = strain.whiten(4,4)

    strain = strain.time_slice(merger.time - 2, merger.time + 2)

    times, freqs, power = strain.qtransform(0.001, logfsteps = 100, qrange = (8,8), frange =  (20,512))

    return times, freqs, power ** 0.5

print(catalog.catalog.list_catalogs())

c = catalog.Catalog("GWTC-1-confident")

for n in c.names:
    m = catalog.Merger(n)

    t, f, p = make_q_from_raw(m)

    plt.pcolormesh(t,f,p, shading = "auto")
    plt.yscale('log')
    plt.xlim(m.time - 0.5, m.time + 0.5)
    plt.show()