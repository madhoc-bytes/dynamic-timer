import tkinter as tk
from tkinter import messagebox, ttk
from pynput import mouse, keyboard
import time
from look_away_window import LookAwayWindow

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("20-20-20 Rule Timer")
        self.root.geometry("500x400")
        
        # Initialize timer settings
        self.default_time = 20 * 60  # 20 minutes in seconds
        self.idle_time = 30 # seconds
        self.lookaway_time = 20 # seconds
        self.time_left = self.default_time
        self.active = False
        self.paused = False
        self.last_activity_time = time.time()

        # Create UI elements
        self.h1_style = ("Helvetica", 48)
        self.p1_style = ("Helvetica", 14)
        self.p2_style = ("Helvetica", 12)
        self.create_widgets()

        # Start the timer and activity monitoring
        self.update_timer()
        self.monitor_activity()

    def create_widgets(self):
        # Timer label
        self.label = tk.Label(self.root, text=self.format_time(self.time_left), font=(self.h1_style))
        self.label.pack(pady=10)
        
        # Active Status label
        self.status_label = tk.Label(self.root, text="Inactive", font=(self.p1_style))
        self.status_label.pack(pady=1)
        
        # Pause Status label
        self.pause_label = tk.Label(self.root, text="", font=(self.p1_style))
        self.pause_label.pack(pady=1)        

        # Idle time label
        self.idle_time_label = tk.Label(self.root, text=f"Idle Time: {self.idle_time} seconds", font=(self.p1_style))
        self.idle_time_label.pack(pady=5)

        # Lookaway time label
        self.lookaway_time_label = tk.Label(self.root, text=f"Lookaway Time: {self.lookaway_time} seconds", font=(self.p1_style))
        self.lookaway_time_label.pack(pady=5)

        
        # Start button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer, width=8, height=2, font=(self.p1_style))
        self.start_button.pack(side=tk.LEFT, padx=20)
        
        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer, width=8, height=2, font=(self.p1_style))
        self.stop_button.pack(side=tk.RIGHT, padx=20)            
        
        # Custom time entry
        self.custom_time_label = tk.Label(self.root, text="Custom Time (min)", font=(self.p2_style))
        self.custom_time_label.pack(pady=2)
        self.custom_time_entry = tk.Entry(self.root)
        self.custom_time_entry.pack(pady=5)

        # Custom idle time entry
        self.custom_idle_label = tk.Label(self.root, text="Custom Idle Time (sec)", font=(self.p2_style))
        self.custom_idle_label.pack(pady=2)
        self.custom_idle_entry = tk.Entry(self.root)
        self.custom_idle_entry.pack(pady=5)
        
        # Custom lookaway time
        self.custom_lookaway_label = tk.Label(self.root, text="Custom Lookaway Time (sec):", font=(self.p2_style))
        self.custom_lookaway_label.pack()        
        self.custom_lookaway_entry = tk.Entry(self.root)
        self.custom_lookaway_entry.pack()
        
        # Temporary messages
        self.message_label = tk.Label(self.root, text="", font=(self.p2_style))
        self.message_label.pack(pady=5)


    def format_time(self, seconds):
        # Format time in MM:SS
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def start_timer(self):
        # Set custom times if provided
        if self.custom_time_entry.get():
            self.set_custom_time()
        if self.custom_idle_entry.get():
            self.set_custom_idle_time()
        if self.custom_lookaway_entry.get():
            self.set_custom_lookaway_time()       

        # Disable input fields
        self.custom_time_entry.config(state=tk.DISABLED)
        self.custom_idle_entry.config(state=tk.DISABLED)
        self.custom_lookaway_entry.config(state=tk.DISABLED)

        # Activate timer
        self.active = True
        self.paused = False
        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Active")

    def stop_timer(self):
        # Deactivate timer
        self.active = False
        self.time_left = self.default_time
        self.label.config(text=self.format_time(self.time_left))
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Inactive")

        #enable input fields
        self.custom_time_entry.config(state=tk.NORMAL)
        self.custom_idle_entry.config(state=tk.NORMAL)
        self.custom_lookaway_entry.config(state=tk.NORMAL)

    def update_timer(self):
        # Update timer every second
        if self.active and not self.paused:
            self.time_left -= 1
            if self.time_left <= 0:
                self.time_left = self.default_time
                self.active = False
                self.start_button.config(state=tk.NORMAL)
                self.show_look_away_window()
            self.label.config(text=self.format_time(self.time_left))
        self.root.after(1000, self.update_timer)

    def monitor_activity(self):
        # Monitor mouse and keyboard activity
        def on_activity(*args):
            self.last_activity_time = time.time()
            if self.paused:
                self.paused = False
                self.show_message("Timer resumed")
                self.pause_label.config(text="")

        mouse_listener = mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity)
        keyboard_listener = keyboard.Listener(on_press=on_activity)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        self.check_idle_time()

    def check_idle_time(self):
        # Check for inactivity
        if self.active and (time.time() - self.last_activity_time > self.idle_time):
            if not self.paused:
                self.paused = True
                self.show_message("Timer paused due to inactivity")
                self.pause_label.config(text="Paused")
        self.root.after(500, self.check_idle_time)

    def show_message(self, message):
        # Display a temporary message
        self.message_label.config(text=message)
        self.root.after(2000, lambda: self.message_label.config(text=""))

    def set_custom_time(self):
        try:
            custom_time = int(self.custom_time_entry.get()) * 60
            self.default_time = custom_time
            self.time_left = custom_time
            self.label.config(text=self.format_time(self.time_left))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    def set_custom_idle_time(self):
        try:
            custom_idle_time = int(self.custom_idle_entry.get())
            self.idle_time = custom_idle_time
            self.idle_time_label.config(text=f"Idle Time: {self.idle_time} seconds")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def set_custom_lookaway_time(self):
        try:
            custom_lookaway_time = int(self.custom_lookaway_entry.get())
            self.lookaway_time = custom_lookaway_time
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    def show_look_away_window(self):        
        self.look_away_window = LookAwayWindow(self.root, self.reset_and_resume_timer, lookaway_time=self.lookaway_time)

    def reset_and_resume_timer(self):
        # Reset and resume the main timer
        self.time_left = self.default_time
        self.label.config(text=self.format_time(self.time_left))
        self.start_timer()