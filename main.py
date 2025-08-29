import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

def start_download():
    threading.Thread(target=download).start()

def download():
    url = url_entry.get()
    folder = folder_path.get()
    if not url or not folder:
        messagebox.showerror("Error", "Please enter a URL and select a folder")
        return

    cmd = ["yt-dlp"]


    if download_type.get() == "Audio":
        cmd.extend(["-x", "--audio-format", file_type.get()])
    else: # Video
     
        quality = quality_var.get().lower()
        if quality == "best":
            cmd.append("-f bestvideo+bestaudio/best")
        elif quality == "worst":
            cmd.append("-f worstvideo+worstaudio/worst")
        
        cmd.extend(["--recode-video", file_type.get()])


    if subtitles_var.get():
        cmd.extend(["--write-subs", "--sub-lang", subtitles_lang.get()])
        
    cmd.extend(["-o", os.path.join(folder, "%(title)s.%(ext)s")])

    cmd.append(url)

    try:
        output_text.delete(1.0, tk.END)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        for line in process.stdout:
            output_text.insert(tk.END, line)
            output_text.see(tk.END)

        process.wait()
        if process.returncode == 0:
            messagebox.showinfo("Success", "Download completed!")
        else:
            messagebox.showerror("Error", "Download failed! Check console output.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("yt-dlp GUI Downloader")
root.geometry("700x500")
root.resizable(False, False)

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=60)
url_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

tk.Label(root, text="Save Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
folder_path = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=folder_path, width=50)
folder_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=10, pady=10)

download_type = tk.StringVar(value="Audio")
tk.Label(root, text="Download Type:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
ttk.Radiobutton(root, text="Audio", variable=download_type, value="Audio").grid(row=2, column=1, sticky="w")
ttk.Radiobutton(root, text="Video", variable=download_type, value="Video").grid(row=2, column=1, sticky="e")

tk.Label(root, text="File Format:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
file_type = tk.StringVar(value="mp3")
file_options = ["mp3", "wav", "m4a", "mp4", "mkv", "webm"]
file_combobox = ttk.Combobox(root, textvariable=file_type, values=file_options, state="readonly")
file_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="w")

playlist_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Download Entire Playlist", variable=playlist_var).grid(row=4, column=1, sticky="w", padx=10, pady=5)

subtitles_var = tk.BooleanVar()
tk.Checkbutton(root, text="Download Subtitles", variable=subtitles_var).grid(row=5, column=1, sticky="w", padx=10, pady=5)
tk.Label(root, text="Subtitle Language:").grid(row=5, column=0, sticky="e")
subtitles_lang = tk.StringVar(value="en")
ttk.Entry(root, textvariable=subtitles_lang, width=10).grid(row=5, column=2, sticky="w")

tk.Label(root, text="Video Quality:").grid(row=6, column=0, sticky="e")
quality_var = tk.StringVar(value="Best")
quality_options = ["Best", "Worst"]
quality_combobox = ttk.Combobox(root, textvariable=quality_var, values=quality_options, state="readonly")
quality_combobox.grid(row=6, column=1, sticky="w")
quality_combobox.config(state="disabled") # Initially disabled

def update_options(*args):
    if download_type.get() == "Audio":
        file_combobox.config(values=["mp3", "wav", "m4a"])
        quality_combobox.config(state="disabled")
    else: # Video
        file_combobox.config(values=["mp4", "mkv", "webm"])
        quality_combobox.config(state="readonly")
    # Reset to default value if the current value is not in the new list
    current_file_type = file_type.get()
    if current_file_type not in file_combobox['values']:
        file_type.set(file_combobox['values'][0])

download_type.trace_add("write", update_options)
update_options()

tk.Button(root, text="Start Download", command=start_download, width=20, bg="green", fg="white").grid(row=7, column=1, pady=15)

tk.Label(root, text="Console Output:").grid(row=8, column=0, sticky="nw", padx=10)
output_text = tk.Text(root, height=12, width=80)
output_text.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

root.mainloop() 
