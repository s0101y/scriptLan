from tkinter import *
from tkinter import font
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
import http.client
import urllib
from xml.etree import ElementTree
import folium
import spam
import webbrowser
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

Tk = Tk()
Tk.title("지진 대피소 검색")

Tk.geometry('800x500+750+200')
photo = PhotoImage(file="shel.png")
Label(Tk, image=photo, height=50, width=50).place(x=20, y=30)
DataList = []


def InitTopText():
    TempFont = font.Font(Tk, size=30, weight='bold', family='Malgun Gothic')
    MainText = Label(Tk, font=TempFont, text="지진 대피소 검색")
    MainText.pack()
    MainText.place(x=100, y=25)

def InitInputSi():
    global Combobox1
    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    SiLabel = Label(Tk, font=TempFont, text="시 / 도 :")
    SiLabel.pack()
    SiLabel.place(x=80, y=120)
    Combobox1 = ttk.Combobox(font=TempFont, textvariable=str, width=10)
    Combobox1['value'] = ("서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원도", "충청북도", "충청남도",
                          "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도")    #종류
    Combobox1.current(0)    #시작지점
    Combobox1.pack()
    Combobox1.place(x=180, y=120)

def InitInputGu():
    global InputLabel
    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    GuLabel = Label(Tk, font=TempFont, text="구 :")
    GuLabel.pack()
    GuLabel.place(x=350, y=120)
    InputLabel = Entry(Tk, font=TempFont, width=15, borderwidth=5, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=400, y=120)

def InitSearchButton():
    TempFont = font.Font(Tk, size=20, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='검 색', command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=600, y=100)

def InitSearchMapButton():
    TempFont = font.Font(Tk, size=15, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='현재 지역 대피소 위치 보기', bg='green', command=SearchMapButtonAction)
    SearchButton.pack()
    SearchButton.place(x=500, y=250)

def SearchMapButtonAction():

    global MAP, Mname
    MAP = []
    Mname = []
    server = "api.data.go.kr"
    conn = http.client.HTTPConnection(server)
    hangul_utf8 = urllib.parse.quote(Combobox1.get() + " " + InputLabel.get())
    conn.request("GET","/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=" + hangul_utf8)
    req = conn.getresponse()
    if int(req.status) == 200:
        strXml = req.read()
    else:
        print("failed!")

    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("item")  # item 엘리먼트 리스트 추출

    for item in itemElements:
        name = item.find("clnsShuntFcltyNm")  # clnsShuntFcltyNm 검색
        longitude = item.find("latitude")  # latitude 검색
        latitude = item.find("hardness")  # hardness 검색

        if len(name.text) > 0:  # 검색된 결과가 있다면
            Mname.append([name.text])  # 하나의 구호소 이름 리스트 Mname에 append

        if len(latitude.text) > 0:  # 검색된 결과가 있다면
            MAP.append([longitude.text, latitude.text])  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 MAP에 append

    for a in range(len(MAP)):
        MAP[a] = [float(x) for x in MAP[a]]

    Mname = sum(Mname, [])
    map_osm = folium.Map(location=MAP[10], zoom_start=15)     # 위도 경도 지정

    for a in range(len(MAP)):
        folium.Marker(MAP[a], popup=Mname[a]).add_to(map_osm)     # 마커 지정

    map_osm.save('now.html')     # html 파일로 저장
    webbrowser.open('now.html')

def SearchButtonAction():

    TempFont = font.Font(Tk, size=15, family='Malgun Gothic')
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    if spam.strlen(InputLabel.get()) <= 0:
        Label(Tk, font=TempFont, text="구를 입력해주세요.", fg='red').place(x=400, y=80)
    else:
        Label(Tk, font=TempFont, text="                          ", fg='red').place(x=400, y=80)
        SearchLibrary()
    RenderText.configure(state='disabled')

def InitSearchDangerPButton():
    TempFont = font.Font(Tk, size=15, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='근처 지진 취약시설 보기', bg='red',command=SearchDangerPButtonAction)
    SearchButton.pack()
    SearchButton.place(x=515, y=330)

def InitSearchHowManyButton():
    TempFont = font.Font(Tk, size=15, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='현재 지역 대피소\n 수용인원 현황 보기', bg='blue',command=SearchHowManyButtonAction)
    SearchButton.pack()
    SearchButton.place(x=535, y=400)

def SearchHowManyButtonAction():
    server = "api.data.go.kr"
    conn = http.client.HTTPConnection(server)
    hangul_utf8 = urllib.parse.quote(Combobox1.get() + " " + InputLabel.get())
    conn.request("GET","/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=" + hangul_utf8)

    req = conn.getresponse()
    if int(req.status) == 200:
        strXml = req.read()
    else:
        print("failed!")

    howmany = []
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("item")  # item 엘리먼트 리스트 추출

    for item in itemElements:
        acceptNum = item.find("aceptncPosblCo")  # aceptncPosblCo 검색
        if len(acceptNum.text) > 0:  # 검색된 결과가 있다면
            howmany.append([acceptNum.text])  # 수용인원

    for a in range(len(howmany)):
        howmany[a] = [int(x) for x in howmany[a]]

    howmany = sum(howmany, [])
    Count = [0, 0, 0, 0, 0]

    for a in range(len(howmany)):
        if howmany[a] <= 500:
            Count[0] += 1
    for a in range(len(howmany)):
        if (howmany[a] <= 1000 and howmany[a] > 500):
            Count[1] += 1
    for a in range(len(howmany)):
        if (howmany[a] <= 5000 and howmany[a] > 1000):
            Count[2] += 1
    for a in range(len(howmany)):
        if (howmany[a] <= 10000 and howmany[a] > 5000):
            Count[3] += 1
    for a in range(len(howmany)):
        if (howmany[a] <= 20000 and howmany[a] > 10000):
            Count[4] += 1

    window1 = Toplevel(Tk)
    window1.title("대피소 수용 인원 비율 현황")

    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

    fig1 = plt.figure(2)
    plt.title('대피소 수용 인원 비율', fontsize=16)
    b = ["500명 이하 수용가능", "1000명 이하 수용가능", "5000명 이하 수용가능", "10000명 이하 수용가능", "20000명 이상 수용가능"]
    plt.pie(Count, labels=b, shadow=True, autopct='%1.1f%%')

    canvas = FigureCanvasTkAgg(fig1, master=window1)
    plot_widget = canvas.get_tk_widget()

    plot_widget.grid(row=0, column=0)

def InitSearchDisasterMsgButton():
    TempFont = font.Font(Tk, size=11, weight='bold', family='Malgun Gothic')
    SearchButton = Button(Tk, font=TempFont, text='재난알림 보내기', command=MailSubmit)
    SearchButton.pack()
    SearchButton.place(x=610, y=185)

    global InputEmail
    InputEmail = Entry(Tk, font=TempFont, width=50, borderwidth=3, relief='ridge')
    InputEmail.pack()
    InputEmail.place(x=140, y=190)

    EmailLabel = Label(Tk, font=TempFont, text="이메일주소 입력:")
    EmailLabel.pack()
    EmailLabel.place(x=20, y=190)



    Label1 = Label(Tk, font=TempFont, text="시설명")
    Label1.pack()
    Label1.place(x=60, y=235)

    Label2 = Label(Tk, font=TempFont, text="상세주소")
    Label2.pack()
    Label2.place(x=290, y=235)


def SearchLibrary():

    global TEXT
    TEXT = []

    server = "api.data.go.kr"
    conn = http.client.HTTPConnection(server)
    hangul_utf8 = urllib.parse.quote(Combobox1.get() + " " + InputLabel.get())
    conn.request("GET","/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=" + hangul_utf8)
    # http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
    req = conn.getresponse()
    print(req.status)
    if int(req.status) == 200:
        strXml = req.read()
    else:
        print("failed!")

    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("item")     # item 엘리먼트 리스트 추출

    for item in itemElements:
        name = item.find("clnsShuntFcltyNm")  # clnsShuntFcltyNm 검색
        adr = item.find("rdnmadr")  # rdnmadr 검색
        if len(adr.text) > 0:  # 검색된 결과가 있다면
            TEXT.append((name.text, adr.text))  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 TEXT에 append

    for i in range(len(TEXT)):  # RenderText에 삽입
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i + 1)
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, TEXT[i][0])
        RenderText.insert(INSERT, " | ")
        RenderText.insert(INSERT, TEXT[i][1])
        RenderText.insert(INSERT, "\n\n")


def MailSubmit():
    conn = http.client.HTTPConnection("apis.data.go.kr")
    conn.request("GET",
                 "/1741000/DisasterMsg2/getDisasterMsgList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=10&type=xml&flag=Y")
    req = conn.getresponse()
    print(req.status, req.reason)
    #print(req.read().decode('utf-8'))
    strXml = req.read().decode('utf-8')
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("msg")  # msg 엘리먼트 리스트 추출


    text = ""
    for data in itemElements:
        text += (data.text+"\n")

    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # TLS 보안 시작
    s.starttls()
    # 로그인 인증
    s.login('sakha1004@gmail.com', 'ereegbpmapsrihsz')
    # 보낼 메시지 설정
    msg = MIMEText(text)
    msg['Subject'] = '제목 : 재난알림.'

    # 메일 보내기
    s.sendmail("sakha1004@gmail.com",InputEmail.get() , msg.as_string())

    # 세션 종료
    s.quit()


def SearchDangerPButtonAction():
    window = Toplevel(Tk)
    window.title("근처 지진 취약 시설")

    server = "apis.data.go.kr"
    conn = http.client.HTTPConnection(server)
    hangul_utf8 = urllib.parse.quote(Combobox1.get() + " " + InputLabel.get())
    conn.request("GET",
                 "/B552016/OldFacilService/getFacil30YearsOldList?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&numOfRows=20&pageNo=1&type=xml&facilAddr=" + hangul_utf8)
    # http://api.data.go.kr/openapi/clns-shunt-fclty-std?serviceKey=pRhsehsqTxKvRoWsJyn%2FALMmqPMUBhRax3KRNAG%2BUQVKM5NBbWpWapjs1BVntARUSUhLvdXkCHzeiXjOh0HmCQ%3D%3D&pageNo=1&numOfRows=100&type=xml&insttNm=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%B6%81%EA%B5%AC
    req = conn.getresponse()
    print(req.status)
    if int(req.status) == 200:
        strXml = req.read()
    else:
        print("failed!")

    Grade = []
    Mname = []
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.getiterator("item")  # item 엘리먼트 리스트 추출

    for item in itemElements:
        name = item.find("facilNm")  # clnsShuntFcltyNm 검색
        grade = item.find("sfGrade")

        if len(name.text) > 0:  # 검색된 결과가 있다면
            Mname.append(name.text)  # 하나의 구호소 이름
            Grade.append(grade.text)  # 하나의 구호소 이름과 주소를 튜플 타입으로 묶어 리스트 TEXT에 append

    # Dmap.save('dangerMap.html')  # html 파일로 저장
    # webbrowser.open('dangerMap.html')
    GradeN = ['A등급', 'B등급', 'C등급', 'D등급']
    gCount = [0, 0, 0, 0]

    for a in range(len(Grade)):
        if Grade[a] == 'A등급':
            gCount[0] += 1
    for a in range(len(Grade)):
        if Grade[a] == 'B등급':
            gCount[1] += 1
    for a in range(len(Grade)):
        if Grade[a] == 'C등급':
            gCount[2] += 1
    for a in range(len(Grade)):
        if Grade[a] == 'D등급':
            gCount[3] += 1

    from matplotlib import font_manager, rc
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)

    fig = plt.figure(1)
    xs = [i for i, _ in enumerate(GradeN)]
    plt.bar(xs, gCount)
    plt.ylabel("건물 개수")
    plt.title("노후건물 안전등급 현황")
    plt.xticks([i for i, _ in enumerate(GradeN)], GradeN)

    canvas = FigureCanvasTkAgg(fig, master=window)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=0)



def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=245)
    RenderText = Text(Tk, width=65, height=17, borderwidth=5, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=260)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)
    RenderText.configure(state='disabled')

InitTopText()
InitInputSi()
InitInputGu()
InitSearchButton()
InitSearchMapButton()
InitSearchDangerPButton()
InitSearchDisasterMsgButton()
InitRenderText()
InitSearchHowManyButton()
Tk.mainloop()