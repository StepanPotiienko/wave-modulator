import tkinter
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        Y = signal.square(2 * numpy.pi * self.frequency * self._X) * self.voltage_amplitude
        return self.create_plot(Y, "Square")

    def sawtooth(self):
        Y = signal.sawtooth(2 * numpy.pi * self.frequency * self._X) * self.voltage_amplitude
        return self.create_plot(Y, "Sawtooth")

    def dc(self):
        Y = numpy.ones_like(self._X) * self.voltage_amplitude
        return self.create_plot(Y, "DC Voltage Level")

    def create_plot(self, Y, title):
        fig, ax = pyplot.subplots(1, 1)
        ax.set_xlim(0, 4 * numpy.pi)
        ax.set_ylim(-self.voltage_amplitude - 20, self.voltage_amplitude + 20)
        line, = ax.plot(self._X, Y, lw=2, color="r", label=title.lower())
        ax.grid()
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig, line

    def update_waveform(self, line, waveform):
        if waveform == 'sine':
            Y = numpy.sin(self._X) * self.voltage_amplitude
        elif waveform == 'square':
            Y = signal.square(2 * numpy.pi * self.frequency * self._X) * self.voltage_amplitude
        elif waveform == 'sawtooth':
            Y = signal.sawtooth(2 * numpy.pi * self.frequency * self._X) * self.voltage_amplitude
        elif waveform == 'dc':
            Y = numpy.ones_like(self._X) * self.voltage_amplitude
        else:
            raise ValueError("Unknown waveform type")

        line.set_ydata(Y)
        return line


class WaveModulatorApp:
    def __init__(self):
        self.modulator = WaveModulator(voltage_amplitude=100, frequency=59)

    def build(self):
        fig, line = self.modulator.sin()
        self.user_interface = UserInterface(title="Wave Form Modulator", geometry="640x480", fig=fig, line=line, modulator=self.modulator)
        self.user_interface.build(self.update_plot, self.change_waveform)

    def update_plot(self, amplitude):
        self.modulator.voltage_amplitude = amplitude
        self.user_interface.update_figure()

    def change_waveform(self, waveform):
        self.user_interface.change_waveform(waveform)


class UserInterface:
    def __init__(self, title, geometry, fig, line, modulator):
        self.title = title
        self.geometry = geometry
        self.fig = fig
        self.line = line
        self.modulator = modulator
        self.current_waveform = 'sine'
        self.root = None

    def build(self, update_callback, waveform_callback):
        self.root = ctk.CTk()
        self.root.wm_title(self.title)
        self.root.geometry(self.geometry)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.amplitude_slider = ctk.CTkSlider(self.root, from_=0, to=self.modulator.voltage_amplitude, command=lambda val: update_callback(float(val)))
        self.amplitude_slider.pack()

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        sine_button = ctk.CTkButton(button_frame, text="Sine", command=lambda: waveform_callback('sine'))
        sine_button.grid(row=0, column=0)

        square_button = ctk.CTkButton(button_frame, text="Square", command=lambda: waveform_callback('square'))
        square_button.grid(row=0, column=1)

        sawtooth_button = ctk.CTkButton(button_frame, text="Sawtooth", command=lambda: waveform_callback('sawtooth'))
        sawtooth_button.grid(row=0, column=2)

        dc_button = ctk.CTkButton(button_frame, text="DC", command=lambda: waveform_callback('dc'))
        dc_button.grid(row=0, column=3)

        exit_btn = ctk.CTkButton(self.root, text="Exit", command=self.root.destroy)
        exit_btn.pack()

        tkinter.mainloop()

    def update_figure(self):
        self.line = self.modulator.update_waveform(self.line, self.current_waveform)
        self.fig.axes[0].set_ylim(-self.modulator.voltage_amplitude - 20, self.modulator.voltage_amplitude + 20)  
        self.canvas.draw()

    def change_waveform(self, waveform):
        self.current_waveform = waveform 
        self.line = self.modulator.update_waveform(self.line, waveform)
        self.canvas.draw()


app = WaveModulatorApp()
app.build()
