from tkinter import *
from tkinter import font

Tk = Tk()
Tk.geometry('800x500+750+200')
DataList = []

def IninTopText():
    TempFont = font.Font(Tk, size=30, weight='bold', family='Malgun Gothic')
    MainText = Label(Tk, font=TempFont, text="지진 대피소 검색")
    MainText.pack()
    MainText.place(x=20)

def InitInputSi():
    global InputLabel
    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    SiLabel = Label(Tk, font=TempFont, text="시 / 도")
    SiLabel.pack()
    SiLabel.place(x=50, y=70)
    InputLabel = Entry(Tk, font=TempFont, width=10, borderwidth=10, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=20, y=100)

def InitInputGu():
    global InputLabel
    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    GuLabel = Label(Tk, font=TempFont, text="구")
    GuLabel.pack()
    GuLabel.place(x=230, y=70)
    InputLabel = Entry(Tk, font=TempFont, width=10, borderwidth=10, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=180, y=100)

def InitSearchButton():
    TempFont = font.Font(Tk, size=12, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='검 색', command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)

def InitSearchDangerPButton():
    TempFont = font.Font(Tk, size=12, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='근처 지진 취약교량 검색', command=SearchDangerPButtonAction)
    SearchButton.pack()
    SearchButton.place(x=10, y=160)

def InitSearchDisasterMsgButton():
    TempFont = font.Font(Tk, size=11, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='현재 장소의 재난알림 검색', command=SearchDisasterMsgButtonAction)
    SearchButton.pack()
    SearchButton.place(x=10, y=200)

    Label1 = Label(Tk, font=TempFont, text="시설명")
    Label1.pack()
    Label1.place(x=50, y=235)

    Label2 = Label(Tk, font=TempFont, text="상세주소")
    Label2.pack()
    Label2.place(x=235, y=235)

def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = SearchListBox.curselection()[0]
    if iSearchIndex == 0:
        SearchLibrary()

def SearchLibrary():
    import http.client

def SearchDangerPButtonAction():
    pass

def SearchDisasterMsgButtonAction():
    pass

def InitRenderText():
    global RenderText
    TempFont = font.Font(Tk, size=10, family='Malgun Gothic')

    RenderTextScrollbar = Scrollbar(Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=245)
    RenderText = Text(Tk, width=55, height=17, borderwidth=5, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=260)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')

IninTopText()
InitInputSi()
InitInputGu()
InitSearchButton()
InitSearchDangerPButton()
InitSearchDisasterMsgButton()
InitRenderText()
Tk.mainloop()