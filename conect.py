import psycopg2
import tkinter as tk
from configparser import ConfigParser

#TKINTER SETUP
def kinter():
    global root
    root = tk.Tk()
    global canvas1
    canvas1 = tk.Canvas(root,width = 500,height = 500)
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
def join_str(tuple_of_string):
    global text
    text = []
    for i in range(len(tuple_of_string)):
        text.append(''.join(tuple_of_string[i]))
    
    
def join_int(tuple_of_string):
    global text
    text = []
    for i in range(len(tuple_of_string)):
        text.append(''.join(str(y) for y in tuple_of_string[i]))

def name():
    sql = 'SELECT username FROM public.users'
    cur.execute(sql)
    global res
    res = cur.fetchall();
    
def rights(name):
    sql = '''SELECT rights FROM public.users where username = '%s' '''
    global rig
    cur.execute(sql % name)
    rig = cur.fetchall();

def print_x(var):
    for i in range(len(var)):
        print(var[i])

def ch_rights(name,value):
    sql = """ UPDATE public.users SET rights = %s WHERE username = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()

#tkinter object
kinter()
root.title("course editor")
cal=['Hunter Course','Extra Course','Premium Course','Assist Course','N Course',
     'Hiden Course','Support Course','N boost Course']
val=[4,8,64,256,1073742336,1024,2048,4096]
l = tk.Label(root, bg='white', width=20, text='empty')
l.pack()

#tkinter function
def calc():
    global intend
    intend = 2 + var0.get()+ var1.get()+ var2.get()+ var3.get()+ var4.get()+ var5.get()+ var6.get()+ var7.get()
    l.config(text= str(intend))

def search():
     global inp
     inp = latex.get(1.0, "end-1c")
     setup()
     rights(inp)
     join_int(rig)
     t2 = tk.Label(root,text=str(text) , fg='red',font=('helvetica',10,'bold'))
     canvas1.create_window(300,200,window=t2)
def setval():
    ch_rights(inp,intend)
    rights(inp)
    join_int(rig)
    t3 = tk.Label(root,text=str(text) , fg='green',font=('helvetica',10,'bold'))
    canvas1.create_window(300,450,window=t3)

#calculator value
for i in range(len(cal)):
    exec(f'''var{i} = tk.IntVar()''')
    exec(f'''label{i} = tk.Checkbutton(root, text=cal[i] ,variable=var{i}, onvalue=val[i], offvalue=0, command=calc) ''')
    exec(f'''canvas1.create_window(100,50+i*50,window=label{i})''')

#test       
t1 = tk.Label(root,text='Search Username' , fg='blue',font=('helvetica',12,'bold'))
canvas1.create_window(300,50,window=t1)
latex = tk.Text(root, height = 1, width = 20)
canvas1.create_window(300,100,window=latex)
button1 = tk.Button(text='Search',command=search,bg='brown',fg='white')
canvas1.create_window(300,150,window=button1)
button2 = tk.Button(text='Set Value',command=setval,bg='brown',fg='white')
canvas1.create_window(300,400,window=button2)
