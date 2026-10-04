"""Peak stretching frequency of N-H / N-D from cpptraj distance time series.

Usage:  python analyze_nh_spectrum.py dist_H_long.dat dist_D_long.dat [dt_fs]

Inputs are cpptraj `distance` outputs (header line + two columns).
Hann window + 8x zero-padding are used only to locate the peak smoothly;
the true frequency resolution is set by the record length (printed at the end).
"""
import sys
import numpy as np

fh, fd = sys.argv[1], sys.argv[2]
dt = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5   # fs per frame
h = np.loadtxt(fh, skiprows=1)[:, 1]
d = np.loadtxt(fd, skiprows=1)[:, 1]

def peak_wavenumber(x, pad=8):
    x = x - x.mean()
    x = x * np.hanning(len(x))
    n = len(x) * pad
    f = np.fft.rfft(x, n=n)
    freqs = np.fft.rfftfreq(n, d=dt * 1e-15)
    i = np.argmax(np.abs(f[1:])) + 1
    return freqs[i] / 2.998e10          # Hz -> cm^-1

wh, wd = peak_wavenumber(h), peak_wavenumber(d)
print(f"frames H, D: {len(h)} {len(d)}")
print(f"N-H mean, std: {h.mean():.4f} {h.std():.4f}")
print(f"N-D mean, std: {d.mean():.4f} {d.std():.4f}")
print(f"peak N-H (cm^-1): {wh:.1f}")
print(f"peak N-D (cm^-1): {wd:.1f}")
print(f"ratio H/D: {wh/wd:.3f}")
print(f"raw bin width (cm^-1): {1/(len(h)*dt*1e-15)/2.998e10:.1f}")
