import tkinter as tk
from tkinter import messagebox, ttk
from pynput import mouse, keyboard
import time
from look_away_window import LookAwayWindow
import settings

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("20-20-20 Rule Timer")
        self.root.geometry("500x400")
        
        self.init_settings()
        self.create_styles()
        self.create_widgets()
        self.update_timer()
        self.monitor_activity()

    def init_settings(self):
        self.focus_time = settings.DEFAULT_FOCUS_TIME # minutes
        self.idle_time = settings.DEFAULT_IDLE_TIME  # seconds
        self.lookaway_time = settings.DEFAULT_LOOKAWAY_TIME  # seconds
        self.time_left = self.focus_time
        self.active = False
        self.paused = False
        self.last_activity_time = time.time()
        self.mouse_listener = None
        self.keyboard_listener = None

    def create_styles(self):
        self.h1_style = ("Helvetica", 48)
        self.p1_style = ("Helvetica", 12)
        self.p2_style = ("Helvetica", 10)

    def create_widgets(self):
        self.create_notebook()
        self.create_timer_tab_widgets()
        self.create_settings_tab_widgets()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        self.timer_frame = tk.Frame(self.notebook, padx=10, pady=10)
        self.settings_frame = tk.Frame(self.notebook, padx=10, pady=10)
        
        self.notebook.add(self.timer_frame, text='Timer')
        self.notebook.add(self.settings_frame, text='Settings')

    def create_timer_tab_widgets(self):
        self.timer_frame_inner = tk.Frame(self.timer_frame)
        self.timer_frame_inner.pack(pady=10)

        self.subtract_button = tk.Button(self.timer_frame_inner, text="-", command=self.subtract_time, width=3, height=2, font=self.p1_style, state=tk.DISABLED)
        self.subtract_button.pack(side=tk.LEFT, padx=10)
        
        self.timer_label = tk.Label(self.timer_frame_inner, text=self.format_time(self.time_left), font=self.h1_style)
        self.timer_label.pack(side=tk.LEFT, padx=10)
        
        self.add_button = tk.Button(self.timer_frame_inner, text="+", command=self.add_time, width=3, height=2, font=self.p1_style, state=tk.DISABLED)
        self.add_button.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(self.timer_frame, text="Inactive", font=self.p1_style)
        self.status_label.pack(pady=5)
        
        self.pause_label = tk.Label(self.timer_frame, text="", font=self.p1_style)
        self.pause_label.pack(pady=5)
        
        self.idle_time_label = tk.Label(self.timer_frame, text=f"Idle Time: {self.idle_time} seconds", font=self.p1_style)
        self.idle_time_label.pack(pady=5)
        
        self.lookaway_time_label = tk.Label(self.timer_frame, text=f"Lookaway Time: {self.lookaway_time} seconds", font=self.p1_style)
        self.lookaway_time_label.pack(pady=5)
        
        self.create_timer_buttons()
        
        self.message_label = tk.Label(self.timer_frame, text="", font=self.p2_style)
        self.message_label.pack(pady=10)

    def create_timer_buttons(self):
        self.button_frame = tk.Frame(self.timer_frame)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer, width=10, height=2, font=self.p1_style)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_timer, width=10, height=2, font=self.p1_style)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

    def create_settings_tab_widgets(self):
        self.custom_time_label = tk.Label(self.settings_frame, text="Custom Time (min)", font=self.p2_style)
        self.custom_time_label.pack(pady=5)
        self.custom_time_entry = tk.Entry(self.settings_frame)
        self.custom_time_entry.pack(pady=5)
        
        self.custom_idle_label = tk.Label(self.settings_frame, text="Custom Idle Time (sec)", font=self.p2_style)
        self.custom_idle_label.pack(pady=5)
        self.custom_idle_entry = tk.Entry(self.settings_frame)
        self.custom_idle_entry.pack(pady=5)
        
        self.custom_lookaway_label = tk.Label(self.settings_frame, text="Custom Lookaway Time (sec):", font=self.p2_style)
        self.custom_lookaway_label.pack(pady=5)
        self.custom_lookaway_entry = tk.Entry(self.settings_frame)
        self.custom_lookaway_entry.pack(pady=5)

        # save settings button
        self.save_settings_button = tk.Button(self.settings_frame, text="Apply", command=self.set_custom_times, width=10, height=2, font=self.p1_style)
        self.save_settings_button.pack(pady=10)
        
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def start_timer(self):
        self.set_custom_times()
        self.disable_custom_inputs()
        self.enable_add_subtract_buttons()
        self.activate_timer()

    def stop_timer(self):
        self.deactivate_timer()        
        self.disable_add_subtract_buttons()
        self.enable_custom_inputs()
        self.reset_timer()

    def set_custom_times(self):
        if self.custom_time_entry.get():
            self.set_custom_time()
        if self.custom_idle_entry.get():
            self.set_custom_idle_time()
        if self.custom_lookaway_entry.get():
            self.set_custom_lookaway_time()

    def disable_custom_inputs(self):
        # disable the settings frame
        self.notebook.tab(1, state='disabled')

    def activate_timer(self):
        self.active = True
        self.paused = False
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Active")

    def deactivate_timer(self):
        self.active = False
        self.stop_button.config(state=tk.DISABLED)
        self.disable_add_subtract_buttons()
        
    def add_time(self):
        self.time_left += 300
        self.timer_label.config(text=self.format_time(self.time_left))

    def subtract_time(self):
        self.time_left = max(0, self.time_left - 300)
        self.timer_label.config(text=self.format_time(self.time_left))
    
    def disable_add_subtract_buttons(self):
        self.subtract_button.config(state=tk.DISABLED)
        self.add_button.config(state=tk.DISABLED)
    
    def enable_add_subtract_buttons(self):
        self.subtract_button.config(state=tk.NORMAL)
        self.add_button.config(state=tk.NORMAL)

    def reset_timer(self):
        self.time_left = self.focus_time
        self.timer_label.config(text=self.format_time(self.time_left))
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Inactive")

    def enable_custom_inputs(self):
        # enable the settings frame
        self.notebook.tab(1, state='normal')

    def update_timer(self):
        if self.active and not self.paused:
            self.time_left -= 1
            if self.time_left <= 0:
                self.reset_timer()
                self.show_look_away_window()
                # stop activity monitoring
                
            self.timer_label.config(text=self.format_time(self.time_left))
        self.root.after(1000, self.update_timer)

    def monitor_activity(self):
        def on_activity(*args):
            self.last_activity_time = time.time()
            if self.paused:
                self.resume_timer()

        self.mouse_listener = mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=on_activity)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        self.check_idle_time()

    def check_idle_time(self):
        if self.active and (time.time() - self.last_activity_time > self.idle_time):
            if not self.paused:
                self.pause_timer()
        self.root.after(500, self.check_idle_time)

    def pause_timer(self):
        self.paused = True
        self.show_message("Timer paused due to inactivity")
        self.pause_label.config(text="Paused")

    def resume_timer(self):
        self.paused = False
        self.show_message("Timer resumed")
        self.pause_label.config(text="")

    def show_message(self, message):
        self.message_label.config(text=message)
        self.root.after(2000, lambda: self.message_label.config(text=""))

    def set_custom_time(self):
        try:
            custom_time = int(self.custom_time_entry.get()) * 60
            self.focus_time = custom_time
            self.time_left = custom_time
            self.timer_label.config(text=self.format_time(self.time_left))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid focus time")

    def set_custom_idle_time(self):
        try:
            custom_idle_time = int(self.custom_idle_entry.get())
            self.idle_time = custom_idle_time
            self.idle_time_label.config(text=f"Idle Time: {self.idle_time} seconds")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid idle time")
    
    def set_custom_lookaway_time(self):
        try:
            custom_lookaway_time = int(self.custom_lookaway_entry.get())
            self.lookaway_time = custom_lookaway_time
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid lookaway time")

    def show_look_away_window(self):
        self.stop_activity_monitoring()
        self.look_away_window = LookAwayWindow(self.root, self.reset_and_resume_timer, lookaway_time=self.lookaway_time)

    def stop_activity_monitoring(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def reset_and_resume_timer(self):
        self.time_left = self.focus_time
        self.timer_label.config(text=self.format_time(self.time_left))
        self.start_timer()
        self.monitor_activity()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()