import tkinter as tk
import customtkinter as ctk  
import aweidaoTXT
import threading
from queue import Queue, Empty
import tempfile
import json

aweidaoTheme_json = """
{
    "CTk": {
      "fg_color": ["#EFEFEF"]
    },
    "CTkToplevel": {
      "fg_color": ["#EFEFEF"]
    },
    "CTkFrame": {
      "corner_radius": 0,
      "border_width": 0,
      "fg_color": ["gray90", "gray13"],
      "top_fg_color": ["gray85", "gray16"],
      "border_color": ["gray65", "gray28"]
    },
    "CTkFont": {
        "macOS": {
          "family": "Roboto",
          "size": 20,
          "weight": "normal"
        },
        "Windows": {
          "family": "Microsoft YaHei",
          "size": 20,
          "weight": "normal"
        },
        "Linux": {
          "family": "Roboto",
          "size": 20,
          "weight": "normal"
        }
      },
    "CTkButton": {
      "corner_radius": 5,
      "border_width": 0,
      "fg_color": ["#009688"],
      "border_color": ["#EFEFEF"],
      "hover_color": ["#007d71"],
      "text_color": ["#EFEFEF"],
      "text_color_disabled": ["EFEFEF"]
    },
    "CTkLabel": {
      "corner_radius": 0,
      "fg_color": "transparent",
      "text_color": ["gray14", "gray84"]
    },
    "CTkEntry": {
      "corner_radius": 5,
      "border_width": 2,
      "fg_color": ["#F9F9FA"],
      "border_color": ["#009688"],
      "text_color": ["gray14", "gray84"],
      "placeholder_text_color": ["gray52", "gray62"]
    },
    "CTkCheckBox": {
      "corner_radius": 6,
      "border_width": 3,
      "fg_color": ["#3a7ebf", "#1f538d"],
      "border_color": ["#3E454A", "#949A9F"],
      "hover_color": ["#325882", "#14375e"],
      "checkmark_color": ["#DCE4EE", "gray90"],
      "text_color": ["gray14", "gray84"],
      "text_color_disabled": ["gray60", "gray45"]
    },
    "CTkTextbox": {
      "corner_radius": 6,
      "border_width": 0,
      "fg_color": ["gray100", "gray20"],
      "border_color": ["#979DA2", "#565B5E"],
      "text_color": ["gray14", "gray84"],
      "scrollbar_button_color": ["gray55", "gray41"],
      "scrollbar_button_hover_color": ["gray40", "gray53"]
    },
    "CTkScrollableFrame": {
      "label_fg_color": ["gray80", "gray21"]
    }
  }
"""
with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
    json_content = json.loads(aweidaoTheme_json)
    json.dump(json_content, temp_file)
    temp_filename = temp_file.name
ctk.set_default_color_theme(temp_filename)
FONT = ("Dengxian", 15)


message_queue = Queue()
def update_gui_from_queue():
    try:
        # Try to get a message from the queue
        message = message_queue.get_nowait()
        result_var.set(message)
    except Empty:
        pass
    # Schedule the function to run again after 100 milliseconds
    app.after(100, update_gui_from_queue)

def threaded_task(entry1_value, entry2_value):
    aweidaoTXT.run(entry1_value, entry2_value, message_queue)

def execute_function():
    result_var.set("启动！")
    app.update()
    # Use threading to run the function in the background
    thread = threading.Thread(target=threaded_task, args=(entry1.get(), entry2.get()))
    thread.start()

app = tk.Tk()
app.title("阿苇岛撸串机")
app.geometry("400x250")  

# Create a centered frame
center_frame = tk.Frame(app)
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# For the first entry
tk.Label(center_frame, text="串号 ", font=FONT).grid(row=0, column=0, sticky=tk.E)
entry1 = ctk.CTkEntry(center_frame, width=120, font=FONT)  
entry1.grid(row=0, column=1, columnspan=2, pady=5)

# For the second entry 
tk.Label(center_frame, text="1 -", font=FONT).grid(row=1, column=0, sticky=tk.E)
entry2 = ctk.CTkEntry(center_frame, width=60, font=FONT)  
entry2.grid(row=1, column=1)
tk.Label(center_frame, text="页  ", font=FONT).grid(row=1, column=2, pady=5)

# Button to execute a function
button3 = ctk.CTkButton(center_frame, text="下载", command=execute_function, font=FONT) 
button3.grid(row=2, column=0, columnspan=3, pady=20)

# Labels to show results
result_var = tk.StringVar()
result_label = tk.Label(app, textvariable=result_var, foreground="#009688", font=("Dengxian", 10))  
result_label.place(relx=0.0, rely=1.0, anchor=tk.SW) 

update_gui_from_queue()
app.mainloop()