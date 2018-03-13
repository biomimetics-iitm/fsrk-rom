from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt
from problem import SerialSMD, PointLoad
from multimodel import MultiModelROM
from fsrk import FSRKROM

def rel_err(u0, u1):
    return np.abs(1-u1/u0)

def plot_fit(s, y, models):
    fig, ax = plt.subplots()
    lf, = ax.plot(s.imag, y.real, 'k-')
    for f in models.models:
        lg, = ax.plot(f.xdata.imag[0:2:], f.eval().real[0:2:], 'ko', markersize=4.)
    ylims = ax.get_ylim()
    for f in models.models:
        ax.plot([f.xdata.imag[0], f.xdata.imag[0]], [ylims[0], ylims[1]], 'k:', linewidth=1.)
    ax.plot([f.xdata.imag[-1], f.xdata.imag[-1]], [ylims[0], ylims[1]], 'k:', linewidth=1.)
    ax.set_xlabel(r'Frequency, $\omega$ [rad/s]')
    ax.set_ylabel(r'$g(\omega)$')
    ax.legend([lf, lg], [r'$g(\omega)$', r'$\hat g(\omega)$'])
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':

    # Degrees of freedom
    N = 500;
    # Mass
    m = [1.]
    # Damping
    c = [1e-2]
    # Stiffness
    k = [100]
    # Frequency domain
    omega = np.linspace(1e-6, 0.5, 500)
    # Damping function
    def damp_func(omega, **kwargs):
        return 1e4*(omega**3 - omega)

    # Load
    f = PointLoad(N, 1e-3, N-1)

    prob = SerialSMD(N=N, m=m, c=c, k=k, damp_func=damp_func)
    prob.assemble()

    # # Eigenproblem
    # w, v = prob.eigen_solve(shift=omega[10])

    # # Frequency response
    # u = prob.get_frf(omega, f, N-1)
    # u0 = prob.get_frf(omega, f, N-1, nonvisc=False)
    # plt.semilogy(omega, np.abs(u0))
    # plt.semilogy(omega, np.abs(u), 'r');
    # plt.show()

    # Full system
    u = prob.get_frf(omega, f, N-1)

    #rom_m_list = [2, 4, 3, 3]
    #rom_n_list = [6, 6, 4, 8]
    rom_m_list = [5]
    rom_n_list = [6]


    for rom_m, rom_n in zip(rom_m_list, rom_n_list):

        # Multi-model ROM
        mmr = MultiModelROM(prob.M, prob.C, prob.K, f.vec, damp_func)
        mmr.reduce(omega, rom_m, rom_n, stat_corr=True)
        ur1 = mmr.get_frf(omega, N-1)

        # FSRK ROM
        fsrk = FSRKROM(prob.M, prob.C, prob.K, f.vec, damp_func)
        fsrk.reduce(omega, rom_m, rom_n)
        ur2 = fsrk.get_frf(omega, N-1)

        e1 = rel_err(u, ur1)
        e2 = rel_err(u, ur2)

        # Plot FRF
        fig, ax = plt.subplots()
        ax.semilogy(omega, np.abs(u), 'k')
        ax.semilogy(omega, np.abs(ur1), 'k:')
        ax.semilogy(omega, np.abs(ur2), 'k--')
        ax.set_xlabel(r'Frequency, $\omega$ [rad/s]')
        ax.set_ylabel('Displacment [m]')
        ax.legend(['Full system', 'Multi-Model', 'FSRK ROM'])

        # Plot error
        fig1, ax1 = plt.subplots()
        ax1.semilogy(omega, np.abs(e1), 'k:')
        ax1.semilogy(omega, np.abs(e2), 'k--')
        ax1.set_xlabel(r'Frequency, $\omega$ [rad/s]')
        ax1.set_ylabel('Relative error')
        ax1.legend(['Multi-model', 'FSRK ROM'])

        plt.show()

