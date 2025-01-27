import tkinter as tk
from tkinter import messagebox
import time

class TimerStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer and Stopwatch")
        
        self.timer_input_label = tk.Label(root, text="Set Timer (seconds):")
        self.timer_input_label.pack()

        self.timer_input = tk.Entry(root)
        self.timer_input.pack()

        self.start_timer_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_timer_button.pack()

        self.time_display = tk.Label(root, text="00:00:000", font=("Arial", 24))
        self.time_display.pack()

        self.stop_button = tk.Button(root, text="Start/Stop Stopwatch", command=self.toggle_stopwatch, state="disabled")
        self.stop_button.pack()

        self.elapsed_time = 0
        self.timer_running = False
        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.last_key_press_time = 0

        self.root.bind('<Return>', self.handle_enter)
        self.root.bind('<space>', self.handle_space)

    def update_display(self, milliseconds):
        mins = milliseconds // 60000
        secs = (milliseconds % 60000) // 1000
        ms = milliseconds % 1000
        self.time_display.config(text=f"{mins:02}:{secs:02}:{ms:03}")

    def start_timer(self):
        try:
            seconds = int(self.timer_input.get())
            if seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number!")
            return
        
        self.timer_running = True
        self.elapsed_time = 0
        self.stopwatch_running = False
        self.stop_button.config(state="normal")
        
        self.timer_interval = self.root.after(1000, self.countdown, seconds)

    def countdown(self, seconds):
        if seconds > 0:
            self.update_display(seconds * 1000)
            self.timer_interval = self.root.after(1000, self.countdown, seconds - 1)
        else:
            self.start_stopwatch()

    def start_stopwatch(self):
        self.stopwatch_running = True
        self.stop_button.config(state="normal")
        self.stopwatch_start_time = time.time() - self.elapsed_time / 1000
        self.stopwatch_interval = self.root.after(10, self.update_stopwatch)

    def update_stopwatch(self):
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start_time
            self.elapsed_time = int(elapsed * 1000)
            self.update_display(self.elapsed_time)
            self.stopwatch_interval = self.root.after(10, self.update_stopwatch)

    def stop_stopwatch(self):
        self.stopwatch_running = False
        self.root.after_cancel(self.stopwatch_interval)

    def toggle_stopwatch(self):
        if self.stopwatch_running:
            self.stop_stopwatch()
        else:
            self.start_stopwatch()

    def reset_interface(self):
        self.root.after_cancel(self.timer_interval)
        self.root.after_cancel(self.stopwatch_interval)
        self.elapsed_time = 0
        self.stopwatch_running = False
        self.timer_running = False
        self.timer_input.delete(0, tk.END)
        self.update_display(0)
        self.stop_button.config(state="disabled")

    def handle_enter(self, event):
        # Allow Enter only if stopwatch is not running
        input_value = self.timer_input.get()

        if not self.stopwatch_running:  # Start timer if stopwatch is not running
            if input_value:  # If there is an input value, start timer with that
                self.start_timer()
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid positive number!")

        elif self.stopwatch_running:  # If stopwatch is running, reset and start the timer with the new value
            if input_value:  # Only start timer if there is an input value
                self.reset_interface()
                self.start_timer()

    def handle_space(self, event):
        current_time = time.time()

        if current_time - self.last_key_press_time < 0.5:
            self.reset_interface()  # Detect double space and reset everything
        else:
            self.toggle_stopwatch()  # Start/Stop stopwatch

        self.last_key_press_time = current_time
        event.prevent_default()  # Prevent default spacebar behavior

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerStopwatchApp(root)
    root.mainloop()

