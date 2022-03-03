import queue
import numpy as np


class Database:

    # Settings
    SNR = 10
    cfo_percent: float = 0.000
    received_iq_signal: list = []
    send_iq_signal: list = []
    rx_bitstream: list = []
    tx_bitstream: list = []
    bandpass_signal: list = []
    impulse_answer: list = []
    spectrum_bp_signal: list = []
    received_bits: int = 0
    error_bits: int = 0
    ber: float = 0
    signal_queue: queue.Queue = None

    @staticmethod
    def set_queue_for_ipc(signal_queue: queue.Queue):  # ipc = interprocess communication
        Database.signal_queue = signal_queue

    @staticmethod
    def save_impulse_answer_rrc_filter(impulse_answer):
        Database.impulse_answer = list(impulse_answer)

    @staticmethod
    def add_iq_samples_to_received_signal(rx_iq_signal):
        Database.received_iq_signal = Database.received_iq_signal + list(rx_iq_signal)

    @staticmethod
    def add_iq_samples_to_send_signal(tx_iq_signal):
        Database.send_iq_signal = Database.send_iq_signal + list(tx_iq_signal)

    @staticmethod
    def add_received_bits_to_rx_bitstream(rx_bitstream):
        Database.rx_bitstream = Database.rx_bitstream + list(rx_bitstream)

    @staticmethod
    def add_send_bits_to_tx_bitstream(tx_bitstream):
        Database.tx_bitstream = Database.tx_bitstream + list(tx_bitstream)

    @staticmethod
    def save_bandpass_signaL(bandpass_signal):
        Database.bandpass_signal = bandpass_signal
        Database.signal_queue.put(np.asarray(bandpass_signal))

    @staticmethod
    def save_spectrum_bandpass_signal(spec_bp_signal):
        Database.spectrum_bp_signal = Database.spectrum_bp_signal + list(spec_bp_signal)

    # ToDo Make analytics data exchange thread save
    @staticmethod
    def save_mean_BER(ber):
        Database.ber = ber

    @staticmethod
    def save_total_number_of_received_bits(received_bits):
        Database.received_bits = received_bits

    @staticmethod
    def save_wrong_received_bits(error_bits):
        Database.error_bits = error_bits
