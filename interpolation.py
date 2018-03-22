# coding: utf-8

import calculations
from Tkinter import *

N = 600  # ширина графика
p = []   # массив точек
q = []   # массив значений


def str_equat(coef):
    """
    создает строку с записью полученной функции,
    форматирует числа до 4 знака после запятой
    """
    n = len(coef)
    rez = 'уравнение: \n y = '
    if n == 2:
        rez += str(format(coef[0], '0.4f')) + 'x'
    else:
        if coef[0]:
            rez += str(format(coef[0], '0.4f')) + 'x^' + str(n - 1)
        for j in xrange(1, n - 2):
            if j % 4 == 0:
                rez += '\n'
            if coef[j] > 0:
                rez += ' + ' + str(format(coef[j], '0.4f')) + 'x^' + str(n - j - 1)
            elif coef[j] < 0:
                rez += ' - ' + str(format(-coef[j], '0.4f')) + 'x^' + str(n - j - 1)
        if coef[-2] > 0:
            rez += ' + ' + str(format(coef[-2], '0.4f')) + 'x'
        elif coef[-2] < 0:
            rez += ' - ' + str(format(-coef[-2], '0.4f')) + 'x'
    if coef[-1] > 0:
        rez += ' + ' + str(format(coef[-1], '0.4f'))
    elif coef[-1] < 0:
        rez += ' - ' + str(format(-coef[-1], '0.4f'))
    return rez


def record(event):
    """
    рисует точку на графике и записывает ее координаты при вводе вручную
    """
    global p, q
    ev_x = event.x
    ev_y = event.y
    p.append(1. * ev_x / 2 - N / 4)
    q.append(N / 4 - 1. * ev_y / 2)
    element = canv.create_rectangle(ev_x - 2,ev_y - 2,ev_x + 2,ev_y + 2,fill='red')
    canv.addtag_withtag('els', element)


def count_f(x, n, mass):
    """
    считает координаты точек полученной функции
    """
    x_ = x / 2 - N / 4
    y_ = 0
    for j in xrange(n):
        y_ += mass[j] * (x_ ** (n - j - 1))
    y = N / 2 - 2 * y_
    return y


def interpolate():
    """
    интерполирует заданные точки,
    по возможности - многочленом заданной степени
    """
    global p, q
    if len(p) > 1:
        if box.curselection():               # проверка на выбор степени многочлена, переменная deg равна количеству
            deg = box.curselection()[0] + 1  # коэффициентов многочлена, то есть, ширине матрицы
        else:                                # при отсутствии выбора желаемой степени deg = 1, в таком случае
            deg = 1                          # ищется многочлен степени не больше, чем количество заданных точек
        mass = calculations.coef(p, q, deg)
        if mass:
            rez = str_equat(mass)
            n = len(mass)
            y = count_f(0, n, mass)
            for i in xrange(1, N - 9):  # рисование кривой на графике
                new_y = count_f(i, n, mass)
                elem = canv.create_line(i - 1, y, i, new_y)
                canv.addtag_withtag('els', elem)
                y = new_y
        else:
            rez = 'Ну зачем вы ввели две разных точки с одной координатой по х?'
    else:
        rez = 'Введите хотя бы две точки'

    result.configure(text=rez)


def clear():
    """
    сбрасывает заданные точки, очищает экран
    """
    global p, q
    p = []
    q = []
    result.configure(text='')
    canv.delete('els')
    entry_x.delete(0, 50)
    entry_y.delete(0, 50)


def read_entry():
    """
    записывает координаты точки, введенные вручную
    отмечает точку на графике
    """
    global p, q
    x = float(entry_x.get())
    y = float(entry_y.get())
    p.append(x)
    q.append(y)
    ev_x = 2 * x + N / 2
    ev_y = N / 2 - 2 * y
    element = canv.create_rectangle(ev_x - 2, ev_y - 2, ev_x + 2, ev_y + 2, fill='red')
    canv.addtag_withtag('els', element)


def axes():
    """
    создает разметку, координатные оси
    """
    canv.create_line(0, N / 2, N, N / 2, arrow=LAST)
    canv.create_line(N / 2, N, N / 2, 0, arrow=LAST)
    for i in xrange(20, N, 20):
        if i != N / 2:
            canv.create_line(i, 0, i, N, fill='lightgrey')
            canv.create_line(0, i, N, i, fill='lightgrey')
            canv.create_line(i, N / 2 - 3, i, N / 2 + 3)
            canv.create_line(N / 2 - 3, i, N / 2 + 3, i)
            canv.create_text(i + 2, N / 2 + 10, text=str(i / 2 - N / 4), font='Verdana 5')
            canv.create_text(N / 2 + 10, i + 2, text=str(N / 4 - i / 2), font='Verdana 5')


root = Tk()
root.title('интерполяция')
frame = Frame(root)
frame.pack()

canv = Canvas(frame, width=N, height=N, bg='white')  # создает холст для графика
axes()
canv.grid(row=4, column=0, columnspan=6)
task = Label(frame, width=40, text='Отметьте точки на графике для интерполяции \n или введите их '
                                                'координаты (x, y) \n в поля слева. Также можете выбрать \n '
                                                'желаемую степень уравнения n')  # область с информацией
task.grid(row=0, column=2, rowspan=3)
result = Label(frame, width=90) # область для вывода результата
result.grid(row=3, column=0, columnspan=6)
check_button = Button(frame, text='интерполировать', command=interpolate, width=20)  # кнопка, запускающая интерполяцию
check_button.grid(row=1, column=3, columnspan=3)
clear_button = Button(frame, text='очистить', command=clear, width=20)  # кнопка сброса настроек
clear_button.grid(row=2, column=3, columnspan=3)
label_x = Label(frame, width=2, text='x:')
label_x.grid(row=0, column=0)
label_y = Label(frame, width=2, text='y:')
label_y.grid(row=1, column=0)
entry_x = Entry(frame, width=17)  # ввод координаты точки по оси Ох
entry_x.grid(row=0, column=1)
entry_y = Entry(frame, width=17)  # ввод координаты точки по оси Оy
entry_y.grid(row=1, column=1)
xy_button = Button(frame, text='отметить точку', command=read_entry, width=18)  # кнопка подтверждения ввода координат
xy_button.grid(row=2, column=0, columnspan=2)
label_deg = Label(frame, width=2, text='n:')
label_deg.grid(row=0, column=3)
box = Listbox(frame, selectmode=SINGLE, height=1, width=17)  # список для выбора степени
box.insert(END, 'не выбрано')
for x in xrange(1, 41):
    box.insert(END, x)
box.grid(row=0, column=4)
scr = Scrollbar(frame, command=box.yview, bg='black', width=9)
box.configure(yscrollcommand=scr.set)
scr.grid(row=0, column=5)
canv.bind("<Button-1>", record)  # привязка нажатия мыши

root.mainloop()
