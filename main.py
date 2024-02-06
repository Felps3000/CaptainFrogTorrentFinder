from tkinter import *
import tkinter as tk
from tkinter import ttk
from torrent_search import *
from PIL import ImageTk, Image
from concurrent import futures

handlers = []


# daqui https://github.com/NatanaelAntonioli/CaptainFrogTorrentFinder/pull/4
def thread_clicked():  # Avoid Tkinter freeze
    thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)
    thread_pool_executor.submit(clicked)


def clicked():
    progressbar.tkraise()
    progressbar.place(x=16, y=155, width=652, height=10)
    progressbar.start(15)
    inp = inputtxt.get()
    global handlers
    handlers = listar_torrents(inp)
    listbox.delete(0, END)
    for i in range(len(handlers)):
        listbox.insert(END, str(handlers[i][2]) + " | " + str(handlers[i][0]))
        listbox.focus_set()
        listbox.select_set(0)
    progressbar.stop()
    progressbar.place_forget()

    # scrollbar pra listbox daqui https://github.com/NatanaelAntonioli/CaptainFrogTorrentFinder/pull/8
    if listbox.size() > 20:
        scrollbar.place(x=749, y=191, height=320)


def listbox_clicked(event):
    cs = listbox.curselection()
    for list in cs:
        os.startfile(handlers[list][1])


global_offset = 130
x_offset_adjust = 23

# Define a janela
window = Tk()
window.resizable(0, 0)
window.title("Captain Frog's Torrent Finder")
window.geometry('782x580')
window.configure(bg='#264653')
bgcolor = "#264653"

style = ttk.Style()
# Set the theme to "clam"
style.theme_use("clam")
# Configure the Horizontal.TProgressbar style in "clam" theme
style.configure("Horizontal.TProgressbar",
                background="#2a9d8f",
                troughcolor="#e9c46a",
                bordercolor="#e9c46a",
                lightcolor="#2a9d8f",
                darkcolor="#2a9d8f")
# Configure the Vertical.TProgressbar style in "clam" theme

progressbar = ttk.Progressbar(window, length=200, orient="horizontal", mode="indeterminate")

# Define o termo de busca
titulo_buscar = Label(window, text="insert search term",
                      bg=bgcolor,
                      fg="white",
                      font=('Bebas Neue', 20))
titulo_buscar.place(x=12, y=123, in_=window)

# Define o campo onde recebemos o input
inputtxt = Entry(window,
                 width=50,
                 bg="#E9C46A",
                 fg="#2A9D8F",
                 bd=0,
                 insertbackground="#2A9D8F",
                 selectbackground="#2a9d8f",
                 selectforeground="#e9c46a",
                 borderwidth=0,
                 highlightthickness=0,
                 font=("Bebas Neue", 18)
                 )
inputtxt.place(x=16, y=160, in_=window)
inputtxt.bind('<Return>', lambda event: thread_clicked())
inputtxt.focus_set()


def popup(event):

    try:
        window.clipboard_get()  # Get the copied item from system clipboard
        menu.entryconfig("Paste", state="active")
    except tk.TclError:
        menu.entryconfig("Paste", state="disabled")

    try:
        inp = inputtxt.get()  # Get the text inside entry widget
        ls = listbox.get(0)
        if not inp:
            menu.entryconfig("Copy", state="disabled")
            menu.entryconfig("Cut", state="disabled")
            menu.entryconfig("Clear", state="disabled")
            if not ls:
                menu.entryconfig("Clear list", state="disabled")
            else:
                menu.entryconfig("Clear list", state="active")
            menu.tk_popup(event.x_root, event.y_root)  # Pop the menu up in the given coordinates
        else:
            menu.entryconfig("Copy", state="active")
            menu.entryconfig("Cut", state="active")
            menu.entryconfig("Clear", state="active")
            if not ls:
                menu.entryconfig("Clear list", state="disabled")
            else:
                menu.entryconfig("Clear list", state="active")
            menu.tk_popup(event.x_root, event.y_root)  # Pop the menu up in the given coordinates
    finally:
        menu.grab_release()  # Release it once an option is selected


def paste():
    clipboard = window.clipboard_get()  # Get the copied item from system clipboard
    inputtxt.insert('end', clipboard)  # Insert the item into the entry widget
 

def copy():
    inp = inputtxt.get()  # Get the text inside entry widget
    if not inp:
        return None
    else:
        window.clipboard_clear()  # Clear the tkinter clipboard
        window.clipboard_append(inp)  # Append to system clipboard


def cut():
    inp = inputtxt.get()  # Get the text inside entry widget
    if not inp:
        return None
    else:
        window.clipboard_clear()  # Clear the tkinter clipboard
        window.clipboard_append(inp)  # Append to system clipboard
        inputtxt.delete(0, END)


def clear():
    inputtxt.delete(0, END)


def clearls():
    listbox.delete(0, END)
    scrollbar.place_forget()


menu = Menu(window,
            tearoff=0,
            activebackground="#264653",
            activeforeground="#e9c46a",
            )  # Create a menu
menu.add_command(label='Copy', command=copy)  # Create labels and commands
menu.add_command(label='Paste', command=paste)
menu.add_command(label='Cut', command=cut)
menu.add_separator()
menu.add_command(label='Clear', command=clear)
menu.add_separator()
menu.add_command(label='Clear list', command=clearls)

inputtxt.bind('<Button-3>', popup)  # Bind a func to right click

# Define o botão
btn = Button(window, text="search",
             bg='#E76F51',
             fg='#E9C46A',
             bd=0,
             width=10,
             font=('Bebas Neue', 13),
             activebackground="#E9C46A",
             activeforeground="#2A9D8F",
             command=thread_clicked)
btn.place(x=647 + x_offset_adjust, y=30 + global_offset, in_=window)

canvas_1 = tk.Canvas(window,
                     width=750,
                     height=320,
                     bg="#2a9d8f",
                     highlightthickness=0,
                     relief=FLAT)
canvas_1.place(x=16, y=191)

# Define a listbox
listbox = Listbox(window,
                  height=20,
                  width=124,
                  bg="#2A9D8F",
                  fg="white",
                  borderwidth=0,
                  highlightthickness=0,
                  bd=0,
                  highlightcolor="#2A9D8F",
                  highlightbackground="#E9C46A",
                  selectforeground="#2A9D8F",
                  selectbackground="#E9C46A",
                  activestyle="none"
                  )
listbox.place(x=20, y=61 + global_offset, in_=window)
listbox.bind('<Double-1>', listbox_clicked)
listbox.bind('<Return>', listbox_clicked)

# Define a scrollbar da listbox
scrollbar = Scrollbar(window, orient='vertical')
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

# Define a imagem do sapo
frame = Frame(window, width=20, height=10)
frame.pack()
frame.place(x=10 + x_offset_adjust, y=45)
img = ImageTk.PhotoImage(Image.open("sapo.png"))
image = Label(frame, image=img, bg=bgcolor)
image.pack()

# Define o título
titulo_sapo = Label(window, text="Captain Frog's Torrent Finder", fg="white", bg=bgcolor)
titulo_sapo.place(x=140 + x_offset_adjust, y=60, in_=window)
titulo_sapo.config(font=("Bebas Neue", 30))

# Define o subtítulo

xx = 16
yy = 515

subtitulo_2 = Label(window, text="M - Main results, probably in good health.", fg="white", bg=bgcolor)
subtitulo_2.place(x=xx, y=yy, in_=window)

subtitulo_3 = Label(window, text="S - Secondary results, could be in good health but probably aren't.", fg="white",bg=bgcolor)
subtitulo_3.place(x=xx, y=yy + 20, in_=window)

window.mainloop()
