import csv
import tkinter.messagebox as messagebox
from tkinter import *
import tkinter.ttk as ttk
from csvview import CSVView
import os
import result
import test

class EntrySampleGetValue(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.entry1 = StringVar()
        self.entry2 = StringVar()
        self.entry3 = StringVar()
        self.entry4 = StringVar()
        self.entry5 = StringVar()
        self.entry6 = StringVar()
        self.year = StringVar()
        self.month = StringVar()
        frame = ttk.Frame(master)
        frame.pack()
        button1 = ttk.Button(
            frame,
            text='OK', command=self.createWidgets)
        button1.grid()
        self.root = ""
        self.pack()

    def createWidgets(self):
        self.root = Tk()
        self.root.geometry("300x500")
        label7 = ttk.Label(self.root,text="作成する年")
        label7.pack()
        self.entry7 = ttk.Entry(self.root,textvariable = self.year)
        self.entry7.pack()
        label8 = ttk.Label(self.root,text="作成する月")
        label8.pack()
        self.entry8 = ttk.Entry(self.root,textvariable = self.month)
        self.entry8.pack()
        label1 = ttk.Label(self.root,text="飛行機1の飛行距離")
        label1.pack()
        self.entry1 = ttk.Entry(self.root,textvariable = self.entry1)
        self.entry1.pack()
        label2 = ttk.Label(self.root,text="飛行機2の飛行距離")
        label2.pack()
        self.entry2 = ttk.Entry(self.root,textvariable = self.entry2)
        self.entry2.pack()
        label3 = ttk.Label(self.root,text="飛行機3の飛行距離")
        label3.pack()
        self.entry3 = ttk.Entry(self.root,textvariable = self.entry3)
        self.entry3.pack()
        label4 = ttk.Label(self.root,text="飛行機4の飛行距離")
        label4.pack()
        self.entry4 = ttk.Entry(self.root,textvariable = self.entry4)
        self.entry4.pack()
        label5 = ttk.Label(self.root,text="飛行機5の飛行距離")
        label5.pack()
        self.entry5 = ttk.Entry(self.root,textvariable = self.entry5)
        self.entry5.pack()
        label6 = ttk.Label(self.root,text="飛行機6の飛行距離")
        label6.pack()
        self.entry6 = ttk.Entry(self.root,textvariable = self.entry6)
        self.entry6.pack()

        button = ttk.Button(self.root,text="ok",command=self.getEntryText)
        button.pack()

    def getEntryText(self):
        print(self.month.get())
        test.main(2020,10,self.entry1.get(),self.entry2.get(),self.entry3.get(),self.entry4.get(),self.entry5.get(),self.entry6.get())
        result.main(self)
        self.root.destroy()

class CSVLogic:
    """
    csvViewer読み込み、書き込みロジック
    """

    def __init__(self):
        """
        列とレコード用の配列を初期化
        """
        self.header =[]
        self.data =[]

    def readCsv(self,data_path):
        """
        csvを読み込んで内部にデータを反映する
        1行目を列名、他の行をデータとして取得する
        """
        ret = True
        header = []
        data =[]
        try :
            with open(data_path, "r",newline="") as csv_file:
                f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)
                header = next(f)
                print(header)
                for row in f:
                    data.append(row)
        except IOError as e:
            print(e)
            ret = False
        self.header = header
        self.data = data
        return ret

    def writeCsv(self,data_path,columns,rows):
        """
        与えられた列名リストとレコードリストを書きだす
        """
        ret = True
        csv_file = open(data_path, "w",newline="")
        try:
            with open(data_path, 'w') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                writer.writerow(columns)
                writer.writerows(rows)
        except IOError as e:
            print(e)
            ret = False
        return ret
    def getHeader(self):
        return self.header
    def getData(self):
        return self.data


class CSVControl:
    """
    csvViewerのコントローラー
    """

    def __init__(self):
        """
        アプリの立ち上げとイベント登録
        """

        master = Tk()
        master.title("flight_schedule_maker")
        master.geometry("1300x1300")
        self.filePath = StringVar()
        self.view = CSVView(master)
        self.logic = CSVLogic()
        self.view.setReadButtonCommand(self.readButtonCommand)
        frame = ttk.Frame(master)
        frame.pack()
        EntrySampleGetValue(master)
#         self.pack()
        master.mainloop()


    def readButtonCommand(self):
        """
        csv読み込みボタン用コマンド
        csvから取得した列名、データをViewに反映する。
        csvが変更されるごとにRowDataフレームがリロードされるので、
        保存ボタンコマンドも再設定
        """

        columns,datas = self.readCsv()
        self.view.setNewColumnAndData(columns,datas)
        self.view.setSaveButtonCommand(self.saveButtonCommand)

    def saveButtonCommand(self):
        """
        保存ボタン用コマンド
        指定されたパスにviewで指定された情報をcsv形式で書きだす
        """
        file_path = self.view.getFilePath()
        columns = self.view.getColumns()
        rows =self.view.getRows()
        ret = self.logic.writeCsv(file_path,columns,rows)
        if ret:
            messagebox.showinfo("writecsv","succeed")
        else:
            messagebox.showerror("writecsv","failed")

    def readCsv(self):
        """
        csv読み込んで列名とデータを返却
        """
        ret = False
        file_path = self.view.getFilePath()
        if os.path.exists(file_path) :
            ret = self.logic.readCsv(file_path)
        if ret:
            messagebox.showinfo("readcsv","succeed")
        else:
            messagebox.showerror("readcsv","failed")
        return self.logic.getHeader(),self.logic.getData()

if __name__ == '__main__':
    control =  CSVControl()
    # control.readCsv()