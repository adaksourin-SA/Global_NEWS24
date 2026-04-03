import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from PIL import Image, ImageTk

from api import get_top_news, search_news
from utils import fetch_and_cache_image, toggle_bookmark, is_bookmarked, load_bookmarks

# Global state
articles = []
index = 0
frames = []

# ================= UI SETUP =================

def setup_ui(root):
    global canvas, frame, progress, search_entry, dummy_root
    dummy_root = root # This var is to aid the features of refresh functionality

    root.title("Global-NEWS")
    root.geometry("750x622+300+100")
    root.resizable(False, False)
    myicon = ImageTk.PhotoImage(
    file="Icons\\news_icon.png")
    root.iconphoto(False, myicon)

    # ===== MENU =====
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    categories = ["general", "business", "health", "sports", "science", "technology"]

    for cat in categories:
        menubar.add_command(
            label=cat.capitalize(),
            font=('Times New Roman', 12,"bold"),
            command=lambda c=cat: start_load_news(c),
        )
    for _ in range(17):
        menubar.add_separator()
    menubar.add_command(label="Bookmarks", command=open_bookmarks_window)
    menubar.add_command(label=" Refresh", command=lambda c="general": start_load_news(c))
    menubar.add_command(label=" Exit", command=quit)

    # ===== TITLE =====
    title_frame = tk.Frame(root, background="#285A48")
    title_frame.pack(side="top", fill= "x")

    icon_can = tk.Canvas(title_frame,background="#285A48",height=60, width=60, bd=0,
                         highlightthickness=0, relief="flat")
    icon_can.pack(side="left",padx=(220,5))

    icon_can.image = ImageTk.PhotoImage(
    file="Icons\\news_icon3.png")
    icon_can.create_image((32,32), image=icon_can.image)

    tk.Label(title_frame, text="Global-NEWS 24",
             font=("Times New Roman", 26, "bold"),
            #  foreground= "#E76F2E",
             foreground= "white",
             background="#285A48"
             ).pack(side="left",pady=5)

    # ===== DRAWING BEAUTIFICATION LINES =====
    linecan = tk.Canvas(root, bg="purple", height=2)
    linecan.pack(side="top", fill="x")

    # ===== SEARCH BAR =====
    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=5)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    tk.Button(search_frame, text="Search", command=start_search,
              background="#4C5C2D",
              foreground="white").pack(side="right")

    # ===== DRAWING BEAUTIFICATION LINES =====
    linecan = tk.Canvas(root, bg="purple", height=2)
    linecan.pack(side="top", fill="x")

    # ===== CONTENT AREA =====
    '''A frame has to be created to contain both canvas and scrollbar as frames does not inherit
    scroll facilities and canvas cannot contain a scrollbar within'''
    midframe = tk.Frame(root)
    midframe.pack(fill="both", expand=True)

    canvas = tk.Canvas(midframe)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(midframe, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))
    # Above line tells canvas how much of it should be inside the gui at a time.

    '''One cannot just put a frame inside canvas, we must use a window to put tkinter general 
    objects inside canvas'''
    dummy_frame = tk.Frame(canvas)
    # 1st argument is the position of the center of the window
    canvas.create_window((650, 945), window=dummy_frame, width=728)

    # Dynamic frames
    for _ in range(10):
        f = tk.Frame(dummy_frame, height=100, bd=2, relief="sunken", background="#7FB77E")
        f.pack(side="top", anchor="nw", fill="x")
        frames.append(f)

    # ===== BOTTOM FRAME TO PUT PROGRESS BAR & NEXT BUTTON =====
    bottom_bar = tk.Frame(root, background="#2F6B3F")
    bottom_bar.pack(side="bottom", fill="x")

    # Progress bar
    progress = ttk.Progressbar(bottom_bar, orient="horizontal", mode="indeterminate")
    progress.pack(side="bottom", anchor="w", fill="x")

    # Next button
    tk.Button(bottom_bar, text="Next", background="#4C5C2D", foreground="white", command=start_next_news)\
        .pack(side="bottom", anchor="e")

# ================= CORE LOGIC =================

def start_load_news(category):
    search_entry.delete(0, tk.END)
    dummy_root.focus()
    '''Above two lines are features that deletes all contents of search bar and removes the cursor of it
    Whenever a category/refresh is chosen'''

    threading.Thread(target=load_news, args=(category,)).start() #Starts new thread for every category

def load_news(category):
    global articles, index

    set_loading(True)

    data = get_top_news(category)

    if not data:
        messagebox.showerror("Error", "Failed to fetch news")
        set_loading(False)
        return

    articles = data["articles"]
    index = 0

    render_news()
    set_loading(False)


def start_search():
    query = search_entry.get()
    threading.Thread(target=search, args=(query,)).start() #Starts new thread for every search query

def search(query):
    global articles, index

    set_loading(True)

    data = search_news(query)

    if not data:
        messagebox.showerror("Error", "Search failed")
        set_loading(False)
        return

    articles = data["articles"]
    index = 0

    render_news()
    set_loading(False)


def start_next_news():
    threading.Thread(target=next_news).start() #Starts new thread when next button is pressed

def next_news():
    global index

    set_loading(True)

    index += 10

    if index >= len(articles):
        messagebox.showinfo("Info", "No more news")
        index = 0

    render_news()
    set_loading(False)


def render_news():
    #Main function that put everything in its place

    for f in frames:
        for widget in f.winfo_children():
            widget.destroy()

    for i, f in enumerate(frames):
        if index + i >= len(articles):
            break

        article = articles[index + i]

        #Building a canvas area first to put relative images; order of creating child widget is important
        right_can = tk.Canvas(f, width=200, height=150, background="#FFF6C0")
        right_can.pack(side="right")

        tk.Message(
            f,
            text=article["title"],
            font=('Calisto MT', 14),aspect=500,justify='center',foreground="#091413", background="#7FB77E").pack(pady=25)

        # BUTTON FRAME
        btn_frame = tk.Frame(f, background="#7FB77E")
        btn_frame.pack(side="right",anchor= "sw")

        tk.Button(
            btn_frame,
            text="Open",
            background="#F7C85C",
            command=lambda url=article["url"]: webbrowser.open(url)
        ).pack(side="right", padx=2)

        is_saved = is_bookmarked(article) #Determines the colour of bookmark based on saved library
        bm = tk.Button(
            btn_frame,
            text="Bookmark",
            bg="green" if is_saved else "#F7C85C"
        )
        bm.config(command=lambda a=article, b=bm: on_bookmark_click(a, b))
        bm.pack(side="right", padx=2)

        img_path = fetch_and_cache_image(article.get("urlToImage"), i)
        try:
            img = Image.open(img_path)
            right_can.image = ImageTk.PhotoImage(img)
            right_can.create_image((100, 80), image=right_can.image)
        except:
            right_can.create_text(
                            (100, 80), text="Image unavailable", fill="red")

def on_bookmark_click(article, button):
    new_state = toggle_bookmark(article)

    # Update button color instantly
    if new_state:
        button.config(bg="green")
    else:
        button.config(bg="#F7C85C")

# ===== LOADING OF PROGRESSBAR ======

def set_loading(state):
    if state:
        progress.pack(side="bottom", anchor="w", fill="x")
        progress.start()
    else:
        progress.stop()
        progress.pack_forget() # Removes the progress bar when done

def open_bookmarks_window():
    # Bookmark window
    
    win = tk.Toplevel()
    win.title("Bookmarks")
    win.geometry("550x500+325+140")

    bookmarks = load_bookmarks()

    canvas = tk.Canvas(win)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(win, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    container = tk.Frame(canvas)
    canvas.create_window((0, 0), window=container, anchor="nw")

    container.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # ===== No bookmarks case =====
    if not bookmarks:
        tk.Label(container, text="No bookmarks yet").pack(pady=20)
        return

    # ===== Render bookmarks =====
    for article in bookmarks:
        frame = tk.Frame(container, bd=1, relief="solid")
        frame.pack(fill="x", padx=5, pady=5)

        # Title
        tk.Label(
            frame,
            text=article["title"],
            wraplength=500,
            justify="left"
        ).pack(anchor="w", padx=5, pady=5)

        # Buttons row
        btn_frame = tk.Frame(frame)
        btn_frame.pack(anchor="w", padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="Open",
            command=lambda url=article["url"]: webbrowser.open(url)
        ).pack(side="left", padx=2)

        tk.Button(
            btn_frame,
            text="Remove",
            command=lambda a=article, f=frame: remove_bookmark_ui(a, f)
        ).pack(side="left", padx=2)
        
def remove_bookmark_ui(article, frame):
    from utils import load_bookmarks, save_all_bookmarks

    data = load_bookmarks()
    data = [item for item in data if item["url"] != article["url"]]
    save_all_bookmarks(data)

    frame.destroy()  # remove from UI instantly