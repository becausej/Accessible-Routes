# This is a sample Python script.
import sys
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from sqlite3 import *
import logging
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
input_file = "input.csv"


if os.path.isfile("data.db"):
    os.remove("data.db")


conn = connect("data.db")
curs = conn.cursor()
cmd = "create table test(floor text, room text primary key, room_type text, door_coordinate text, acc_door text, in_acc text, room_name text, building_name text, tags text)"
curs.execute(cmd)
conn.close()
conn = connect("data.db")
curs = conn.cursor()
textfile = open(input_file)
lines = textfile.readlines()
for line in lines:
    x = line.split(',')
    cmd2 ="insert into test values('{floor:s}','{rn:s}','{rt:s}','{dc:s}','{ad:s}','{ia:s}','{rna:s}','{bn:s}','{tg:s}')"
    cmd2 = cmd2.format(floor = x[0], rn = x[1],rt =x[2],dc=(x[3] +',' + x[4]),ad=x[5],ia=x[6],rna=x[7],bn=x[8],tg=x[9])
    curs.execute(cmd2)
conn.commit()

def display():
    conn2 = None
    try:
        conn2 = connect("data.db")
        cursor = conn2.cursor()
        db2 = "select * from test"
        cursor.execute(db2)
        tv = treeview
        fetchdata = tv.get_children()
        for elements in fetchdata:
            tv.delete(elements)
        data = cursor.fetchall()
        for d in data:
            tv.insert("", END, values=d)
        conn2.commit()
    except Exception as e:
        showerror("Database Error")
        logging.exception(e)
        conn2.rollback()
    finally:
        if conn2 is not None:
            conn2.close()

def show():
    ws_ent.delete(0, END)
    ws_ent.focus()
    treeview.selection()
    display()

def reset():
    show()

def search():
    treeview.selection()
    fetchdata = treeview.get_children()
    for f in fetchdata:
        treeview.delete(f)
    conn2 = None
    try:
        conn2 = connect("data.db")
        core = conn2.cursor()
        db2 = "select * from test WHERE instr(lower(room), lower('%s')) > 0"
        name = ws_ent.get()
        if '\'' in name:
            index = name.find('\'')
            name = name[0:index] + '\'' + name[index:]
        core.execute(db2 % name)
        data = core.fetchall()
        for d in data:
            treeview.insert("", END, values=d)

    except Exception as e:
        showerror("Search Error")
        logging.exception(e)

    finally:
        if conn2 is not None:
            conn2.close()

ws = Tk()
ws.title("TFT Stats")
# width = ws.winfo_screenwidth() - ws.winfo_width()
# height = ws.winfo_screenheight() - ws.winfo_height()
# ws.geometry('+%d+%d' % (width/2, height/2))
ws.geometry("+150+50")
ws.resizable(False, False)



style = ttk.Style()
style.theme_use("default")
style.map("Treeview")
overall_frame = Frame(ws)
overall_frame.pack(side=TOP)
treeview = ttk.Treeview(overall_frame, columns=("floor","rn","rt","dc","ad","ia","rna","bn","tg"), show='headings', height=22)
treeview.pack(side=TOP)
treeview.heading('floor', text="Floor", anchor=CENTER)  # could west anchor these
treeview.column("floor", stretch=False, width=70)
treeview.heading('rn', text="Room Number", anchor=CENTER)
treeview.column("rn", stretch=False, width=70)
treeview.heading('rt', text="Room Type", anchor=CENTER)
treeview.column("rt", stretch=False, width=70)
treeview.heading('dc', text="Door Coordinates", anchor=CENTER)
treeview.column("dc", stretch=False, width=90)
treeview.heading('ad', text="Accessible Door", anchor=CENTER)
treeview.column("ad", stretch=False, width=100)
treeview.heading('ia', text="Inside Accessibility", anchor=CENTER)
treeview.column("ia", stretch=False, width=100)
treeview.heading('rna', text="Room Name", anchor=CENTER)
treeview.column("rna", stretch=False, width=70)
treeview.heading('bn', text="Building Name", anchor=CENTER)
treeview.column("bn", stretch=False, width=90)
treeview.heading('tg', text="Tags", anchor=CENTER)
treeview.column("tg", stretch=False, width=70)
frame_low = Frame(ws)
frame_low.pack(side=BOTTOM)
ws_ent = Entry(frame_low, width=20, font=('Arial', 15, 'bold'))
ws_ent.pack(side=TOP)
last_frame = Frame(frame_low)
last_frame.pack(side=BOTTOM)
ws_btn1 = Button(last_frame, text='Search', width=11, font=('calibri', 12, 'normal'), command=search)
ws_btn1.pack(side=LEFT, pady=(0, 5), padx=(0, 5))
ws_btn2 = Button(last_frame, text='Reset', width=11, font=('calibri', 12, 'normal'), command=reset)
ws_btn2.pack(side=RIGHT, pady=(0, 5), padx=(5, 0))

show()
ws.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
