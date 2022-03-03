import multiprocessing
import queue
import threading
import numpy as np
from OFDM_System.Database import Database
from OFDM_System.SpectrumAnalyser import SpectrumAnalyser
from OFDM_System.Transmitter import Transmitter
from OFDM_System.Receiver import Receiver
from OFDM_System.Channel import Channel
import matplotlib.pyplot as plt


class OfdmSystem:
    receiver = None
    transmitter = None
    channel = None
    run_simulation = True
    SNR_dB = Database.SNR
    Analyser = None

    def __init__(self):
        self.transmitter = Transmitter(seed=None)
        self.receiver = Receiver()
        self.channel = Channel()
        self.tx_bitstream = []
        self.Analyser = AnalysingThread()

    def start_simulation(self, signal_queue, analysis_result_queue):
        Database.set_queue_for_ipc(signal_queue)  # has to be implemented!!
        bitstream_queue = queue.Queue()
        # parallel thread for BER and error rate analysis ! (Data is saved in database??)
        analysis_thread = threading.Thread(target=self.Analyser.analyse_transmission_quality,
                                           args=(bitstream_queue, analysis_result_queue))
        analysis_thread.start()

        rx_bitstream = self.start_transmission(bitstream_queue)
        # self.analyse_transmission_quality(rx_bitstream)
        self.plot_signals()
        plt.show()

    def stop_simulation(self):
        self.run_simulation = False

    @staticmethod
    def plot_signals():
        SpectrumAnalyser.plot_iq_chart(Database.received_iq_signal)
        SpectrumAnalyser.plot_power_spectrum(Database.bandpass_signal, 2048)

    def start_transmission(self, bitstream_queue) -> list:
        buffer_1024_bit = []
        rx_bitstream = []

        while True:

            if not self.run_simulation:
                break

            bit = self.transmitter.get_single_random_bit()

            if len(buffer_1024_bit) == 1024:
                self.tx_bitstream = self.tx_bitstream + buffer_1024_bit.copy()
                tx_signal = self.transmitter.transmitter_processing_chain(buffer_1024_bit)
                tx_signal = self.transmit_signal(tx_signal)
                Database.save_bandpass_signaL(bandpass_signal=tx_signal)
                rx_frame: list = self.receiver.receiver_processing_chain(tx_signal)
                rx_bitstream = rx_bitstream + rx_frame
                queue_data = buffer_1024_bit + rx_frame
                bitstream_queue.put(queue_data)  # add tx and rx signal to queue for BER analysis
                buffer_1024_bit.clear()
            buffer_1024_bit.append(bit)

        return rx_bitstream

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


class AnalysingThread:

    database = None
    tx_bitstream = []
    rx_bitstream = []
    BER = 0
    bit_cnt = 0
    error_cnt = 0

    def analyse_transmission_quality(self, bitstream_queue, analysis_result_queue):
        while True:
            bitstream = bitstream_queue.get()
            tx_bitstream = bitstream[:1024]
            rx_bitstream = bitstream[1024:]
            self.calculate_ber_and_error_rate(tx_bitstream, rx_bitstream)
            liste = [self.BER, self.error_cnt, self.bit_cnt]
            analysis_result_queue.put(liste)


    # the optimum is to transfer the information back to the main thread and print the info there
    def calculate_ber_and_error_rate(self, tx_bitstream, rx_bitstream):
        self.tx_bitstream = self.tx_bitstream + tx_bitstream
        self.rx_bitstream = self.rx_bitstream + rx_bitstream
        bit_cnt = len(rx_bitstream)
        self.bit_cnt = self.bit_cnt + bit_cnt
        for i in range(len(rx_bitstream)):
            if tx_bitstream[i] != rx_bitstream[i]:
                self.error_cnt += 1
        if self.error_cnt != 0:
            self.BER = 100 * self.error_cnt / len(self.rx_bitstream)


if __name__ == "__main__":
    ofdm_system = OfdmSystem()
