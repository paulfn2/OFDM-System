import multiprocessing
import time
import queue
from numpy import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from OFDM_System.OfdmSystem import OfdmSystem
from OFDM_System.Database import Database
from multiprocessing.managers import BaseManager
from queue import LifoQueue


class Main:
    data = None
    xAxis = None
    line = None
    time_template = None
    signal_old = np.asarray([])
    time_text = None
    signal_queue = None
    analysis_queue = None
    ofdm_system = None

    def __init__(self):
        self.data = np.zeros(100)
        self.xAxis = np.linspace(0, 100, 100)
        self.ofdm_system = OfdmSystem()

    def main_process(self):
        self.signal_queue = multiprocessing.Queue()
        self.analysis_queue = multiprocessing.Queue()
        simulate = multiprocessing.Process(None, self.ofdm_system.start_simulation, args=(self.signal_queue,
                                                                                          self.analysis_queue))
        simulate.start()

        plot_id_1 = 1
        fig_1 = self.create_single_plot(plot_id_1)
        ani_1 = self.run_dynamic_plot(fig_1)  # DO NOT REMOVE "ani = " Otherwise some errors will occur

        # ani.save('double_pendulum.mp4', fps=15)
        plt.show()
        simulate.terminate()

        analysis_list = []
        while True:
            try:
                analysis_list.append(self.analysis_queue.get_nowait())
            except queue.Empty:
                break
        print("SNR (set):", Database.SNR)
        print("CFO (set):", Database.cfo_percent)
        print("Total Number of Received Bits: ", analysis_list[len(analysis_list)-1][2])
        print("False received Bits: ", analysis_list[len(analysis_list)-1][1])
        print("BER: ", analysis_list[len(analysis_list)-1][0], " %")

    def run_dynamic_plot(self, fig):
        ani = animation.FuncAnimation(fig, self.animate, 100,
                                      interval=25, blit=True, init_func=self.init)
        return ani

    def create_single_plot(self, plot_id):
        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, 1000), ylim=(-1, 1))
        ax.grid()
        self.line, = ax.plot([], [], lw=2)
        self.time_template = 'time = %.1fs'
        self.time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        return fig

    def init(self):
        self.line.set_data([], [])
        self.time_text.set_text('')
        return self.line, self.time_text

    def animate(self, i):
        try:
            result: np.ndarray = self.signal_queue.get_nowait()  # same as signal_queue.get(False)-> goes to except path if queue is empty
            self.xAxis = np.linspace(0, len(result), len(result))
            signal = [result]
            self.line.set_data(self.xAxis, signal)
        except queue.Empty:  # no data available
            pass
        self.time_text.set_text(self.time_template % (i * 0.05))
        return self.line, self.time_text

    @staticmethod
    def ofdm_transmission(q):

        while True:
            for i in range(100):
                noise = np.random.randn(100)
                q.put(noise)

            time.sleep(10)
            for i in range(100):
                noise = np.zeros(100)
                q.put(noise)


if __name__ == "__main__":
    main = Main()
    main.main_process()
