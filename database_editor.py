import os
import psycopg2
import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk


#TKINTER SETUP
def kinter():
    global root
    global tab1
    global tab2
    global tab3
    global tab4
    global tab5
    global tab6
    global tab7
    root = tk.Tk()
    root.title("Database Edit")
    tabControl = ttk.Notebook(root,height=400,width=300,padding=10)
    
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab1 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)
    tab5 = ttk.Frame(tabControl)
    tab6 = ttk.Frame(tabControl)
    tab7 = ttk.Frame(tabControl)
  
    tabControl.add(tab2, text ='Course')
    tabControl.add(tab3, text ='GCP')
    tabControl.add(tab1, text ='Transmog')
    tabControl.add(tab4, text ='gacha')
    tabControl.add(tab5, text ='guild')
    tabControl.add(tab6, text ='login')
    tabControl.add(tab7, text ='road')
    tabControl.pack(expand = 2, fill ="both")
    
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
    for i in range(len(numb)):
        numb[i]=int(numb[i])
def join_str(tuple_of_string):
    global text
    text = []
    for i in range(len(tuple_of_string)):
        text.append(''.join(tuple_of_string[i]))

def gcp_name():
    sql = 'SELECT name FROM public.characters WHERE gcp IS NOT NULL'
    cur.execute(sql)
    global gcp_n
    gcp_n = cur.fetchall();

def gcp_all():
    sql = 'SELECT gcp FROM public.characters WHERE gcp IS NOT NULL'
    cur.execute(sql)
    global gcp_a
    gcp_a = cur.fetchall();
    
def gcp_search(name):
    sql = '''SELECT gcp FROM public.characters where name = '%s' '''
    global gcp_s
    cur.execute(sql % name)
    gcp_s = cur.fetchall();

def gcp_ch(name,value):
    sql = """ UPDATE public.characters SET gcp = %s WHERE name = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()
def rg_name():
    sql = 'SELECT username FROM public.users'
    cur.execute(sql)
    global rg_n
    rg_n = cur.fetchall();
    
def rg_search(name):
    sql = '''SELECT rights FROM public.users where username = '%s' '''
    global rg_s
    cur.execute(sql % name)
    rg_s = cur.fetchall();

def rg_ch(name,value):
    sql = """ UPDATE public.users SET rights = %s WHERE username = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()
def rg_ch_all(value):
    sql = """ UPDATE public.users SET rights = %s """
    cur.execute(sql % str(value))
    conn.commit()
def rg_def(value):
    sql="""ALTER TABLE public.users ALTER COLUMN rights SET DEFAULT %s """
    cur.execute(sql % str(value))
    conn.commit()
def tra_ind(name):
    sql = '''UPDATE characters SET skin_hist=pg_read_binary_file('%s') WHERE name= '%s' '''
    cur.execute(sql % (cwd,name))
    conn.commit()
def tra_all():
    sql = '''UPDATE characters SET skin_hist=pg_read_binary_file('%s') '''
    cur.execute(sql % cwd)
    conn.commit()
def prem_ind(name,value):
    sql = """ UPDATE public.characters SET gacha_prem = %s WHERE name = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()
def trial_ind(name,value):
    sql = """ UPDATE public.characters SET gacha_trial = %s WHERE name = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()
def prem_all(value):
    sql = """ UPDATE public.characters SET gacha_prem = %s """
    cur.execute(sql % str(value))
    conn.commit()
def trial_all(value):
    sql = """ UPDATE public.characters SET gacha_trial = %s """
    cur.execute(sql % str(value))
    conn.commit()
def guild_ind(name,value):
    sql = """ UPDATE public.guilds SET rank_rp = %s WHERE name = '%s' """
    cur.execute(sql % (str(value),name))
    conn.commit()
def guild_all(value):
    sql = """ UPDATE public.guilds SET rank_rp = %s"""
    cur.execute(sql % str(value))
    conn.commit()
def guild_name():
    sql = 'SELECT name FROM public.guilds'
    cur.execute(sql)
    global guild_n
    guild_n = cur.fetchall();
def log_id(name):
    sql = '''SELECT user_id FROM public.characters WHERE name='%s' '''
    cur.execute(sql % name)
    global log_i
    log_i  = cur.fetchall();
def log_tof(idn):
    sql = ''' UPDATE public.login_boost_state SET end_time = 0 WHERE char_id= %s '''
    cur.execute(sql % str(idn))
    conn.commit()
def log_ton(idn):
    log_tof(idn)
    sql = '''UPDATE public.login_boost_state SET week_count = 1 WHERE char_id= %s'''
    sql1= '''UPDATE public.login_boost_state SET available = true WHERE char_id= %s'''
    cur.execute(sql % str(idn))
    conn.commit()
    cur.execute(sql1 % str(idn))
    conn.commit()
def log_tof_all():
    sql = ''' UPDATE public.login_boost_state SET end_time = 0'''
    cur.execute(sql)
    conn.commit()
def log_ton_all():
    log_tof_all()
    sql = '''UPDATE public.login_boost_state SET week_count = 5 '''
    sql1= '''UPDATE public.login_boost_state SET available = true'''
    sql2= '''UPDATE public.login_boost_state SET end_time = 2000000 WHERE week_req = 5'''
    cur.execute(sql)
    cur.execute(sql1)
    cur.execute(sql2)
    conn.commit()
def road_up():
    sql = '''TRUNCATE TABLE public.normal_shop_items RESTART IDENTITY'''
    sql1='''COPY public.normal_shop_items FROM '%s' DELIMITER ',' CSV '''
    if ( cb_head.get()==1):
        sql1 = sql1 + '''HEADER'''
    cur.execute(sql)
    conn.commit()
    cur.execute(sql1 % cwe)
    conn.commit()
###tkinter function

#Tab 1    
def start():
    try:
        setup()
        l.config(text="connected to database")
    except (Exception, psycopg2.DatabaseError) as error:
        l.config(text=error)
def set_tra_ind():
    global inp3
    inp3 = latexxxx.get(1.0, "end-1c")
    gcp_name()
    join_str(gcp_n)
    a = 0
    for i in range(len(text)):
        if (text[i]==inp3):
            a = 1
    if (a==1):
        tra_ind(inp3)
        l.config(text='updating mog success')
    else:
        l.config(text='name not found')
    
def set_tra_all():
    tra_all()
    l.config(text='updating all mog success')
        
#Tab 2    
    
def search_rg():
    t_state[0]=2
    state2[0]=1
    global inp
    inp = latex.get(1.0, "end-1c")
    rg_search(inp)
    join_int(rg_s)
    if (len(numb)==0):
        l.config(text="name not found, its case sensitive")
    else:
        l.config(text="found "+inp+" with rights = "+str(numb[0]))
def set_rg_ind():
    if (t_state[0]==2):
        if (state2[0]==1):
            rg_ch(inp,intend)
            l.config(text="set specific success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
        
def set_rg_all():
    rg_ch_all(intend)
    l.config(text="set all success")

def set_rg_def():
    rg_def(intend)
    l.config(text="set dafault success")
       
#Tab 3
def scan_gcp():
    state3[0]=2
    t_state[0]=3
    gcp_name()
    gcp_all()
    a = len(gcp_a)
    l.config(text ="scanned "+str(a)+" not null characters")
    join_str(gcp_n)
    join_int(gcp_a)

def search_gcp():
    state3[0]=1
    t_state[0]=3
    global inp2
    inp2 = latexx.get(1.0, "end-1c")
    gcp_search(inp2)
    join_int(gcp_s)
    if (len(numb)==0):
        l.config(text="name not found, its case sensitive")
    else:
        l.config(text="found "+inp2+" with "+str(numb[0])+" gcp")

def set_gcp_all():
    if (t_state[0]==3):
        if (state3[0]==2):
            ber = latexxx.get(1.0, "end-1c")
            a = int(ber)
            for i in range(len(numb)):
                gcp_ch(text[i],a)
            l.config(text="set all success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
def add_gcp_all():
    if (t_state[0]==3):
        if (state3[0]==2):
            ber = latexxx.get(1.0, "end-1c")
            a = int(ber)
            for i in range(len(numb)):
                numb[i] = a +numb[i]
                gcp_ch(text[i],numb[i])
            l.config(text="add all success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
def sub_gcp_all():
    if (t_state[0]==3):
        if (state3[0]==2):
            ber = latexxx.get(1.0, "end-1c")
            a = int(ber)
            for i in range(len(numb)):
                numb[i] = numb[i]- a
                if (numb[i]<0):
                    numb[i]=0
                gcp_ch(text[i],numb[i])
            l.config(text="substract all success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
def set_gcp_ind():
    if (t_state[0]==3):
        if (state3[0]==1):
            ber = latexxx.get(1.0, "end-1c")
            a = int(ber)
            gcp_ch(inp,a)
            l.config(text="set specific success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
def add_gcp_ind():
    if (t_state[0]==3):
        if (state3[0]==1):
            ber = latexxx.get(1.0, "end-1c")
            a = int(ber)
            x = a + numb[0]
            gcp_ch(inp,x)
            l.config(text="add specific success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
def sub_gcp_ind():
    if (t_state[0]==3):
        if (state3[0]==1):
            ber = latexxx.get(1.0, "end-1c")
            a = int(ber)
            x = numb[0]-a
            if (x<0):
                x=0
            gcp_ch(inp,x)
            l.config(text="substract specific success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
#Tab 4
def set_prem_ind():
    ber = latex5.get(1.0, "end-1c")
    inp = latex4.get(1.0, "end-1c")
    if (ber!='' and inp!=''):
        a = int(ber)
        gcp_name()
        join_str(gcp_n)
        a = 0
        for i in range(len(text)):
            if (text[i]==inp):
                a = 1
        if (a==1):
            prem_ind(inp,ber)
            l.config(text='set gacha prem success')
        else:
            l.config(text='name not found')
    else:
        l.config(text='parameter not inserted yet')
def set_trial_ind():
    ber = latex5.get(1.0, "end-1c")
    inp = latex4.get(1.0, "end-1c")
    if (ber!='' and inp!=''):
        a = int(ber)
        gcp_name()
        join_str(gcp_n)
        a = 0
        for i in range(len(text)):
            if (text[i]==inp):
                a = 1
        if (a==1):
            trial_ind(inp,ber)
            l.config(text='set gacha trial success')
        else:
            l.config(text='name not found')
    else:
        l.config(text='parameter not inserted yet')
def set_prem_all():
    ber = latex5.get(1.0, "end-1c")
    if (ber!=''):
        a = int(ber)
        prem_all(ber)
        l.config(text='set gacha all prem success')
    else:
        l.config(text='parameter not inserted yet')
def set_trial_all():
    ber = latex5.get(1.0, "end-1c")
    if (ber!=''):
        a = int(ber)
        trial_all(ber)
        l.config(text='set gacha all trial success')
    else:
        l.config(text='parameter not inserted yet')
#Tab 5
def set_guild_ind():
    ber = latex7.get(1.0, "end-1c")
    inp = latex6.get(1.0, "end-1c")
    if (ber!='' and inp!=''):
        a = int(ber)
        guild_name()
        join_str(guild_n)
        a = 0
        for i in range(len(text)):
            if (text[i]==inp):
                a = 1
        if (a==1):
            guild_ind(inp,ber)
            l.config(text='set guild rp success')
        else:
            l.config(text='name not found')
    else:
        l.config(text='parameter not inserted yet')
def set_guild_all():
    ber = latex7.get(1.0, "end-1c")
    if (ber!=''):
        a = int(ber)
        guild_all(ber)
        l.config(text='set all guild rp success')
    else:
        l.config(text='parameter not inserted yet')
#Tab 6
def id_search():
    t_state[0]=6
    state6[0]=1
    global inp6
    inp6 = latex8.get(1.0, "end-1c")
    log_id(inp6)
    join_int(log_i)
    a = len(log_i)
    if (a==0):
        l.config(text='name not found')
    else :
        l.config(text=inp6+' found with id='+str(numb[0]))
def tof_log_ind():
    if (t_state[0]==6):
        if (state6[0]==1):
            log_tof(numb[0])
            l.config(text='turn off boost specific success')
        else:
            l.config(text='name not scanned yet')
    else:
        l.config(text='properties in wrong tab or not used yet')
def ton_log_ind():
    if (t_state[0]==6):
        if (state6[0]==1):
            log_ton(numb[0])
            l.config(text='make boost available specific success')
        else:
            l.config(text='name not scanned yet')
    else:
        l.config(text='properties in wrong tab or not used yet')
def tof_log_all():
    log_tof_all()
    l.config(text='turn off all boost success')
def ton_log_all():
    log_ton_all()
    l.config(text='make all boost available success')
    

#Tab 7

def up_road():
    road_up()
    l.config(text='road csv success')
    
#Error State
        
t_state = [0]
state2 = [0]
state3 = [0]
state6 = [0]

#Course Calculator aset

def calc():
    global intend
    intend = 2 + var0.get()+ var1.get()+ var2.get()+ var3.get()+ var4.get()+ var5.get()+ var6.get()+ var7.get()
    z.config(text= str(intend))
cal=['Hunter Course','Extra Course','Premium Course','Assist Course','N Course',
     'Hiden Course','Support Course','N boost Course']
val=[4,8,64,256,1073742336,1024,2048,4096]





####START CODE

kinter()
cwd = os.getcwd()
cwd = cwd + '\\skin_hist.bin'
cwe = os.getcwd() + '\\road\\road.csv'
###TKINTER OBJECT

cb_head = tk.IntVar()

##Root
#Button and Label
l = tk.Label(root, bg='black',fg='white', width=30, text='empty')
s_but = tk.Button(root,text="start",command=start,bg='green',fg='white',
                  height=1,width=10)
l1 = tk.Label(root,fg='red', text='Press Button Bellow First')
#Position
l1.pack()
s_but.pack()
l.pack()


##Tab 1
#button and label
tk.Label(tab1, text="character name",fg='blue').place(x=50,y=20)
latexxxx = tk.Text(tab1, height = 1, width = 20)
but1_ind=tk.Button(tab1,bg='red',fg='white',width=10,text='set specific',
                 command=set_tra_ind)
but1_all=tk.Button(tab1,bg='red',fg='white',width=10,text='set all',
                 command=set_tra_all)
#position
latexxxx.place(x=50,y=50)
but1_ind.place(x=50,y=80)
but1_all.place(x=50,y=110)
##Tab 2
tk.Label(tab2, text="username",fg='blue').place(x=50,y=20)
for i in range(len(cal)):
    exec(f'''var{i} = tk.IntVar()''')
    exec(f'''ck_but{i} = tk.Checkbutton(tab2, text=cal[i] ,variable=var{i}, onvalue=val[i], offvalue=0, command=calc) ''')
    exec(f'''ck_but{i}.place(x=10,y=200+i*20)''')
#Button and Label
z = tk.Label(tab2, bg='black',fg='white', width=10, text='empty')
latex = tk.Text(tab2, height = 1, width = 20)
but2_sc=tk.Button(tab2,bg='blue',fg='white',width=10,text='search',
                 command=search_rg)
but2_set=tk.Button(tab2,bg='red',fg='white',width=10,text='set specific',
                 command=set_rg_ind)
but2_all=tk.Button(tab2,bg='red',fg='white',width=10,text='set all',
                 command=set_rg_all)
but2_def=tk.Button(tab2,bg='red',fg='white',width=10,text='set default',
                 command=set_rg_def)
#position
z.place(x=150,y=300)
latex.place(x=50,y=50)
but2_sc.place(x=50,y=100)
but2_set.place(x=150,y=210)
but2_all.place(x=150,y=240)
but2_def.place(x=150,y=270)
##Tab 3
#Button and Label
tk.Label(tab3, text="character name",fg='blue').place(x=70,y=20)
tk.Label(tab3, text="gcp value",fg='blue').place(x=70,y=120)
latexx = tk.Text(tab3, height = 1, width = 20)
latexxx = tk.Text(tab3, height = 1, width = 20)
but3_sc=tk.Button(tab3,bg='blue',fg='white',width=10,text='search',
                 command=search_gcp)
but3_sc_a=tk.Button(tab3,bg='blue',fg='white',width=10,text='scan all',
                 command=scan_gcp)
but3_set=tk.Button(tab3,bg='red',fg='white',width=10,text='set specific',
                 command=set_gcp_ind)
but3_set_a=tk.Button(tab3,bg='red',fg='white',width=10,text='set all',
                 command=set_gcp_all)
but3_add=tk.Button(tab3,bg='red',fg='white',width=10,text='add specific',
                 command=add_gcp_ind)
but3_add_a=tk.Button(tab3,bg='red',fg='white',width=10,text='add all',
                 command=add_gcp_all)
but3_sub=tk.Button(tab3,bg='red',fg='white',width=10,text='sub specific',
                 command=sub_gcp_ind)
but3_sub_a=tk.Button(tab3,bg='red',fg='white',width=10,text='sub all',
                 command=sub_gcp_all)
#position
latexx.place(x=70,y=50)
latexxx.place(x=70,y=150)
but3_sc.place(x=40,y=80)
but3_sc_a.place(x=190,y=80)
but3_set.place(x=40,y=180)
but3_set_a.place(x=190,y=180)
but3_add.place(x=40,y=210)
but3_add_a.place(x=190,y=210)
but3_sub.place(x=40,y=240)
but3_sub_a.place(x=190,y=240)

##Tab 4
#Button and Label
tk.Label(tab4, text="character name",fg='blue').place(x=70,y=20)
tk.Label(tab4, text="coin value",fg='blue').place(x=70,y=70)
latex4 = tk.Text(tab4, height = 1, width = 20)
latex5 = tk.Text(tab4, height = 1, width = 20)
but4_prem=tk.Button(tab4,bg='red',fg='white',width=10,text='set spe prem',
                 command=set_prem_ind)
but4_prem_a=tk.Button(tab4,bg='red',fg='white',width=10,text='set all prem',
                 command=set_prem_all)
but4_trial=tk.Button(tab4,bg='red',fg='white',width=10,text='set spe trial',
                 command=set_trial_ind)
but4_trial_a=tk.Button(tab4,bg='red',fg='white',width=10,text='set all trial',
                 command=set_trial_all)
#position
latex4.place(x=70,y=50)
latex5.place(x=70,y=100)
but4_prem.place(x=40, y=130)
but4_prem_a.place(x=40,y=160)
but4_trial.place(x=190,y=130)
but4_trial_a.place(x=190,y=160)
##Tab 5
#buton and label
tk.Label(tab5, text="guild name",fg='blue').place(x=70,y=20)
tk.Label(tab5, text="rp value",fg='blue').place(x=70,y=70)
latex6=tk.Text(tab5, height = 1, width = 20)
latex7=tk.Text(tab5, height = 1, width = 20)
but5_guild=tk.Button(tab5,bg='red',fg='white',width=10,text='sp spec',
                 command=set_guild_ind)
but5_guild_a=tk.Button(tab5,bg='red',fg='white',width=10,text='rp all',
                 command=set_guild_all)
#position
latex6.place(x=70,y=50)
latex7.place(x=70,y=100)
but5_guild.place(x=40,y=130)
but5_guild_a.place(x=190,y=130)

##Tab 6
#button and label
tk.Label(tab6, text="in game name",fg='blue').place(x=70,y=20)
latex8 = tk.Text(tab6, height = 1, width = 20)
but81 = tk.Button(tab6,bg='blue',fg='white',width=10,text='search',
                 command=id_search)
but82 = tk.Button(tab6,bg='red',fg='white',width=10,text='Turn Off spe',
                 command=tof_log_ind)
but83 = tk.Button(tab6,bg='red',fg='white',width=10,text='Turn On spe',
                 command=ton_log_ind)
but84 = tk.Button(tab6,bg='red',fg='white',width=10,text='Turn Off all',
                 command=tof_log_all)
but85 = tk.Button(tab6,bg='red',fg='white',width=10,text='Turn On all',
                 command=ton_log_all)
#position
latex8.place(x=70,y=50)
but81.place(x=70,y=80)
but82.place(x=40,y=150)
but83.place(x=40,y=180)
but84.place(x=190,y=150)
but85.place(x=190,y=180)
##Tab 7
ckbut7 = tk.Checkbutton(tab7, text='Header' ,variable=cb_head, onvalue=1, offvalue=0).place(x=70,y=50)
but71= tk.Button(tab7,bg='red',fg='white',width=10,text='Upload',
                 command=up_road).place(x=70,y=80)
##end loop
root.mainloop()

####END CODE
