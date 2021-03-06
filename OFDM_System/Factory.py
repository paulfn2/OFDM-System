from OFDM_System.Filterdesigner import Filterdesigner
from OFDM_System.IQModem import IQModem


class Factory:

    @staticmethod
    def create_filter_designer():
        return Filterdesigner()

    @staticmethod
    def create_IQ_Modem(filterdesigner, os):
        return IQModem(filterdesigner, os)
