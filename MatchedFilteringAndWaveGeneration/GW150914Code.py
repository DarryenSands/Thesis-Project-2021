from pycbc.frame import read_frame
from pycbc.filter import highpass_fir, lowpass_fir, matched_filter
from pycbc.waveform import get_fd_waveform, get_td_waveform
from pycbc.psd import welch, interpolate
from pycbc.catalog import Merger
import pylab 


for i in ['H1', 'L1']:
    h1 = Merger('GW150914').strain(i)
    h1 = highpass_fir(h1, 15,8)

    psd = interpolate(welch(h1), 1.0/ h1.duration)

    white_strain = (h1.to_frequencyseries() / psd ** 0.5).to_timeseries()
    
    smooth = highpass_fir(white_strain, 35, 8)
    smooth = lowpass_fir(white_strain, 300, 8)

    if i == 'L1':
        smooth *= -1 
        smooth.roll(int(.007 / smooth.delta_t))


    pylab.plot(smooth.sample_times, smooth, label = i)
pylab.legend()
pylab.xlim(1126259462.21, 1126259462.45)
pylab.savefig("StrainGW150914.png")
pylab.ylim(-150, 150)
pylab.ylabel('Smoothed-Whitened Strain')
pylab.grid()
pylab.xlabel('GPS Time (s)')
pylab.show()

hp, hc = get_fd_waveform(approximant="IMRPhenomD", mass1=40, mass2=32,
                         f_lower=20, delta_f=1.0/h1.duration)

hp.resize(len(h1) // 2 + 1)

snr = matched_filter(hp,h1,psd=psd, low_frequency_cutoff = 20.0)
snr = snr[len(snr) // 4: len(snr) * 3 // 4]

pylab.plot(snr.sample_times, abs(snr))
pylab.savefig("SNRGW150914.png")
pylab.ylabel('Signal-to-Noise')
pylab.xlabel('GPS Time (s)')
pylab.show()