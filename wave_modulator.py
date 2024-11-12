import numpy
from scipy import signal

import matplotlib.pyplot as pyplot


class WaveModulator:
    def __init__(self, voltage_amplitude, frequency):
        self.voltage_amplitude = voltage_amplitude
        self.frequency = frequency
        self._X = numpy.linspace(0, 4 * numpy.pi, 400)

    def sin(self):
        Y = numpy.sin(self._X) * self.voltage_amplitude
        return self.create_plot(Y, "Sine")

    def square(self):
        Y = (
            signal.square(2 * numpy.pi * self.frequency * self._X)
            * self.voltage_amplitude
        )
        return self.create_plot(Y, "Square")

    def sawtooth(self):
        Y = (
            signal.sawtooth(2 * numpy.pi * self.frequency * self._X)
            * self.voltage_amplitude
        )
        return self.create_plot(Y, "Sawtooth")

    def dc(self):
        Y = numpy.ones_like(self._X) * self.voltage_amplitude
        return self.create_plot(Y, "DC Voltage Level")

    def create_plot(self, Y, title):
        fig, ax = pyplot.subplots(1, 1)
        ax.set_xlim(0, 4 * numpy.pi)
        ax.set_ylim(-self.voltage_amplitude - 20, self.voltage_amplitude + 20)
        (line,) = ax.plot(self._X, Y, lw=2, color="r", label=title.lower())
        ax.grid()
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig, line

    def update_waveform(self, line, waveform):
        if waveform == "sine":
            Y = numpy.sin(self._X) * self.voltage_amplitude
        elif waveform == "square":
            Y = (
                signal.square(2 * numpy.pi * self.frequency * self._X)
                * self.voltage_amplitude
            )
        elif waveform == "sawtooth":
            Y = (
                signal.sawtooth(2 * numpy.pi * self.frequency * self._X)
                * self.voltage_amplitude
            )
        elif waveform == "dc":
            Y = numpy.ones_like(self._X) * self.voltage_amplitude
        else:
            raise ValueError("Unknown waveform type")

        line.set_ydata(Y)
        return line
