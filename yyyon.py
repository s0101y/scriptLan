#파이참 커밋
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.tix import ComboBox

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
    global InputGu
    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    GuLabel = Label(Tk, font=TempFont, text="구")
    GuLabel.pack()
    GuLabel.place(x=230, y=70)
    InputGu = Entry(Tk, font=TempFont, width=10, borderwidth=10, relief='ridge')
    InputGu.pack()
    InputGu.place(x=180, y=100)

def InitSearchButton():
    TempFont = font.Font(Tk, size=12, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='검 색', command=ButtonClick)
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

def ButtonClick():
    import http.client
    import urllib
    global DataList
    global data


    server = "api.data.go.kr"
    conn = http.client.HTTPConnection(server)
    DataList = Combobox1.get() + " " + InputGu.get()
    hangul_utf8 = urllib.parse.quote(DataList)

    print(DataList)
    conn.request("GET",
                 "/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=" + hangul_utf8)
    # http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
    req = conn.getresponse()

   # DataList.clear()

    if req.status == 200:

        data = req.read().decode('utf-8')
        from xml.etree import ElementTree
        RenderText.insert(INSERT, data)
        tree = ElementTree.fromstring(data)
        itemElements = tree.getiterator("item")

        for item in itemElements:
            ShelterName = item.find("clnsShuntFcltyNm")
            ShelterAdr = item.find("rdnmadr")
            if len(ShelterName.text) > 0:
                return [ShelterName.text, ShelterAdr.text]  # 사전형식 반환

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
    RenderText = Text(Tk, width=100, height=17, borderwidth=5, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=260)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
   # RenderText.configure(state='disabled')
   # RenderText.insert(INSERT,data)


IninTopText()
InitInputSi()
InitInputGu()
InitSearchButton()
InitSearchDangerPButton()
InitSearchDisasterMsgButton()
InitRenderText()
Tk.mainloop()