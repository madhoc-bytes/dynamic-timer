import tkinter as tk

class LookAwayWindow:
    def __init__(self, root, on_close_callback):
        self.root = root
        self.on_close_callback = on_close_callback
        self.look_away_window = tk.Toplevel(self.root)
        self.look_away_window.attributes('-fullscreen', True)
        self.look_away_window.configure(bg='black')
        
        look_away_label = tk.Label(self.look_away_window, text="LOOK AWAY", font=("Helvetica", 72), fg="white", bg="black")
        look_away_label.pack(expand=True)
        
        self.look_away_time_label = tk.Label(self.look_away_window, text="20", font=("Helvetica", 48), fg="white", bg="black")
        self.look_away_time_label.pack(pady=20)
        
        self.look_away_time_left = 20
        self.update_look_away_timer()
        
        # Force focus on the look_away_window
        self.look_away_window.attributes("-topmost", True)
        self.look_away_window.focus_force()
        
        # Bind the close event to switch the timer to inactive
        self.look_away_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_look_away_timer(self):
        if self.look_away_time_left > 0:
            self.look_away_time_left -= 1
            self.look_away_time_label.config(text=str(self.look_away_time_left))
            self.look_away_window.after(1000, self.update_look_away_timer)
        else:
            self.look_away_window.destroy()
            self.on_close_callback()

    def on_close(self):
        self.look_away_window.destroy()
        self.on_close_callback()