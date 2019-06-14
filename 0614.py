from tkinter import *

def pressed(X):

    frames[X].tkraise()

window = Tk()
frame0 = Frame(window)
frame0.grid(row=0,column=0)
frames=[]
for i in range (2):
    Button(frame0,text="Frame"+str(i),command=lambda X=i: pressed(X)).pack(side=LEFT)
    frames.append(Frame(window))
    frames[i].grid(row=1,column=0)
    label = Label(frames[i],text="FRAME"+str(i),width=10,height=10)
    label.pack()



window.mainloop()