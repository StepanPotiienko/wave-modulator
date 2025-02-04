import tkinter
import sys
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from wave_modulator import WaveModulator


class Application:
    def __init__(self):
        self.modulator = WaveModulator(voltage_amplitude=100, phase=45, frequency=1)

    def build(self):
        fig, line = self.modulator.sin()
        self.user_interface = UserInterface(
            title="Wave Form Modulator",
            geometry="1280x720",
            fig=fig,
            line=line,
            modulator=self.modulator,
        )

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
        self.current_waveform = "sine"
        self.root = None

    def build(self, update_callback, waveform_callback):
        self.root = ctk.CTk()
        self.root.wm_title(self.title)
        self.root.geometry(self.geometry)

        # I set it to light for now, for it looks awful on auto/dark. (-:
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.amplitude_value_var = tkinter.IntVar(
            self.root, value=self.modulator.voltage_amplitude
        )
        self.amplitude_value_label = tkinter.Label(
            self.root, textvariable=self.amplitude_value_var
        )
        self.amplitude_slider = ctk.CTkSlider(
            self.root,
            from_=0,
            variable=self.amplitude_value_var,
            to=self.modulator.voltage_amplitude,
            command=lambda val: update_callback(float(val)),
        )
        self.amplitude_slider.pack()
        self.amplitude_value_label.pack()

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        sine_button = ctk.CTkButton(
            button_frame, text="Sine", command=lambda: waveform_callback("sine")
        )
        sine_button.grid(row=0, column=0)

        square_button = ctk.CTkButton(
            button_frame, text="Square", command=lambda: waveform_callback("square")
        )
        square_button.grid(row=0, column=1)

        sawtooth_button = ctk.CTkButton(
            button_frame, text="Sawtooth", command=lambda: waveform_callback("sawtooth")
        )
        sawtooth_button.grid(row=0, column=2)

        dc_button = ctk.CTkButton(
            button_frame, text="DC", command=lambda: waveform_callback("dc")
        )
        dc_button.grid(row=0, column=3)

        self.root.mainloop()

    def update_figure(self):
        self.line = self.modulator.update_waveform(self.line, self.current_waveform)
        self.fig.axes[0].set_ylim(
            -self.modulator.voltage_amplitude - 10,
            self.modulator.voltage_amplitude + 10,
        )
        self.canvas.draw()

    def change_waveform(self, waveform):
        self.current_waveform = waveform
        self.line = self.modulator.update_waveform(self.line, waveform)
        self.canvas.draw()


app: Application = Application().build()
