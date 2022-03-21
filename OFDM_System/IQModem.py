import numpy as np
from numpy import cos, sin, pi, arange
from Database import Database


class IQModem:
    filterdesigner = None
    ia_rrc_filter = None

    def __init__(self, filterdesigner, os: int):
        self.filterdesigner = filterdesigner
        self.os = os
        self.ia_rrc_filter = self.filterdesigner.create_rrc_filter(scale_factor=30, f_s=1, f_a=self.os,
                                                                   roll_off=0.35)
        Database.save_impulse_answer_rrc_filter(impulse_answer=self.ia_rrc_filter)

    def modulate_ofdm_signal(self, ofdm_time_signal: list) -> list:
        real_data = []
        imag_data = []
        for i in range(len(ofdm_time_signal)):
            real_data.append(ofdm_time_signal[i].real)
            imag_data.append(ofdm_time_signal[i].imag)

        real_data_interpol = self._increase_sample_rate(real_data)
        imag_data_interpol = self._increase_sample_rate(imag_data)
        cfo = self.calc_cfo_offset_factor()
        f_tr = cfo + 2/self.os
        n = arange(len(real_data_interpol))
        cos_carrier = cos(2 * pi * n * f_tr)
        sin_carrier = sin(2 * pi * n * f_tr)

        real_data_interpol_mod = real_data_interpol * cos_carrier
        imag_data_interpol_mod = imag_data_interpol * sin_carrier
        ofdm_bandpass_signal = imag_data_interpol_mod + real_data_interpol_mod

        return ofdm_bandpass_signal

    def calc_cfo_offset_factor(self):
        scale_factor = (-1) * Database.cfo_percent/100 * 1 / self.os
        return scale_factor

    def extract_real_part_from_rx_signal(self, rx_signal):
        n = arange(len(rx_signal))
        cos_carrier = cos(2 * pi * n * 2 / self.os)
        rx_signal_i = rx_signal * cos_carrier
        rx_signal_i = np.convolve(rx_signal_i, self.ia_rrc_filter, "same")
        rx_signal_i = self._decrease_sample_rate(rx_signal_i)
        return rx_signal_i

    def extract_imag_part_from_rx_signal(self, rx_signal):
        n = arange(len(rx_signal))
        sin_carrier = sin(2 * pi * n * 2 / self.os)
        rx_signal_q = rx_signal * sin_carrier
        rx_signal_q = np.convolve(rx_signal_q, self.ia_rrc_filter, "same")
        rx_signal_q = self._decrease_sample_rate(rx_signal_q)
        return rx_signal_q

    def _decrease_sample_rate(self, rx_signal):
        rx_signal = rx_signal[::self.os]
        return rx_signal

    def _increase_sample_rate(self, signal) -> list:
        vector_size = self.os * len(signal)
        signal_with_zeros = list(np.zeros(vector_size))

        signal_with_zeros[::self.os] = signal
        ia_rrc_filter = self.ia_rrc_filter * 8
        signal_interpolated = list(np.convolve(signal_with_zeros, ia_rrc_filter, "same"))

        return signal_interpolated
