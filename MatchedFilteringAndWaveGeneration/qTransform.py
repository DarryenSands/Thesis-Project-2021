from pycbc import catalog
from pycbc import filter
from pycbc import psd
from pycbc.frame import query_and_read_frame
from pycbc.frame.losc import read_strain_losc
import matplotlib.pyplot as plt

def make_q_from_raw(detector,start, end):
    strain = read_strain_losc(detector, start, end)
    #strain = query_and_read_frame('LOSC', "H1:LOSC-STRAIN", start, end)
    #strain = merger.strain('H1')
    strain = strain.whiten(2,2)
    strain = filter.highpass_fir(strain, 15, 8)
    strain = filter.lowpass_fir(strain, 250, 8)

    #strain = strain.time_slice(merger.time - 2, merger.time + 2)

    times, freqs, power = strain.qtransform(0.001, logfsteps = 100, qrange = (8,8), frange =  (20,512))

    return times, freqs, power ** 0.5

"""
print(catalog.catalog.list_catalogs())

c = catalog.Catalog("GWTC-1-confident")

for n in c.names:

    m = catalog.Merger(n)

    t, f, p = make_q_from_raw(m)

    plt.pcolormesh(t,f,p, shading = "auto")
    plt.yscale('log')
    plt.xlim(m.time - 0.5, m.time + 0.5)
    plt.show()
"""
#gpsStart = 1126259460
#gpsEnd = 1126259464

#gpsStart = 1167559934
#gpsEnd = 1167559938

gpsStarts = [1126259460, 1167559934, 1187008880,1187058325]
gpsEnds = [1126259464, 1167559938, 1187008884, 1187058329]


for i in range(len(gpsStarts)):
    t, f, p = make_q_from_raw('H1',gpsStarts[i], gpsEnds[i])

    plt.pcolormesh(t,f,p, shading = "auto")
    plt.yscale('log')
    #plt.xlim(m.time - 0.5, m.time + 0.5)
    plt.show()

    t, f, p = make_q_from_raw('L1',gpsStarts[i], gpsEnds[i])
    
    plt.pcolormesh(t,f,p, shading = "auto")
    plt.yscale('log')
    #plt.xlim(m.time - 0.5, m.time + 0.5)
    plt.show()