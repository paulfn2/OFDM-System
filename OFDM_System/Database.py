# the purpose of this class is to save signals or parameters that seems interesting
# on the processing chain
# Config Data can also be saved here
class Database:

    # Settings
    cfo_percent = 0.01

    received_iq_signal = []
    send_iq_signal = []
    rx_bitstream = []
    tx_bitstream = []
    bandpass_signal = []
    impulse_answer = []

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
        Database.bandpass_signal = Database.bandpass_signal + list(bandpass_signal)
