import tkinter as tk
from datetime import datetime

# Function to update time and date
def update_time():
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y/%m/%d')
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(1000, update_time)  # Update time every 1000ms (1 second)

# Function to handle window focus events
def on_focus_in(event):
    root.attributes('-alpha', 0.75)  # 75% When focused

def on_focus_out(event):
    root.attributes('-alpha', 0.5)  # Semi-transparent when unfocused (50%)

# Create the main window
root = tk.Tk()
root.title("Clock")
root.geometry('300x150')  # Initial size of the window
root.resizable(True, True)  # Allow resizing in both directions

# Keep the window on top
root.attributes('-topmost', True)

# Set initial transparency
root.attributes('-alpha', 1.0)

# Bind focus events
root.bind('<FocusIn>', on_focus_in)
root.bind('<FocusOut>', on_focus_out)

# Label to display time
time_label = tk.Label(root, text="", font=("Helvetica", 48))
time_label.pack(pady=20)

# Label to display date
date_label = tk.Label(root, text="", font=("Helvetica", 18))
date_label.pack()

# Initially update time and date
update_time()

# Start the Tkinter event loop
root.mainloop()
