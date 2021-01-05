from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib as mpl
import japanize_matplotlib
import csv

import tkinter as tk
import tkinter.ttk as ttk
from functools import partial


# プロットをする関数
def plot_wave(day_data):

    # Figureインスタンスを生成する。
    fig = plt.Figure()

    # 目盛を内側にする。
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # Axesを作り、グラフの上下左右に目盛線を付ける。
    ax1 = fig.add_subplot(111)
    ax1.yaxis.set_ticks_position('both')
    ax1.xaxis.set_ticks_position('both')

    # 軸のラベルを設定する。
    ax1.yaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    ax1.xaxis.set_major_locator(mpl.ticker.MultipleLocator(2))
    ax1.set_xticklabels([0,"6時","7時","8時","9時","10時","11時","12時","13時","14時", "15時","16時","17時","18時","19時","20時","21時","22時","23時","24時"])

    ax1.set_xlim(0,36)
    ax1.grid()


    # データをプロットする。
    color_list=["r", "g", "b", "c", "m", "y"]
    air_list=[0]
    for i in range(len(day_data)):
        air_list.append("飛行機"+str(day_data[i][0]))
        num = 0
        for flight in range(int((len(day_data[i])-1)/4)):
            place=[]
            y=[]
            place.append(day_data[i][num+1])
            place.append(day_data[i][num+3])
            y_value = float(day_data[i][num+2]) - 6.0
            y_sum = int(y_value*2)
            y.append(y_sum)
            y_value = float(day_data[i][num+4]) - 6.0
            y_sum = int(y_value*2)
            y.append(y_sum)
            num+=4

            x=np.array(y)
            y=np.array([i for ii in range(len(y))])

            ax1.set_yticklabels(air_list)
            ax1.plot(x, y, color=color_list[int(day_data[i][0])-1],linewidth=5)
            label=str(place[0])+"→"+str(place[1])
            ax1.text(x[0], i+0.1, label, size=8)

    return fig

def button1(event,tab,list, exit):

    value = tab.get()
    children = event.winfo_children()
    for child in children:
        child.destroy()
    value = value.replace("日","")
    fig = plot_wave(list[int(value)-1])
    canvas = FigureCanvasTkAgg(fig, event)
    canvas.get_tk_widget().grid(row=1, column=0)

def main(master):

    # Windowの設定
    root = master
#     root.title("Plot window")
#     root.geometry()
#     root.geometry("1000x500")


    # csvの読み込み
    month_data = []
    num=0
    with open('month1.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                month_data.append(row)
    num=0
    nb = ttk.Notebook(root)
    day_data=[]
    data = []
    flag = False
    days_data = []
    #test.pyの出力結果読み込み
    while True:
        while True:
            if flag == False:
                days_data.append(month_data[num])
                flag = True
                num+=1
                continue

            if month_data[num][0] != "/" and not num>int(len(month_data)):
                day_data.append(month_data[num])
                num+=1
            else:
                flag = False
                data.append(day_data)
                day_data=[]
                num+=1
                break
        if num==int(len(month_data)):
            break


    frame = ttk.Frame(root)
    frame.pack()
    frame1 = ttk.Frame(root)
    frame1.pack()

    v = StringVar()
    s = ""
    box_word = ["".join(days_data[i])+"日" for i in range(len(days_data))]
    cb = ttk.Combobox(
            frame, textvariable=v,
            values=box_word, width=10)
    cb.grid(row=1, column=0, padx=5, pady=5)
    cb.bind(
            '<<ComboboxSelected>>',
            partial(button1,frame1 ,v, data))

    root.mainloop()

def createNewWindow():
        root = Tk()
        sub_win = Toplevel(root)
        sub_win.title("modal dialog")
        sub_win.geometry("300x300")
        paramdialog = StringVar()
        label = ttk.Label(sub_win,text="input param")
        label.pack()
        entry = ttk.Entry(sub_win,textvariable=paramdialog)
        entry.pack()
        button = ttk.Button(sub_win,text="open",command = print(paramdialog.get()))
        button.pack()
#         test.main(2020,10)

if __name__ == "__main__":
    main("test")