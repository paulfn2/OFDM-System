import numpy as np
from Database import Database
from SpectrumAnalyser import SpectrumAnalyser
from Transmitter import Transmitter
from Receiver import Receiver
from Channel import Channel
import matplotlib.pyplot as plt


class OfdmSystem:
    receiver = None
    transmitter = None
    channel = None
    SNR_dB = 10

    def __init__(self):
        self.transmitter = Transmitter(seed=None)
        self.receiver = Receiver()
        self.channel = Channel()
        self.tx_bitstream = []

    def run_radio_in_the_loop(self):

        rx_bitstream = self.start_transmission()
        self.analyse_transmission_quality(rx_bitstream)
        self.plot_signals()
        plt.show()

    @staticmethod
    def plot_signals():
        SpectrumAnalyser.plot_iq_chart(Database.received_iq_signal)
        SpectrumAnalyser.plot_power_spectrum(Database.bandpass_signal, 2048)
        #SpectrumAnalyser.plot_power_spectrum(Database.impulse_answer, len(Database.impulse_answer))

    def start_transmission(self) -> list:
        buffer_1024_bit = []
        rx_bitstream = []
        cnt = 0
        while cnt < 50:
            bit = self.transmitter.get_single_random_bit()

            if len(buffer_1024_bit) == 1024:
                self.tx_bitstream = self.tx_bitstream + buffer_1024_bit.copy()
                tx_signal = self.transmitter.transmitter_processing_chain(buffer_1024_bit)
                #print("Power(dBm) TX Signal", 10 * np.log10(self.measure_signal_power(tx_signal)))
                tx_signal = self.transmit_signal(tx_signal)
                Database.save_bandpass_signaL(bandpass_signal=tx_signal)
                #print("TX Power (dBm) TX Signal after AWGN", 10 * np.log10(self.measure_signal_power(tx_signal)))
                rx_frame = self.receiver.receiver_processing_chain(tx_signal)
                rx_bitstream = rx_bitstream + rx_frame
                buffer_1024_bit.clear()
                cnt += 1
            buffer_1024_bit.append(bit)
        return rx_bitstream

    def analyse_transmission_quality(self, rx_bitstream):
        bit_cnt = len(rx_bitstream)
        print("Total number of transmitted bits: ", bit_cnt)
        error_cnt = 0
        BER = 0
        for i in range(len(rx_bitstream)):
            if self.tx_bitstream[i] != rx_bitstream[i]:
                error_cnt += 1
        print("False received Bits: ", error_cnt)

        if error_cnt != 0:
            BER = 100 * error_cnt / len(rx_bitstream)
            BER = np.round(BER,3)
        print("BER: ", BER, " %")

    def transmit_signal(self, tx_signal):
        white_noise = self.create_noise(tx_signal)
        for i in range(len(tx_signal)):
            tx_signal[i] = tx_signal[i] + white_noise[i]
        return tx_signal

    def create_noise(self, signal):
        signal_power = self.measure_signal_power(signal)
        noise_power = self.calculate_noise_power(signal_power)
        white_noise: np.ndarray = np.random.randn(len(signal))
        white_noise = noise_power * white_noise
        return white_noise

    @staticmethod
    def measure_signal_power(signal):
        N = len(signal)
        power = 0

        for sample in signal:
            power += 1 / N * np.power(np.abs(sample), 2)
        return power

    def calculate_noise_power(self, signal_power):
        snr_lin = np.power(10, self.SNR_dB / 10)
        noise_power = np.sqrt(0.5 * signal_power / snr_lin)
        return noise_power


ofdm_system = OfdmSystem()
ofdm_system.run_radio_in_the_loop()
