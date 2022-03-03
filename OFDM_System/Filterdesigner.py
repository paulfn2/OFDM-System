# design 2 Filter and compare the results
from numpy import ndarray, pi, sin, cos, sqrt, e
import numpy as np
import matplotlib.pyplot as plt


class Filterdesigner:

    def create_rrc_filter(self, scale_factor: int, f_s: float, f_a: float, roll_off: float):
        time_vector = self._create_time_vector(1 / f_a, 1 / f_s, scale_factor)
        ia = np.zeros(len(time_vector))
        return self._calculate_filter_bins(roll_off, ia, time_vector, f_s)

    @staticmethod
    def _create_time_vector(sample_time: float = 1 / 4, t_symbol_rate: float = 1, delay: float = 30) -> list:
        time = []
        Range = int(delay * t_symbol_rate / sample_time)
        for t in range(-1 * Range, Range + 1):
            t: float = t * sample_time
            time.append(t)
        return time

    @staticmethod
    def _calculate_filter_bins(roll_off: float, ia: ndarray, time: list,
                              t_symbol_rate: float) -> ndarray:
        for i in range(len(time)):
            if time[i] == 0:
                ia[i] = 1 - roll_off + 4 * roll_off / pi
            elif abs(abs(time[i]) - t_symbol_rate / (roll_off * 4)) < 1 * e - 16:
                ia[i] = (roll_off / sqrt(2)) * (
                        (1 + 2 / pi) * sin(pi / (4 * roll_off)) + (1 - 2 / pi) * cos(pi / (4 * roll_off)))
            else:
                denominator = pi * (time[i] / t_symbol_rate) * (1 - (4 * roll_off * (time[i] / t_symbol_rate)) ** 2)
                while denominator == 0:
                    roll_off = roll_off + 0.01
                    denominator = pi * (time[i] / t_symbol_rate) * (1 - (4 * roll_off * (time[i] / t_symbol_rate)) ** 2)

                ia[i] = (sin(pi * (time[i] / t_symbol_rate) * (1 - roll_off)) + (4 * roll_off) * (
                        time[i] / t_symbol_rate) * cos(pi * (time[i] / t_symbol_rate) * (1 + roll_off)))
                ia[i] = ia[i] / denominator
        ia: ndarray = ia / (sum(ia))
        return ia


if __name__ == "__main__":
    impulse_answer = Filterdesigner().create_rrc_filter(3, 1, 4,0.35)
    print(len(impulse_answer))
    plt.figure(1)
    plt.plot(impulse_answer)
    plt.show()
