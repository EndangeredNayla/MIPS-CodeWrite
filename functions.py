# ============================================
# MIPS-CodeWrite
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 6/20/2024
# License: GPLv2
# ============================================

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path
import sys
import webbrowser
import tkinter.filedialog
import os
import threading
import json
import subprocess

def createDialog(windowTitle, warn, info, buttonTxt=None):
    completeWindow = ctk.CTkToplevel()
    completeWindow.title(windowTitle)

    # Load success image and display it in the success window
    img = ctk.CTkImage(Image.open(fetchResource("assets/operation/" + warn + ".png")), size=(100, 100))
    imgLabel = ctk.CTkLabel(completeWindow, image=img, text="")
    imgLabel.grid(row=0, column=0, padx=10, pady=10)
    imgLabel.image = img  # Keep a reference to the image

    if buttonTxt is not None:
        try:
            button = ctk.CTkButton(completeWindow, command=run_update, text=buttonTxt)
            button.grid(row=1, column=0, padx=50, pady=10)
        except Exception as e:
            print("Error creating button:", e)

    # Adjust geometry to place the window in the bottom right corner
    screen_width = completeWindow.winfo_screenwidth()
    screen_height = completeWindow.winfo_screenheight()
    window_width = completeWindow.winfo_reqwidth()
    window_height = completeWindow.winfo_reqheight()
    if sys.platform == "darwin":
        x_coordinate = 15
        y_coordinate = screen_height - window_height
    else:
        x_coordinate = 15
        y_coordinate = screen_height - window_height - 20
    completeWindow.geometry(f"+{x_coordinate}+{y_coordinate}")

    # Configure row and column weights
    completeWindow.columnconfigure(0, weight=1)
    completeWindow.rowconfigure(0, weight=1)

    # Display success message in the success window
    label = ctk.CTkLabel(completeWindow, text=info, font=ctk.CTkFont(size=18))
    label.grid(row=0, column=1, padx=25, pady=10)
    
    # Function to close the window after 2.5 seconds
    def close_window():
        completeWindow.destroy()

    # Close the window after 2.5 seconds
    completeWindow.after(2500, close_window)

    completeWindow.focus()

def fetchResource(resource_path: Path) -> Path:
    try:  # Running as *.exe; fetch resource from temp directory
        base_path = Path(sys._MEIPASS)
    except AttributeError:  # Running as script; return unmodified path
        return resource_path
    else:   # Return temp resource path
        return base_path.joinpath(resource_path)