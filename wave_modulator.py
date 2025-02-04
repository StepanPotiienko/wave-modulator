import numpy
from scipy import signal
import matplotlib.pyplot as pyplot
import mplcursors


class WaveModulator:
    def __init__(
        self, voltage_amplitude: float = 220, phase: float = 0, frequency: float = 60
    ):
        self.voltage_amplitude = voltage_amplitude
        self.phase = phase
        self.frequency = frequency
        self._X = numpy.linspace(0, 4 * numpy.pi, 400)

    def sin(self):
        Y = numpy.sin(self.frequency * self._X + self.phase) * self.voltage_amplitude
        return self.create_plot(Y, "Sine")

    def square(self):
        Y = signal.square(self.frequency * self._X) * self.voltage_amplitude
        return self.create_plot(Y, "Square")

    def sawtooth(self):
        Y = signal.sawtooth(self.frequency * self._X) * self.voltage_amplitude
        return self.create_plot(Y, "Sawtooth")

    def dc(self):
        Y = numpy.ones_like(self._X) * self.voltage_amplitude * self.frequency
        return self.create_plot(Y, "DC Voltage Level")

    def create_plot(self, Y, title):
        fig, ax = pyplot.subplots(1, 1)
        ax.set_xlim(0, 4 * numpy.pi)
        ax.set_ylim(-self.voltage_amplitude - 20, self.voltage_amplitude + 20)
        (line,) = ax.plot(self._X, Y, lw=2, color="r", label=title.lower())
        ax.grid()
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        cursor = mplcursors.cursor(line, hover=True)
        cursor.connect(
            "add",
            lambda sel: sel.annotation.set_text(
                f"X: {sel.target[0]:.2f}\nY: {sel.target[1]:.2f}"
            ),
        )

        return fig, line

    def update_waveform(self, line, waveform):
        if waveform == "sine":
            Y = (
                numpy.sin(self.frequency * self._X + self.phase)
                * self.voltage_amplitude
            )
        elif waveform == "square":
            Y = (
                signal.square(self.frequency * self._X + self.phase)
                * self.voltage_amplitude
            )
        elif waveform == "sawtooth":
            Y = (
                signal.sawtooth(self.frequency * self._X + self.phase)
                * self.voltage_amplitude
            )
        elif waveform == "dc":
            Y = (
                numpy.ones_like(self.frequency * self._X + self.phase)
                * self.voltage_amplitude
            )
        else:
            raise ValueError("Unknown waveform type")

        line.set_ydata(Y)
        return line
