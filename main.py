# ============================================
# MIPS-CodeWrite
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 6/20/2024
# License: GPLv2
# ============================================

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import queue
import threading
import customtkinter
import version
from functions import createDialog, fetchResource
import webbrowser
import platform
import injector_lib

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("MIPS CodeWrite")
        self.geometry(f"{680}x{480}")
        
        frame = customtkinter.CTkFrame(self, fg_color=("#fcfcfc", "#2e2e2e"))
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Create a small text box for user input on the left side
        label1 = customtkinter.CTkLabel(frame, text="Insertion Address:", font=("Arial", 14, "bold"), text_color="orange")
        label1.grid(row=0, column=0, sticky="w", padx=10)
        self.insertionAddress = customtkinter.CTkTextbox(frame, height=20)
        self.insertionAddress.grid(row=1, column=0, padx=10, sticky="nsew")
        
        # Create a larger text box for user input on the left side
        label2 = customtkinter.CTkLabel(frame, text="Codes:", font=("Arial", 14, "bold"), text_color="orange")
        label2.grid(row=2, column=0, sticky="w", padx=10)
        self.inputCode = customtkinter.CTkTextbox(frame)
        self.inputCode.grid(row=3, column=0, padx=10, sticky="nsew")
        
        # Create a text box for displaying data on the right side
        label3 = customtkinter.CTkLabel(frame, text="Output:", font=("Arial", 14, "bold"), text_color="orange")
        label3.grid(row=0, column=1, sticky="w", padx=10)
        self.output = customtkinter.CTkTextbox(frame)
        self.output.grid(row=1, column=1, rowspan=3, padx=10, sticky="nsew")

        # Create a button at the bottom to patch
        self.patchButton = customtkinter.CTkButton(frame, text="Patch", command=self.patch)
        self.patchButton.grid(row=4, column=0, columnspan=2, pady=10)

    def patch(self):
        insertionAddRaw = self.insertionAddress.get("1.0", "end-1c")
        asmRaw = self.inputCode.get("1.0", "end-1c")
        
        try:
            # Convert insertion address to integer
            memory_address_start = int(insertionAddRaw, 16)
        except ValueError:
            createDialog("Error", "error", "Invalid or missing insertion address. Please enter a valid hexadecimal number.")
            return
        
        # Preprocess ASM code: add commas between instructions if missing
        asm_lines = preprocess_asm_code(asmRaw)
        
        #try:
        gscode_lines = injector_lib.asm_to_gameshark(memory_address_start, asm_lines)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, '\n'.join(gscode_lines))
        #except Exception as e:
        #    createDialog("Error", "error", "Invalid ASM code.")
        #    return

def preprocess_asm_code(asmRaw):
    # Split by lines
    lines = asmRaw.splitlines()
    
    processed_lines = []
    
    for line in lines:
        # Remove leading and trailing spaces
        line = line.strip()
        
        # Add comma at the end if not already present
        if line and not line.endswith(','):
            line += ','
        
        processed_lines.append(line)
    
    return processed_lines

if __name__ == "__main__":
    app = App()
    app.mainloop()