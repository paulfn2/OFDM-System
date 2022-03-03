from OFDM_System.Factory import Factory
from OFDM_System.Database import Database
import numpy as np


class Receiver:

    def __init__(self):
        self.Filterdesigner = Factory.create_filter_designer()
        self.IQModem = Factory.create_IQ_Modem(self.Filterdesigner, 8)

    def receiver_processing_chain(self, rx_signal: list) -> list:
        rx_signal_i = self.IQModem.extract_real_part_from_rx_signal(rx_signal)
        rx_signal_q = self.IQModem.extract_imag_part_from_rx_signal(rx_signal)
        rx_analytic_signal = self._create_analytic_time_signal(rx_signal_i, rx_signal_q)
        rx_analytic_signal = self._remove_guard_interval(rx_analytic_signal)
        iq_signal = self._create_iq_signal(rx_analytic_signal)
        Database.add_iq_samples_to_received_signal(rx_iq_signal=iq_signal)
        bitstream = self._qam16_demodulator(iq_signal)
        Database.add_received_bits_to_rx_bitstream(rx_bitstream=bitstream)
        return bitstream

    # ToDo: find a way to get the start index for the guard interval in a dynamic way
    @staticmethod
    def _remove_guard_interval(iq_signal):
        iq_signal = iq_signal[32:]
        return iq_signal

    @staticmethod
    def _create_analytic_time_signal(rx_signal_i, rx_signal_q):
        rx_analytic_signal = []
        for i in range(len(rx_signal_i)):
            rx_analytic_signal.append(2 * complex(rx_signal_i[i], rx_signal_q[i]))
        return rx_analytic_signal

    @staticmethod
    def _create_iq_signal(rx_analytic_signal):
        rx_analytic_signal = np.fft.fft(rx_analytic_signal)
        return rx_analytic_signal

    def _qam16_demodulator(self, rx_signal):
        bit_stream = []
        for sample in rx_signal:
            buffer = []
            if sample.imag > 2:
                buffer = [0, 0] + self.map_least_significant_bits(sample.real)
            elif 2 > sample.imag > 0:
                buffer = [0, 1] + self.map_least_significant_bits(sample.real)
            elif 0 > sample.imag > -2:
                buffer = [1, 0] + self.map_least_significant_bits(sample.real)
            elif sample.imag < -2:
                buffer = [1, 1] + self.map_least_significant_bits(sample.real)
            for bit in buffer:
                bit_stream.append(bit)
        return bit_stream

    @staticmethod
    def map_least_significant_bits(signal_real) -> list:
        if signal_real > 2:
            return [0, 0]
        elif 2 > signal_real > 0:
            return [0, 1]
        elif 0 > signal_real > -2:
            return [1, 0]
        else:
            return [1, 1]
