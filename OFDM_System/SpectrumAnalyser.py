from numpy import fft
import numpy as np
import matplotlib.pyplot as plt


class SpectrumAnalyser:
    plot_ids = []

    def __init__(self):
        pass

    @staticmethod
    def plot_eye_diagram(signal, plot_size, plot_ID=None):
        plot_id = SpectrumAnalyser._manage_plot_ids(plot_ID)
        buffer_vector = []
        for i in range(0, len(signal), plot_size):
            buffer_vector.append(signal[i:i + plot_size])

        xAxis = np.linspace(0, plot_size, plot_size)
        plt.figure(plot_id)
        plt.plot(xAxis, np.asarray(buffer_vector).T)

    @staticmethod
    def plot_iq_chart(analytic_signal, plot_ID=None):
        plot_id = SpectrumAnalyser._manage_plot_ids(plot_ID)
        real_part = []
        imag_part = []

        for sample in analytic_signal:
            real_part.append(sample.real)
            imag_part.append(sample.imag)

        plt.figure(plot_id)
        plt.plot(real_part, imag_part, "+")
        plt.title("IQ - Diagram")
        plt.xlabel("Inphase Component")
        plt.ylabel("Quadrature Component")
        plt.grid()

    @staticmethod
    def calculate_nominated_power_spectrum(signal: list, N: int = 2048) -> np.ndarray:
        num_fft = N
        num_tapper = int(len(signal) / num_fft)
        fft_bins = np.zeros(num_fft)
        for i in range(num_tapper):
            transponder_samples = signal[i * num_fft:(1 + i) * num_fft]
            fft_bins = fft_bins + abs(1 / num_fft * np.fft.fft(transponder_samples)) ** 2
        return np.fft.fftshift(10 * np.log10(fft_bins))

    @staticmethod
    def plot_power_spectrum(signal, fft_size, plot_ID=None):
        plot_id = SpectrumAnalyser._manage_plot_ids(plot_ID)
        xAxis = np.arange(-fft_size / 2, fft_size / 2)
        Y = SpectrumAnalyser.calculate_nominated_power_spectrum(signal, fft_size)
        plt.figure(plot_id)
        plt.title("Power Spectrum")
        plt.ylabel("Power [dBw]")
        plt.plot(xAxis, Y)
        plt.grid()

    @staticmethod
    def plot_time_signal(signal, plot_ID=None):
        plot_id = SpectrumAnalyser._manage_plot_ids(plot_ID)
        plt.figure(plot_id)
        plt.title("Time Signal")
        plt.ylabel("U in V")
        plt.xlabel("Samples 0..N-1")
        plt.plot(signal)
        plt.grid()

    # Sets new plot ID if no id is selected
    @staticmethod
    def _manage_plot_ids(plot_ID):
        if plot_ID is None:
            highest_id = 0
            for single_id in SpectrumAnalyser.plot_ids:
                if single_id > highest_id:
                    highest_id = single_id
            plot_ID = highest_id + 1
        SpectrumAnalyser.plot_ids.append(plot_ID)
        return plot_ID
