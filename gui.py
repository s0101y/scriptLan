#파이참 커밋
from tkinter import *
from tkinter import font
from tkinter import ttk



Tk = Tk()
Tk.geometry('800x500+750+200')
DataList = []

def IninTopText():
    TempFont = font.Font(Tk, size=30, weight='bold', family='Malgun Gothic')
    MainText = Label(Tk, font=TempFont, text="지진 대피소 검색")
    MainText.pack()
    MainText.place(x=20)

def InitInputSi():

    global Combobox1

    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    SiLabel = Label(Tk, font=TempFont, text="시 / 도")
    SiLabel.pack()
    SiLabel.place(x=50, y=70)
    #InputLabel = Entry(Tk, font=TempFont, width=10, borderwidth=10, relief='ridge')
    #InputLabel.pack()
    #InputLabel.place(x=20, y=100)

    Combobox1 = ttk.Combobox(font=TempFont, textvariable=str, width=10)
    Combobox1['value'] = ("서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원도", "충청북도", "충청남도",
                          "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도")    #종류
    Combobox1.current(0)    #시작지점
    Combobox1.pack()
    Combobox1.place(x=20, y=110)

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

def SearchButtonAction():

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    SearchLibrary()
    RenderText.configure(state='disabled')


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


def SearchLibrary():
    import http.client
    import urllib
    from xml.etree import ElementTree
    global TEXT
    TEXT = []
    server = "api.data.go.kr"
    conn = http.client.HTTPConnection(server)
    hangul_utf8 = urllib.parse.quote(Combobox1.get() + " " + InputLabel.get())
    conn.request("GET",
                 "/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=" + hangul_utf8)
    # http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
    req = conn.getresponse()
    print(req.status)
    if int(req.status) == 200:
        strXml = req.read()
    else:
        print("failed!")

    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("item")  # item 엘리먼트 리스트 추출

    for item in itemElements:
        name = item.find("clnsShuntFcltyNm")  # clnsShuntFcltyNm 검색
        adr = item.find("rdnmadr")              # rdnmadr 검색
        if len(adr.text) > 0:
            TEXT.append((name.text, adr.text))

    for i in range(len(TEXT)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i + 1)
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, TEXT[i][0])
        RenderText.insert(INSERT, " | ")
        RenderText.insert(INSERT, TEXT[i][1])
        RenderText.insert(INSERT, "\n\n")


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