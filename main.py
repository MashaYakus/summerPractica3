from tkinter import *
from tkinter import colorchooser, messagebox
from tkinter.ttk import Radiobutton
from PIL import Image, ImageDraw, ImageTk
import os
import random

brushSize = 5
brushColor = "black"
brushColor0 = brushColor

w = 450
h = 350

def draw(event):
    global brushColor
    global brushSize
    x1, y1 = (event.x - brushSize / 2), (event.y - brushSize/2)
    x2, y2 = (event.x + brushSize/2), (event.y + brushSize/2)
    canvas.create_oval(x1, y1, x2, y2, fill=brushColor, outline=brushColor)
    draw_image.ellipse((x1, y1, x2, y2), fill=brushColor, outline=brushColor)


def chooseColor():
    global brushColor
    global brushColor0
    (rgb, hx) = colorchooser.askcolor()
    if r_var.get() == 0:
        brushColor = hx
        colorSpace['bg'] = hx
    else:
        brushColor0 = hx
        colorSpace['bg'] = hx

def select(value):
    global brushSize
    brushSize = int(value)


def chooseBrush():
    global brushColor
    global brushColor0
    if r_var.get() == 0:
        brushColor = brushColor0
    else:
        brushColor0 = brushColor
        brushColor = 'white'

# _____Функции файла ___________________

def saveImg():
    filename = f'{txt.get()}.png'
    image.save(filename)
    messagebox.showinfo('Сохранение', 'Сохранено под именем %s' % filename)

def loadImg():
    global image, img, draw_image
    filename = f'{txt.get()}.png'
    image = Image.open(filename)
    img = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=img)
    draw_image = ImageDraw.Draw(image)

#________Работа с канвасом____________

def fillCanvas():
    global brushColor
    canvas.delete('all')
    #(rgb, hx) = colorchooser.askcolor()
    canvas['bg'] = brushColor
    draw_image.rectangle((0, 0, w, h), width=0, fill=brushColor)


def clearCanvas():
    canvas.delete('all')
    canvas['bg'] = 'white'
    draw_image.rectangle((0, 0, w, h), width=0, fill='white')

# _____Функции фотоэффекта для меню ___________________


def saveLoad():
    global image, img, draw_image
    filename = "crutch.png"
    image.save(filename)
    image = Image.open(filename)
    img = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=img)
    draw_image = ImageDraw.Draw(image)
    os.remove(filename)

def negImage():
    global image, img, draw_image
    pix = image.load()
    for i in range(w):
        for j in range(h):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            draw_image.point((i, j), (255 - a, 255 - b, 255 - c))
    saveLoad()

def bwImage():
    global image, img, draw_image
    factor = 50
    pix = image.load()
    for i in range(w):
        for j in range(h):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = a + b + c
            if (S > (((255 + factor) // 2) * 3)):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw_image.point((i, j), (a, b, c))
    saveLoad()

def greyImage():
    global image, img, draw_image
    pix = image.load()
    for i in range(w):
        for j in range(h):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw_image.point((i, j), (S, S, S))
    saveLoad()

def noiseImage():
    global image, img, draw_image
    factor = 100
    pix = image.load()
    for i in range(w):
        for j in range(h):
            rand = random.randint(-factor, factor)
            a = pix[i, j][0] + rand
            b = pix[i, j][1] + rand
            c = pix[i, j][2] + rand
            if (a < 0):
                a = 0
            if (b < 0):
                b = 0
            if (c < 0):
                c = 0
            if (a > 255):
                a = 255
            if (b > 255):
                b = 255
            if (c > 255):
                c = 255
            draw_image.point((i, j), (a, b, c))
    saveLoad()

# _____Функции фигур для меню ___________________
def noneFigure(event):
    canvas.create_polygon(0, 0, 0, 0, 0, 0)


def squareFunction():
    canvas.bind("<B1-Motion>", noneFigure)
    canvas.bind("<ButtonPress-1>", sqCreate)


def circleFunction():
    canvas.bind("<B1-Motion>", noneFigure)
    canvas.bind("<ButtonPress-1>", circCreate)


def triangleFunction():
    canvas.bind("<B1-Motion>", noneFigure)
    canvas.bind("<ButtonPress-1>", triCreate)


def noneFigureFunction():
    canvas.bind("<ButtonPress-1>", noneFigure)
    canvas.bind('<ButtonRelease-1>', noneFigure)
    canvas.bind("<B1-Motion>", draw)


# _________Новые фигуры______________________________________________

x = None
y = None

fill_color = "black"
outline_color_line = "black"
width_maintainer = 2


def sq(event):
    global x, y
    canvas.create_rectangle(x, y, event.x, event.y, fill=brushColor, width=0)
    draw_image.polygon((x, y, x, event.y, event.x, event.y, event.x, y), fill=brushColor)


def sqCreate(event):
    global x, y
    x = event.x
    y = event.y
    canvas.bind('<ButtonRelease-1>', sq)


def circ(event):
    global x, y
    canvas.create_oval(x, y, event.x, event.y, fill = brushColor, width=0)
    draw_image.ellipse((x, y, event.x, event.y), fill=brushColor)


def circCreate(event):
    global x, y
    x = event.x
    y = event.y
    canvas.bind('<ButtonRelease-1>', circ)


def tri(event):
    global x, y
    canvas.create_polygon(x, event.y, event.x, event.y, (x + event.x) / 2, (y+event.y) / 2, fill = brushColor, width=0)
    draw_image.polygon((x, event.y, event.x, event.y, (x + event.x) / 2, (y+event.y) / 2), fill = brushColor)


def triCreate(event):
    global x, y
    x = event.x
    y = event.y
    canvas.bind('<ButtonRelease-1>', tri)

#________Функции линий для меню_____________

def lineFunction():
    canvas.bind("<B1-Motion>", noneFigure)
    canvas.bind("<ButtonPress-1>", lineCteate)


def dashLineFunction():
    canvas.bind("<B1-Motion>", noneFigure)
    canvas.bind("<ButtonPress-1>", dashLineCreate)

#_________Линии________________________

def line(event):
    global x, y
    canvas.create_line(x, y, event.x, event.y, width=width_maintainer, fill=fill_color)
    draw_image.line((x, y, event.x, event.y), width=width_maintainer, fill=fill_color)


def lineCteate(event):
    global x, y
    x = event.x
    y = event.y
    canvas.bind('<ButtonRelease-1>', line)

def dashLine(event):
    global x, y
    canvas.create_line(x, y, event.x, event.y, width=width_maintainer, fill=fill_color, dash=(10,5))
    draw_image.line((x, y, event.x, event.y), width=width_maintainer, fill=fill_color, dash=(10,5))

def dashLineCreate(event):
    global x, y
    x = event.x
    y = event.y
    canvas.bind('<ButtonRelease-1>', dashLine)


# ____________________Основная функция________________________________________________

window = Tk()
window.geometry('500x450')
#window.resizable(0,0)
window.title("PyPaint Саша&Маша")

canvas = Canvas(window,  width=w, height=h, bg='white')
canvas.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E + W + S + N)
canvas.columnconfigure(6, weight=1)
canvas.rowconfigure(2, weight=1)
canvas.bind("<B1-Motion>", draw)

image = Image.new('RGB', (w, h), 'white')
#w_image = image.size[0]
#h_image = image.size[1]
draw_image = ImageDraw.Draw(image)

lbl = Label(window, text="Название:", width=12)
lbl.grid(column=0, row=0)
txt = Entry(window, width=16)
txt.insert(0, "image_1")
txt.grid(column=1, row=0)
Button(window, text="Сохранить", width=8, command=saveImg).grid(row=1, column=0, padx=6)
Button(window, text="Загрузить", width=8, command=loadImg).grid(row=1, column=1, padx=6)

Button(window, text="Цвет", width=6, command=chooseColor).grid(row=0, column=2, padx=6)
colorSpace = Label(window, bg=brushColor, width=6)
colorSpace.grid(row=1, column=2, padx=6)

label_scale = Label(window, text="Толщина")
s_var = IntVar(value=5)
scale = Scale(window, variable=s_var, width=10, from_=1, to=100, orient=HORIZONTAL, command=select)
label_scale.grid(row=1, column=3)
scale.grid(row=0, column=3, padx=6)

r_var = BooleanVar()
r_var.set(bool(0))
rad1 = Radiobutton(window, text='Кисть', variable=r_var, value=0, command=chooseBrush)
rad2 = Radiobutton(window, text='Ластик', variable=r_var, value=1, command=chooseBrush)
rad1.grid(column=4, row=0)
rad2.grid(column=4, row=1)

mainMenu = Menu(window)
window.config(menu=mainMenu)

figureMenu = Menu(mainMenu, tearoff=0)
figureMenu.add_command(label="Прямая", command=lineFunction)
figureMenu.add_command(label="Прямоугольник", command=squareFunction)
figureMenu.add_command(label="Элипс", command=circleFunction)
figureMenu.add_command(label="Равнобедренный треугольник", command=triangleFunction)
figureMenu.add_command(label="Отменить создание фигур", command=noneFigureFunction)

mainMenu.add_cascade(label="Фигуры", menu=figureMenu)

fotoMenu = Menu(mainMenu, tearoff=0)
fotoMenu.add_command(label="Негатив", command=negImage)
fotoMenu.add_command(label="Черно-белое", command=bwImage)
fotoMenu.add_command(label="Оттеноки серого", command=greyImage)
#fotoMenu.add_command(label="Яркость")
fotoMenu.add_command(label="Создание шумов", command=noiseImage)
mainMenu.add_cascade(label="Фотоэффекты", menu=fotoMenu)

addMenu = Menu(mainMenu, tearoff=0)
addMenu.add_command(label="Заливка", command=fillCanvas)
addMenu.add_command(label="Очистить все", command=clearCanvas)
mainMenu.add_cascade(label="Дополнительные функции", menu=addMenu)


window.mainloop()




