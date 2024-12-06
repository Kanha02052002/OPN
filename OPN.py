import tkinter as tk
from tkinter import filedialog, Menu, messagebox
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledText
import webbrowser
from PIL import Image, ImageTk
import os
import sys

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)

def set_always_on_top(window):
    window.wm_attributes("-topmost", True)

def save_note():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"), 
                                                       ("All files", "*.*")])
    if file_path:
        content = note_area.text.get("1.0", tk.END).strip()
        with open(file_path, 'w') as file:
            file.write(content)

def open_note():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        note_area.text.delete("1.0", tk.END)
        note_area.text.insert(tk.END, content)

def exit_app():
    content = note_area.text.get("1.0", tk.END).strip()
    if content and content != ".":
        response = messagebox.askyesnocancel(
            "Warning", "Do you want to save your note before exiting?"
        )
        if response:
            save_note()
            root.destroy()
        elif response is None:
            return
        else:
            root.destroy()
    else:
        root.destroy()

def on_focus_out(event):
    root.wm_attributes("-alpha", 0.5)

def on_focus_in(event):
    root.wm_attributes("-alpha", 1.0)

def on_click(event):
    if note_area.text.get("1.0", "1.end") == "\n":
        note_area.text.delete("1.0", "1.end")

def on_key_press(event):
    if note_area.text.get("1.0", "1.end") == "\n":
        note_area.text.delete("1.0", "1.end")

def start_drag(event):
    root._drag_data = {"x": event.x, "y": event.y}

def do_drag(event):
    x = root.winfo_x() - root._drag_data["x"] + event.x
    y = root.winfo_y() - root._drag_data["y"] + event.y
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    max_x = screen_width - root.winfo_width()
    max_y = screen_height - root.winfo_height()
    x = min(max(x, 0), max_x)
    y = min(max(y, 0), max_y)
    root.geometry(f"+{x}+{y}")

def start_resize(event):
    root._resize_data = {"x": event.x_root, "y": event.y_root, "width": root.winfo_width(), "height": root.winfo_height()}

def do_resize(event):
    dx = event.x_root - root._resize_data["x"]
    dy = event.y_root - root._resize_data["y"]
    new_width = max(root._resize_data["width"] + dx, 300)
    new_height = max(root._resize_data["height"] + dy, 200)
    root.geometry(f"{new_width}x{new_height}")

def new_note():
    response = messagebox.askyesno("Warning", "All data will be deleted. Do you want to proceed?")
    if response:
        note_area.text.delete("1.0", tk.END)
        note_area.text.insert(tk.END, "")

def open_source_code():
    webbrowser.open("https://github.com/Kanha02052002/OPN")

def show_about():
    messagebox.showinfo(
        "About OPN",
        "OPN: On Page Notes, is an overlap application developed by Kanha Khantaal.\n\nGitHub: https://github.com/Kanha02052002"
    )

style = Style("darkly")
root = style.master
root.geometry("400x300")
root.title("Notes Application")
root.configure(bg='black')

root.overrideredirect(True)
set_always_on_top(root)

root.resizable(True, True)

icon_image = Image.open(resource_path("assests\opn.ico"))
icon_image = icon_image.resize((32, 32))
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

navbar = tk.Frame(root, bg='#000000', height=30)
navbar.pack(fill='x')

navbar_label = tk.Label(navbar, text="Drag from here", bg='#000000', fg='white', font=("Arial", 12, "bold"))
navbar_label.pack(side='left', padx=10)

navbar.bind("<ButtonPress-1>", start_drag)
navbar.bind("<B1-Motion>", do_drag)
navbar_label.bind("<ButtonPress-1>", start_drag)
navbar_label.bind("<B1-Motion>", do_drag)

menu_bar = tk.Menu(root, bg='#333333', fg='white')

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_note)
file_menu.add_command(label="Save", command=save_note)
file_menu.add_separator()
file_menu.add_command(label="New note", command=new_note)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
file_menu.config(bg='#333333', fg='white', activebackground='#555555', activeforeground='white')

menu_bar.add_cascade(label="File", menu=file_menu)

about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", command=show_about)
about_menu.add_command(label="Source Code", command=open_source_code)

menu_bar.add_cascade(label="More", menu=about_menu)

root.config(menu=menu_bar)

note_area = ScrolledText(
    root,
    autohide=True,
    padding=5,
    bootstyle="dark"
)
note_area.text.config(
    wrap=tk.WORD,
    bg='#000000',
    fg='white',
    font=('Cascadia Code', 12),
    insertbackground='white',
    insertwidth=4,
    padx=10,
    pady=5
)
note_area.pack(expand=True, fill='both')

note_area.text.insert(tk.END, "")
note_area.text.bind("<Button-1>", on_click)
note_area.text.bind("<KeyPress>", on_key_press)

resize_grip = tk.Label(root, text="⇲", bg='black', fg='gray', font=("Arial", 10, "bold"), cursor="size_nw_se")
resize_grip.pack(side="bottom", anchor="se", padx=5, pady=5)

resize_grip.bind("<ButtonPress-1>", start_resize)
resize_grip.bind("<B1-Motion>", do_resize)

root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out)

root.mainloop()
