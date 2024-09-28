import tkinter as tk

class LookAwayWindow:
    def __init__(self, root, on_close_callback, lookaway_time):
        self.root = root
        self.on_close_callback = on_close_callback
        self.window = tk.Toplevel(self.root)
        self.window.attributes('-fullscreen', True)
        self.window.configure(bg='black')
        
        label = tk.Label(self.window, text="LOOK AWAY", font=("Helvetica", 72), fg="white", bg="black")
        label.pack(expand=True)
        
        self.time_label = tk.Label(self.window, text=str(lookaway_time), font=("Helvetica", 48), fg="white", bg="black")
        self.time_label.pack(pady=20)
        
        self.time_left = lookaway_time
        self.update_timer()
        
        # Force focus on the window
        self.window.attributes("-topmost", True)
        self.window.focus_force()
        
        # Bind the close event to switch the timer to inactive
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=str(self.time_left))
            self.window.after(1000, self.update_timer)
        else:
            self.window.destroy()
            self.on_close_callback()
    
    def on_close(self):
        self.window.destroy()
        self.on_close_callback()