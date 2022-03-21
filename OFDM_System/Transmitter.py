import numpy as np
from numpy import random
from Factory import Factory
from Database import Database


class Transmitter:
    os = 8
    Filterdesigner = None
    IQModem = None

    def __init__(self, seed: int = None):
        if seed is None:
            seed = random.randint(0, 1000)
        self.Filterdesigner = Factory.create_filter_designer()
        self.IQModem = Factory.create_IQ_Modem(self.Filterdesigner, self.os)
        random.seed(seed)

    @staticmethod
    def get_single_random_bit() -> int:
        single_bit = random.randn()
        if single_bit >= 0:
            single_bit = 1
        else:
            single_bit = 0
        return single_bit

    def transmitter_processing_chain(self, buffer_1024_samples: list):
        buffer_bank_256 = self._split_buffer_in_chunks(buffer_1024_samples, new_buffer_size=4)
        buffer_iq_samples = self._map_bitstream_to_qam16_data(buffer_bank_256)
        ofdm_time_signal = np.fft.ifft(buffer_iq_samples)
        Database.add_iq_samples_to_send_signal(tx_iq_signal=ofdm_time_signal)
        ofdm_time_signal = self._add_guard_interval(ofdm_time_signal)
        ofdm_bandpass_signal = self.IQModem.modulate_ofdm_signal(ofdm_time_signal)
        return ofdm_bandpass_signal

    @staticmethod
    def _split_buffer_in_chunks(buffer: list, new_buffer_size: int):
        buffer_vector = []
        for i in range(0, len(buffer), new_buffer_size):
            buffer_vector.append(buffer[i:i + new_buffer_size])
        return buffer_vector

    def _map_bitstream_to_qam16_data(self, buffer_bank_256: list) -> list:
        buffer_qam16_samples = []

        for buffer_4_bit in buffer_bank_256:
            iq_sample = self._qam16_modulator(buffer_4_bit)
            buffer_qam16_samples.append(iq_sample)
        return buffer_qam16_samples

    @staticmethod
    def _add_guard_interval(ofdm_time_signal):
        guard_interval_size = 1 / 8
        gi_samples = int(len(ofdm_time_signal) * guard_interval_size)
        index_gi = (len(ofdm_time_signal) - gi_samples)
        ofdm_time_signal_offset = ofdm_time_signal[index_gi:]
        ofdm_time_signal = list(ofdm_time_signal_offset) + list(ofdm_time_signal)
        return ofdm_time_signal

    @staticmethod
    def _qam16_modulator(buffer: list):
        if buffer[0] == 0:
            if buffer[1] == 0:
                if buffer[2] == 0:
                    if buffer[3] == 0:
                        return 3 + 3j
                    else:
                        return 1 + 3j
                else:
                    if buffer[3] == 0:
                        return -1 + 3j
                    else:
                        return -3 + 3j
            else:
                if buffer[2] == 0:
                    if buffer[3] == 0:
                        return 3 + 1j
                    else:
                        return 1 + 1j
                else:
                    if buffer[3] == 0:
                        return -1 + 1j
                    else:
                        return -3 + 1j
        else:
            if buffer[1] == 0:
                if buffer[2] == 0:
                    if buffer[3] == 0:
                        return 3 - 1j
                    else:
                        return 1 - 1j
                else:
                    if buffer[3] == 0:
                        return -1 - 1j
                    else:
                        return -3 - 1j
            else:
                if buffer[2] == 0:
                    if buffer[3] == 0:
                        return 3 - 3j
                    else:
                        return 1 - 3j
                else:
                    if buffer[3] == 0:
                        return -1 - 3j
                    else:
                        return -3 - 3j
