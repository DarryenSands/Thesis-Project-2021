from pycbc import catalog
from pycbc.waveform import get_td_waveform
import pycbc.noise as noise
import pycbc.psd as psd
from pycbc.psd import welch, interpolate
from pycbc.filter import highpass_fir, lowpass_fir, matched_filter
import matplotlib.pyplot as plt
import numpy as np

def FakeNoise(f_lower, f_length, delta_f, delta_t, tsamples, i):
    '''
    Creates the signal within noise.
    Input: Low Cut-off frequency, the length of the frequency, the step-size of the frequency, the step-size of the time,
    the number of sample data points, the number of the data, the masses of the objects, 
    the distance of the merge, the spins of the objects

    Output: A graph of the Q-transform (noise)
    '''

    ps = psd.aLIGOaLIGO140MpcT1800545(f_length, delta_f, f_lower)
    ts = 10.0 * noise.noise_from_psd(tsamples, delta_t, ps)

    times, freqs, power = ts.whiten(4,4).qtransform(0.001, logfsteps=100, qrange=(8,8), frange=(20, 512),)
    #power = power ** (1.0/2.0)

    t = 10.0

    fig = plt.figure(figsize = (6,6))
    ax = fig.add_subplot(1,1,1)

    ax.pcolormesh(times, freqs, power, shading = "auto")
    ax.set_yscale('log')
    ax.set_axis_off()
    ax.set_xlim(t - 0.5, t+ 0.5)
    plt.savefig(f'/home/darryen/Documents/thesis-project-2021/Dataset/Noise/noisedata{i}.png', bbox_inches='tight')
    ax.cla()
    fig.clf()
    plt.close('all')
    

def Signal(f_lower, f_length, delta_f, delta_t, tsamples, i, m1, m2, dist, spin1, spin2):
    '''
    Creates the signal within noise.
    Input: Low Cut-off frequency, the length of the frequency, the step-size of the frequency, the step-size of the time,
    the number of sample data points, the number of the data, the masses of the objects, 
    the distance of the merge, the spins of the objects

    Output: A graph of the Q-transform (signal)
    '''

    ps = psd.aLIGOaLIGO140MpcT1800545(f_length, delta_f, f_lower)
    ts = noise.noise_from_psd(tsamples, delta_t, ps)

    hp,hc = get_td_waveform(approximant = "SEOBNRv4", 
    mass1 = m1, mass2 = m2, spin1z = spin1, spin2z = spin2, delta_t = delta_t, f_lower = f_lower, distance = dist)

    t = np.random.uniform(5,15)
    signal = hp
    signal.start_time += t

    ts = ts.add_into(signal)

    times, freqs, power = ts.whiten(4,4).qtransform(0.001, logfsteps=100, qrange=(8,8), frange=(20, 512),)

    power = power **(1.0/2.0)

    fig = plt.figure()

    ax = fig.gca()
    ax.pcolormesh(times, freqs, power, shading = "auto")
    plt.yscale('log')
    ax.axis('off')
    plt.xlim(t - 0.5, t + 0.5)
    plt.savefig(f'/home/darryen/Documents/thesis-project-2021/Dataset/Signal/signaldata{i}.png', bbox_inches='tight')
    ax.cla()
    fig.clf()
    plt.close('all')
    
    