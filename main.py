from tkinter import *
from torrent_search import *
from PIL import ImageTk, Image
from concurrent import futures

handlers = []

# from here https://github.com/NatanaelAntonioli/CaptainFrogTorrentFinder/pull/4/commits
def thread_clicked(): #Avoid Tkinter freeze
    thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)
    thread_pool_executor.submit(clicked)

def clicked():
    inp = inputtxt.get()
    global handlers
    handlers = listar_torrents(inp)
    listbox.delete(0, END)
    for i in range(len(handlers)):
        listbox.insert(END, str(handlers[i][2]) + " | " + str(handlers[i][0]))
        listbox.focus_set()

# scrollbar pra listbox daqui https://github.com/NatanaelAntonioli/CaptainFrogTorrentFinder/pull/8
    if (listbox.size()>22):
            scrollbar.place(x=749, y=191, height=320)

def listbox_clicked():
    cs = listbox.curselection()
    for list in cs:
        os.startfile(handlers[list][1])

global_offset = 130
x_offset_adjust = 23

# Define a janela
window = Tk()
window.resizable(0, 0)
window.title("Captain Frog's Torrent Finder")
window.geometry('782x630')
window.configure(bg='#264653')
bgcolor = "#264653"

# Define o termo de busca
titulo_buscar = Label(window, text="insert search term",
                      bg=bgcolor,
                      fg="white",
                      font=('Bebas Neue', 20))
titulo_buscar.place(x=12, y=128, in_=window)

# Define o campo onde recebemos o input
inputtxt = Entry(window,
                 width=50,
                 bg="#E9C46A",
                 fg="#2A9D8F",
                 bd=0,
                 insertbackground="#2A9D8F",
                 borderwidth=0,
                 highlightthickness=0,
                 font=("Bebas Neue", 18)
                 )
inputtxt.place(x=16, y=160, in_=window)
inputtxt.bind('<Return>', lambda event: thread_clicked())
inputtxt.focus_set()

# Define o botão
btn = Button(window, text="search",
             bg='#E76F51',
             fg='#E9C46A',
             bd=0,
             width=10,
             font=('Bebas Neue', 13),
             command=thread_clicked)
btn.place(x=647 + x_offset_adjust, y=30 + global_offset, in_=window)

# Define a listbox
listbox = Listbox(window,
                  height=20,
                  width=125,
                  bg="#2A9D8F",
                  fg="white",
                  borderwidth=0,
                  highlightthickness=0,
                  bd=0,
                  highlightcolor="#E9C46A",
                  )
listbox.place(x=16, y=61 + global_offset, in_=window)
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
image = Label(frame, image=img, bg=bgcolor
              )
image.pack()

# Define o título
titulo_sapo = Label(window, text="Captain Frog's Torrent Finder", fg="white", bg=bgcolor)
titulo_sapo.place(x=140 + x_offset_adjust, y=60, in_=window)
titulo_sapo.config(font=("Bebas Neue", 30))

# Define o subtítulo

xx = 16
yy = 515

subtitulo_1 = Label(window, text="Please wait a few seconds to see results.", fg="white", bg=bgcolor)
subtitulo_1.place(x=xx, y=yy, in_=window)

subtitulo_2 = Label(window, text="M - Main results, probably in good health.", fg="white", bg=bgcolor)
subtitulo_2.place(x=xx, y=yy + 20, in_=window)

subtitulo_3 = Label(window, text="S - Secondary results, could be in good health but probably aren't.", fg="white",
                    bg=bgcolor)
subtitulo_3.place(x=xx, y=yy + 40, in_=window)

subtitulo_4 = Label(window, text="G - Google search results, useful for niche contents.", fg="white", bg=bgcolor)
subtitulo_4.place(x=xx, y=yy + 60, in_=window)

window.mainloop()
