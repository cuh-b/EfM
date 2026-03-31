# Copyright (c) 2026 Cubb
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (see LICENSE file)





# basic emergency file manager that works from windows 2000 up to the nt10 kernel
# by cubb, 2024-11-04
# this even works on Windows PE, which is kinda impressive as it is REALLY stripped down

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency File Manager")
        self.current_path = os.getcwd()

        # Create navigation frame
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_label = tk.Label(self.nav_frame, text=self.current_path, bg="lightgray", relief=tk.SUNKEN)
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.navigate_btn = tk.Button(self.nav_frame, text="Go To Path", command=self.navigate_to_path)
        self.navigate_btn.pack(side=tk.LEFT, padx=2)

        self.up_btn = tk.Button(self.nav_frame, text="↑ Up", command=self.go_parent_directory)
        self.up_btn.pack(side=tk.LEFT, padx=2)

        # File listbox
        self.file_listbox = tk.Listbox(root, width=80, height=20)
        self.file_listbox.pack()
        self.file_listbox.bind('<Double-1>', self.open_item)

        # Main buttons frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.copy_button = tk.Button(self.button_frame, text="Copy", command=self.copy_item)
        self.copy_button.pack(side=tk.LEFT, padx=2)

        self.move_button = tk.Button(self.button_frame, text="Move", command=self.move_item)
        self.move_button.pack(side=tk.LEFT, padx=2)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT, padx=2)

        self.rename_button = tk.Button(self.button_frame, text="Rename", command=self.rename_item)
        self.rename_button.pack(side=tk.LEFT, padx=2)

        # Load the initial file list
        self.load_file_list()
    def load_file_list(self):
        self.file_listbox.delete(0, tk.END)
        try:
            for item in os.listdir(self.current_path):
                self.file_listbox.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_parent_directory(self):
        parent = os.path.dirname(self.current_path)
        if parent != self.current_path:  # Prevent going above root
            self.current_path = parent
            self.path_label.config(text=self.current_path)
            self.load_file_list()

    def navigate_to_path(self):
        new_path = simpledialog.askstring("Navigate to Path", "Enter directory path:")
        if new_path:
            if os.path.isdir(new_path):
                self.current_path = new_path
                self.path_label.config(text=self.current_path)
                self.load_file_list()
            else:
                messagebox.showerror("Error", "Invalid directory path.")
    def open_item(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            item_name = self.file_listbox.get(selection[0])
            item_path = os.path.join(self.current_path, item_name)
            if os.path.isdir(item_path):
                self.current_path = item_path
                self.path_label.config(text=self.current_path)
                self.load_file_list()
            else:
                os.startfile(item_path)
    def copy_item(self):
        selection = self.file_listbox.curselection()
        if selection:
            item_name = self.file_listbox.get(selection[0])
            item_path = os.path.join(self.current_path, item_name)
            destination = filedialog.askdirectory(title="Select Destination")
            if destination:
                try:
                    if os.path.isdir(item_path):
                        shutil.copytree(item_path, os.path.join(destination, item_name))
                    else:
                        shutil.copy2(item_path, destination)
                    messagebox.showinfo("Success", "Item copied successfully.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
    def move_item(self):
        selection = self.file_listbox.curselection()
        if selection:
            item_name = self.file_listbox.get(selection[0])
            item_path = os.path.join(self.current_path, item_name)
            destination = filedialog.askdirectory(title="Select Destination")
            if destination:
                try:
                    shutil.move(item_path, destination)
                    messagebox.showinfo("Success", "Item moved successfully.")
                    self.load_file_list()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
    def delete_item(self):
        
        selection = self.file_listbox.curselection()
        if selection:
            item_name = self.file_listbox.get(selection[0])
            item_path = os.path.join(self.current_path, item_name)
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?")
            if confirm:
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    messagebox.showinfo("Success", "Item deleted successfully.")
                    self.load_file_list()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
    def rename_item(self):

        selection = self.file_listbox.curselection()
        if selection:
            item_name = self.file_listbox.get(selection[0])
            item_path = os.path.join(self.current_path, item_name)
            new_name = simpledialog.askstring("Rename Item", "Enter new name:")
            if new_name:
                new_path = os.path.join(self.current_path, new_name)
                try:
                    os.rename(item_path, new_path)
                    messagebox.showinfo("Success", "Item renamed successfully.")
                    self.load_file_list()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
if __name__ == "__main__":
    root = tk.Tk()
    app = FileManager(root)
    root.mainloop()
    