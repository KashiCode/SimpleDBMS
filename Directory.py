import tkinter as tk
import sys

# create the Tkinter window
window = tk.Tk()

# set the window title
window.title("Python Directory")

# set the window size and position
window.geometry("1000x300")
window.resizable(False, False)
window.configure(bg="#F0F0F0")

# create the label with the message
message = "This is your Python directory:\n" + sys.executable
label = tk.Label(window, text=message, font=("Helvetica", 12), bg="#F0F0F0", padx=20, pady=20)
label.pack(fill="both", expand=True)

# create the button to close the window
button = tk.Button(window, text="OK", font=("Helvetica", 12), bg="#606060", fg="white", command=window.destroy)
button.pack(side="bottom", padx=20, pady=10)

# start the window event loop
window.mainloop()
