import tkinter as tk
from api import init_api
from ui import setup_ui, start_load_news
from APIkey import API_KEY #Change accordingly

root = tk.Tk()  

init_api(API_KEY)
setup_ui(root)

# Auto-load General news
start_load_news("general")

root.mainloop()