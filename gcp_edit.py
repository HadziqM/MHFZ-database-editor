import psycopg2
import tkinter as tk
from configparser import ConfigParser

#TKINTER SETUP
def kinter():
    global root
    root = tk.Tk()
    global canvas1
    canvas1 = tk.Canvas(root,width = 300,height = 300)
    canvas1.pack()

#POSTGRAS SETUP
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
def setup():
    global conn
    param = config()
    conn = psycopg2.connect(**param)
		
    # create a cursor
    global cur
    cur = conn.cursor()

# Call Funnction
def join_int(tuple_of_string):
    global numb
    numb = []
    for i in range(len(tuple_of_string)):
        numb.append(''.join(str(y) for y in tuple_of_string[i]))
def join_str(tuple_of_string):
    global text
    text = []
    for i in range(len(tuple_of_string)):
        text.append(''.join(tuple_of_string[i]))

def name():
    sql = 'SELECT name FROM public.characters WHERE gcp IS NOT NULL'
    cur.execute(sql)
    global res
    res = cur.fetchall();

def gcp_all():
    sql = 'SELECT gcp FROM public.characters WHERE gcp IS NOT NULL'
    cur.execute(sql)
    global gec
    gec = cur.fetchall();
    
def gcp(name):
    sql = '''SELECT gcp FROM public.characters where name = '%s' '''
    global rig
    cur.execute(sql % name)
    rig = cur.fetchall();

def ch_gcp(name,value):
    sql = """ UPDATE public.characters SET gcp = %s WHERE name = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()

#tkinter function
def start():
    setup()
    l.config(text="connected to database")
    
def scanall():
    state[0]=1
    state[1]=0
    name()
    gcp_all()
    a = len(res)
    l.config(text ="scanned "+str(a)+" not null characters")
    join_str(res)
    join_int(gec)

def search():
    state[0]=0
    state[1]=1
    global inp
    inp = latex.get(1.0, "end-1c")
    gcp(inp)
    join_int(rig)
    if (len(numb)==0):
        l.config(text="name not found, its case sensitive")
    else:
        l.config(text="found "+inp+" with "+str(numb[0])+" gcp")

def setall():
    if (state[0]==1):
        ber = latexx.get(1.0, "end-1c")
        a = int(ber)
        for i in range(len(text)):
            ch_gcp(text[i],a)
        l.config(text="set all success")
    else:
        l.config(text="subject isnt scanned yet")
def addall():
    if (state[0]==1):
        ber = latexx.get(1.0, "end-1c")
        a = int(ber)
        for i in range(len(text)):
            numb[i] = a +int(numb[i])
            ch_gcp(text[i],numb[i])
        l.config(text="add all success")
    else:
        l.config(text="subject isnt scanned yet")
def setind():
    if (state[1]==1):
        ber = latexx.get(1.0, "end-1c")
        a = int(ber)
        ch_gcp(inp,a)
        l.config(text="set specific success")
    else:
        l.config(text="subject isnt scanned yet")
        
#state error
state=[0,0]

#TK action
kinter()
root.title("gcp editor")
l = tk.Label(root, bg='black',fg='white', width=30, text='empty')
l.pack()
#text and button
latex = tk.Text(root, height=1, width = 20)
canvas1.create_window(150,100,window=latex)
latexx = tk.Text(root,height=1, width = 20)
canvas1.create_window(150,200,window=latexx)
button1 = tk.Button(text='Connect',command=start,bg='green',fg='white')
canvas1.create_window(150,50,window=button1)
button2 = tk.Button(text='Scan all',command=scanall,bg='blue',fg='white')
canvas1.create_window(100,130,window=button2)
button3 = tk.Button(text='Search',command=search,bg='blue',fg='white')
canvas1.create_window(200,130,window=button3)
button4 = tk.Button(text='Set individual',command=setind,bg='brown',fg='white')
canvas1.create_window(75,230,window=button4)
button5 = tk.Button(text='Set all',command=setall,bg='brown',fg='white')
canvas1.create_window(150,230,window=button5)
button6 = tk.Button(text='add all',command=addall,bg='brown',fg='white')
canvas1.create_window(210,230,window=button6)

#end
root.mainloop()
