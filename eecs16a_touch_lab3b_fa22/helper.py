import matplotlib.pyplot as plt
from scipy import signal
from scipy.integrate import cumtrapz
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from pylab import rcParams

def test_cap_IV(cap_IV):
    i_test = np.array([0.002,0.002,0.002,0.002,0.002])
    c_test = 1e-9
    t_test = 3e-6
    V_correct = [0.0, 6.0, 12.0, 18.0, 24.0]
    V_check = np.array(cap_IV(i_test, c_test, t_test))
    rtol = 1e-4
    if (np.linalg.norm(V_check - V_correct) / np.linalg.norm(V_correct) > rtol):
        print("Incorrect! Fix your cap_IV before moving on")
    else:
        print("cap_IV test passed!")

def test_v_out1(V_out1_notouch, V_out1_touch):
    R_in = 1e4
    C    = 50e-12
    C_t  = 150e-12
    dt   = .4e-6
    v_in = gen_vin()
    
    no_touch_equal = np.allclose(V_out1_notouch, integrate(v_in, dt, 0)/(R_in*C))
    touch_equal = np.allclose(V_out1_touch, integrate(v_in, dt, 0)/(R_in*C_t))
    
    if no_touch_equal and touch_equal:
        print("v_out1 test passed!")
    else:
        print("Incorrect! Try referring to the pre-lab reading and/or presentation for deriving voltage")

def square_wave_zerod():
    return np.concatenate((np.array(200*[0]), (0.01 * signal.square(2 * np.pi * 3 * np.linspace(0, 1, 1200)))))

def integrate(function, dt, c=0):
    return cumtrapz(function, dx=dt, initial=c);

def gen_vin():
    return .05 * signal.square(2 * np.pi * 2 * np.linspace(0, 1, 1000))[125:625:]

def plot_Vin_Vout(vo, vot, v_in, dt):
    time = [dt * x / dt for x in range(0, len(v_in))]
    tmax = time[-1]

    fig, ax1 = plt.subplots()
    plt.title("Voltage vs Time")
    plt.subplots_adjust(bottom=0.2)
    plt.grid(True)

    l, = plt.plot(time, vo, lw=2)
    plt.ylim(-(max(vo)*2),max(vo)*2)
    class Index(object):
        touch = False
        def a_touch(self, event):
            self.touch = True
            ydata = vot
            l.set_ydata(ydata)

            plt.draw()
        def a_notouch(self, event):
            self.touch = False
            ydata = vo
            l.set_ydata(ydata)
            plt.draw()

    callback = Index()
    axtouch   = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnotouch = plt.axes([0.81, 0.05, 0.1, 0.075])
    btouch = Button(axtouch, 'Touch')
    btouch.on_clicked(callback.a_touch)
    bnotouch = Button(axnotouch, 'No Touch')
    bnotouch.on_clicked(callback.a_notouch)
    ax1.set_xlabel('time')
    ax1.set_ylabel('Vout (V)', color='b')
    ax2 = ax1.twinx()
    ax2.plot(time, v_in, 'r')
    ax2.set_ylabel('Vin (V)', color='r')

    ax1.xaxis.set_ticks([0, tmax/4, tmax/2, 3*tmax/4, tmax])
    ax1.set_xticklabels(['T/4', 'T/2', '3T/4', 'T', '5T/4'])

    return btouch, bnotouch, callback
