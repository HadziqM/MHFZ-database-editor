import os
import ast
import csv
import psycopg2
import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk
from tkinter import filedialog as fd


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
    global tab8
    
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
    tab8 = ttk.Frame(tabControl)
  
    tabControl.add(tab2, text ='Course')
    tabControl.add(tab3, text ='GCP')
    tabControl.add(tab1, text ='mog')
    tabControl.add(tab4, text ='gacha')
    tabControl.add(tab5, text ='guild')
    tabControl.add(tab6, text ='login')
    tabControl.add(tab7, text ='road')
    tabControl.add(tab8, text ='save')
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
    global cur
    try:
        param = config()
        conn = psycopg2.connect(**param)
        cur = conn.cursor()
        state0[0]=0
    except (Exception, psycopg2.DatabaseError) as error:
        state0[0]=1
        l.config(text="database error")

# Call Funnction
def join_int(tuple_of_string):
    global numb 
    numb = []
    for i in range(len(tuple_of_string)):
        numb.append(''.join(str(y) for y in tuple_of_string[i]))
    for i in range(len(numb)):
        numb[i]=int(numb[i])
def join_int2(tuple_of_string):
    global numb2 
    numb2 = []
    for i in range(len(tuple_of_string)):
        numb2.append(''.join(str(y) for y in tuple_of_string[i]))
    for i in range(len(numb2)):
        numb2[i]=int(numb2[i])
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
    
def gcp_search(inp):
    sql = '''SELECT gcp FROM public.characters where id = %s '''
    global gcp_s
    cur.execute(sql % inp)
    gcp_s = cur.fetchall();

def gcp_ch(idn,value):
    sql = """ UPDATE public.characters SET gcp = %s WHERE id = %s """
    cur.execute(sql % (str(value),idn))
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
def tra_ind(idn):
    hexa = open(cwd,'rb').read().hex()
    sql = '''UPDATE characters SET skin_hist=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (hexa,idn))
    conn.commit()
def tra_all():
    hexa = open(cwd,'rb').read().hex()
    sql = '''UPDATE characters SET skin_hist=(decode('%s','hex')) '''
    cur.execute(sql % hexa)
    conn.commit()
def prem_ind(idn,value):
    sql = """ UPDATE public.characters SET gacha_prem = %s WHERE id = %s """
    cur.execute(sql % (str(value),idn))
    conn.commit()
def trial_ind(idn,value):
    sql = """ UPDATE public.characters SET gacha_trial = %s WHERE id = %s """
    cur.execute(sql % (str(value),idn))
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
    sql = '''SELECT id FROM public.characters WHERE name='%s' '''
    cur.execute(sql % name)
    global log_i
    log_i  = cur.fetchall();
def log_tof(idn):
    sql = ''' UPDATE public.login_boost_state SET end_time = 1 WHERE char_id= %s '''
    cur.execute(sql % str(idn))
    conn.commit()
def log_ton(idn):
    sql = '''UPDATE public.login_boost_state SET week_count = 5 WHERE char_id= %s'''
    sql1= '''UPDATE public.login_boost_state SET available = true WHERE char_id= %s'''
    sql2 = ''' UPDATE public.login_boost_state SET end_time = 0 WHERE char_id= %s '''
    cur.execute(sql % str(idn))
    cur.execute(sql2 % str(idn))
    cur.execute(sql1 % str(idn))
    conn.commit()
def log_tof_all():
    sql = ''' UPDATE public.login_boost_state SET end_time = 1'''
    cur.execute(sql)
    conn.commit()
def log_ton_all():
    sql = '''UPDATE public.login_boost_state SET week_count = 5 '''
    sql1= '''UPDATE public.login_boost_state SET available = true'''
    sql2= '''UPDATE public.login_boost_state SET end_time = 0'''
    cur.execute(sql)
    cur.execute(sql1)
    cur.execute(sql2)
    conn.commit()
def road_up():
    file = open(road_dir)
    csvrd = csv.reader(file)
    sql2 = '''TRUNCATE TABLE public.normal_shop_items RESTART IDENTITY'''
    sql = ''' INSERT INTO normal_shop_items (shoptype,shopid,itemhash,itemid,points,tradequantity,rankreqlow,rankreqhigh,rankreqg,storelevelreq,maximumquantity,boughtquantity,roadfloorsrequired,weeklyfataliskills) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    sql1 = ''' INSERT INTO normal_shop_items (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    if ( cb_head.get()==1):
        header_id = []
        header_id = next(csvrd)
        cur.execute(sql2)        
        for row in csvrd:
            a = []
            a.append(row)
            cur.execute(sql1 % (header_id[0],header_id[1],header_id[2],header_id[3],header_id[4],header_id[5],header_id[6],header_id[7],header_id[8],header_id[9],header_id[10],header_id[11],header_id[12],header_id[13],a[0][0],a[0][1],a[0][2],a[0][3],a[0][4],a[0][5],a[0][6],a[0][7],a[0][8],a[0][9],a[0][10],a[0][11],a[0][12],a[0][13]))
    else:
        cur.execute(sql2)    
        for row in csvrd:
            a = []
            a.append(row)
            cur.execute(sql % (a[0][0],a[0][1],a[0][2],a[0][3],a[0][4],a[0][5],a[0][6],a[0][7],a[0][8],a[0][9],a[0][10],a[0][11],a[0][12],a[0][13]))
    conn.commit()
            
def save_save(idn):
    hexa = open(savefile,'rb').read().hex()
    sql = '''UPDATE characters SET savedata=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (hexa,idn))
    conn.commit()
def save_partner(idn):
    hexa = open(partner,'rb').read().hex()
    sql = '''UPDATE characters SET partner=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (hexa,idn))
    conn.commit()
def road_scan():
    sql = 'SELECT itemhash FROM public.normal_shop_items'
    cur.execute(sql)
    global road_s
    road_s = cur.fetchall();
    global road_i
    road_i = len(road_s)    
def road_add(item,price,quant,floor,fata):
    sql = ''' INSERT INTO normal_shop_items (shoptype,shopid,itemhash,itemid,points,tradequantity,rankreqlow,rankreqhigh,rankreqg,storelevelreq,maximumquantity,boughtquantity,roadfloorsrequired,weeklyfataliskills) VALUES (10,5,%s,%s,%s,%s,0,0,1,1,0,1,%s,%s)'''
    cur.execute(sql % (str(road_i+1),item,price,quant,floor,fata))
    conn.commit()

def ferias(inp):
    x = list(inp)
    y = '0x'+x[0]+x[1]+x[2]+x[3]
    z = ast.literal_eval(y)
    global item_id
    item_id = z
    
def untranslated(inp):
    x = list(inp)
    y = '0x'+x[2]+x[3]+x[0]+x[1]
    z = ast.literal_eval(y)
    global item_id
    item_id = z
def check_id(idnumb):
    sql = '''SELECT name FROM public.characters WHERE id=%s '''
    sql1= '''SELECT user_id FROM public.characters WHERE id=%s'''
    sql2 = '''SELECT username FROM public.users WHERE id= %s '''
    cur.execute(sql % idnumb)
    global nm
    nm = cur.fetchall();
    join_str(nm)
    nm = text[0]
    cur.execute(sql1 % idnumb)
    global nd
    uid = cur.fetchall();
    join_int2(uid)
    cur.execute(sql2 % numb2[0])
    nd = cur.fetchall();
    join_str(nd)
    nd = text[0]

###tkinter function

##ERROR define
def multiple_err(name):
    log_id(name)
    join_int(log_i)
    a = len(numb)
    global cid
    if a>=2 :
        l.config(text='same name with id = '+str([numb[i] for i in range(a)]))
        pick_id()
    elif (a==0):
        l.config(text='name not found')
    elif (a==1):
        l.config(text=name+' found with id '+str(numb[0]))
    cid = numb[0]
                 
def timeout():
    try:
        sql = 'SELECT username FROM public.users'
        cur.execute(sql)
    except psycopg2.OperationalError as error:
        l.config(text='connection timed out or failed to connect')
        
def drop_c(ch):
    ch = variable.get()
    numb[0] = ch
    l.config(text='you selected id = '+str(numb[0]))
    global cid
    cid = numb[0]
    root1.destroy()
def pick_id():
    global root1
    root1 = tk.Tk()
    root1.title("pick id")
    tabControl = ttk.Notebook(root1)
    a = len(numb)
    for i in range(a):
        check_id(numb[i])
        tk.Label(root1, text='id '+str(numb[i])+' have c_name ='+nm+' u_name ='+nd
                 ,fg='white',bg='black').pack()
    global variable
    variable = tk.StringVar()
    variable.set(numb[a-1])
    tk.OptionMenu(root1,variable,*numb,command=drop_c).pack()
    root1.mainloop()

#root
def connect():
    setup()
    if (state0[0]==0):
        l.config(text='reconnected to database')

#Tab 1

def search_tra():
    t_state[0]=1
    state1[0]=1
    global inp3
    inp3 = latexxxx.get(1.0, "end-1c")
    multiple_err(inp3)
    
    
def set_tra_ind():
    if (t_state[0]==1):
        if (state1[0]==1):
            tra_ind(cid)
            l.config(text="set specific success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
        
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
    multiple_err(inp2)
    gcp_search(cid)
    join_int(gcp_s)
    if (len(numb)==0):
        l.config(text="name not found, its case sensitive")
    else:
        if (gcp_s[0]==(None,)):
            l.config(text="you have no gcp")
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
            gcp_ch(cid,a)
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
            gcp_ch(cid,x)
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
            gcp_ch(cid,x)
            l.config(text="substract specific success")
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
#Tab 4

def search_gacha():
    t_state[0]=4
    state4[0]=1
    ber = latex4.get(1.0, "end-1c")
    multiple_err(ber)
    
def set_prem_ind():
    inp = latex5.get(1.0, "end-1c")
    if (t_state[0]==4):
        if (state4[0]==1):
            if (inp!=''):
                prem_ind(cid,inp)
                l.config(text="set specific success")
            else:
                l.config(text='fill your value input')
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
def set_trial_ind():
    ber = latex5.get(1.0, "end-1c")
    if (t_state[0]==4):
        if (state4[0]==1):
            if (ber!=''):
                trial_ind(cid,ber)
                l.config(text="set specific success")
            else:
                l.config(text='fill your value input')
        else:
            l.config(text="subject isnt scanned yet")
    else:
        l.config(text= "properties in wrong tab or not used yet")
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
    filetypes = (
                ('csv files', '*.csv'),
                ('All files', '*.*')
                )
    global road_dir

    road_dir = fd.askopenfilename(
              title='Open a file',
              initialdir='/',
              filetypes=filetypes)
    road_up()
    l.config(text='road csv success')

def scan_road():
    state7[1]=1
    road_scan()
    l.config(text='road shop has '+str(road_i)+' item')
    
def add_road():
    if (state7[1]==1):
        if (state7[0]==1):
            i2 = latex72.get(1.0, "end-1c")
            i3 = latex73.get(1.0, "end-1c")
            i4 = latex74.get(1.0, "end-1c")
            i5 = latex75.get(1.0, "end-1c")
            if (i2!='' and i3!='' and i4!='' and i5!=''):
                road_add(item_id,i2,i3,i4,i5)
                l.config(text='item added')
                state7[1]=0
            else:
                l.config(text='input blank')
        else:
            l.config(text='input blank')
    else:
        l.config(text='scan first')
def calc_f():
    state7[0]=1
    i1 = latex71.get(1.0, "end-1c")
    a = len(list(i1))
    if (a == 4):
        ferias(i1)
        l71.config(text=str(item_id))
    else:
        l.config(text= "format false")

def calc_u():
    state7[0]=1
    i1 = latex71.get(1.0, "end-1c")
    a = len(list(i1))
    if (a == 4):
        untranslated(i1)
        l71.config(text=str(item_id))
    else:
        l.config(text= "format false")
    
#Tab 8
def search_save():
    t_state[0]=8
    state8[0]=1
    inp8 = latex81.get(1.0, "end-1c")
    multiple_err(inp8)

def insert_save():
    if (t_state[0]==8):
        if (state8[0]==1):
            filetypes = (
                ('binary files', '*.bin'),
                ('All files', '*.*')
                )
            global savefile

            savefile = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            save_save(cid)
            l.config(text='upload savefile success')
        else:
            l.config(text='name not scanned yet')
    else:
        l.config(text='properties in wrong tab or not used yet')
def insert_partner():
    if (t_state[0]==8):
        if (state8[0]==1):
            filetypes = (
                ('binary files', '*.bin'),
                ('All files', '*.*')
                )
            global partner
            partner = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
            save_partner(cid)
            l.config(text='upload partner success')
        else:
            l.config(text='name not scanned yet')
    else:
        l.config(text='properties in wrong tab or not used yet')
#Error State
        
t_state = [0]
state0 = [0]
state1 = [0]
state2 = [0]
state3 = [0]
state4 = [0]
state5 = [0]
state6 = [0]
state8 = [0]
state7 = [0,0]

#Course Calculator aset

def calc():
    global intend
    intend = 2 + var0.get()+ var1.get()+ var2.get()+ var3.get()+ var4.get()+ var5.get()+ var6.get()+ var7.get()
    z.config(text= str(intend))
cal=['Hunter Course','Extra Course','Premium Course','Assist Course','N Course',
     'Hiden Course','Support Course','N boost Course']
val=[4,8,64,256,512,1024,2048,4096]





####START CODE

kinter()
cwd = os.getcwd()
cwd = cwd + '\\skin_hist.bin'
cwe = os.getcwd() + '\\road\\road.csv'
###TKINTER OBJECT

cb_head = tk.IntVar()

##Root


#Button and Label
l = tk.Label(root, bg='black',fg='white', width=30, text='connected to database')

tk.Button(root,bg='green',fg='white',width=10,height=2,text='reconnect',
                 command=connect).pack()

setup()
#Position
l.pack()


##Tab 1
#button and label
tk.Label(tab1, text="character name",fg='blue').place(x=50,y=20)
latexxxx = tk.Text(tab1, height = 1, width = 20)
but1_ind=tk.Button(tab1,bg='red',fg='white',width=10,text='set specific',
                 command=set_tra_ind)
but1_all=tk.Button(tab1,bg='red',fg='white',width=10,text='set all',
                 command=set_tra_all)
but11= tk.Button(tab1,bg='blue',fg='white',width=10,text='search',
                 command=search_tra)
#position
latexxxx.place(x=50,y=50)
but11.place(x=50,y=80)
but1_ind.place(x=50,y=110)
but1_all.place(x=50,y=140)
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
tk.Label(tab4, text="coin value",fg='blue').place(x=70,y=120)
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
but41 = tk.Button(tab4,bg='blue',fg='white',width=10,text='search',
                 command=search_gacha)
#position
latex4.place(x=70,y=50)
but41.place(x=70,y=80)
latex5.place(x=70,y=140)
but4_prem.place(x=40, y=170)
but4_prem_a.place(x=190,y=170)
but4_trial.place(x=40,y=200)
but4_trial_a.place(x=190,y=200)
##Tab 5
#buton and label
tk.Label(tab5, text="guild name",fg='blue').place(x=70,y=20)
tk.Label(tab5, text="rp value",fg='blue').place(x=70,y=70)
latex6=tk.Text(tab5, height = 1, width = 20)
latex7=tk.Text(tab5, height = 1, width = 20)
but5_guild=tk.Button(tab5,bg='red',fg='white',width=10,text='rp spec',
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
#button
l71 = tk.Label(tab7, text="empty",fg='white',width=5,bg='black')
tk.Label(tab7, text="Upload csv file",fg='blue').place(x=70,y=20)
ckbut7 = tk.Checkbutton(tab7, text='Header' ,variable=cb_head, onvalue=1, offvalue=0)
but71= tk.Button(tab7,bg='red',fg='white',width=10,text='Upload',
                 command=up_road)
latex71 = tk.Text(tab7, height = 1, width = 5)
latex72 = tk.Text(tab7, height = 1, width = 10)
latex73 = tk.Text(tab7, height = 1, width = 10)
latex74 = tk.Text(tab7, height = 1, width = 10)
latex75 = tk.Text(tab7, height = 1, width = 10)
tk.Label(tab7, text="Item id",fg='blue').place(x=20,y=150)
tk.Label(tab7, text="Item Price",fg='blue').place(x=20,y=180)
tk.Label(tab7, text="Item quantity",fg='blue').place(x=20,y=210)
tk.Label(tab7, text="Floor req",fg='blue').place(x=20,y=240)
tk.Label(tab7, text="Fatalis req",fg='blue').place(x=20,y=270)
but72= tk.Button(tab7,bg='blue',fg='white',width=10,text='scan',
                 command=scan_road)
but73= tk.Button(tab7,bg='red',fg='white',width=10,text='add item',
                 command=add_road)
but74= tk.Button(tab7,bg='blue',fg='white',width=10,text='conv ferias',
                 command=calc_f)
but75= tk.Button(tab7,bg='blue',fg='white',width=10,text='conv untrans',
                 command=calc_u)
#position
but71.place(x=70,y=80)
ckbut7.place(x=70,y=50)
l71.place(x=100,y=150)
latex71.place(x=150,y=150)
latex72.place(x=100,y=180)
latex73.place(x=100,y=210)
latex74.place(x=100,y=240)
latex75.place(x=100,y=270)
but72.place(x=100,y=300)
but73.place(x=100,y=330)
but74.place(x=200,y=135)
but75.place(x=200,y=165)

##Tab 8
#button
tk.Label(tab8, text="Character name",fg='blue').place(x=40,y=20)
latex81 = tk.Text(tab8, height = 1, width = 20)
but81= tk.Button(tab8,bg='blue',fg='white',width=10,text='search',
                 command=search_save)
but82=tk.Button(tab8,bg='red',fg='white',width=10,text='savefile',
                 command=insert_save)
but83=tk.Button(tab8,bg='red',fg='white',width=10,text='partner',
                 command=insert_partner)
#position
latex81.place(x=40,y=50)
but81.place(x=40,y=80)
but82.place(x=40,y=150)
but83.place(x=40,y=180)

##end loop
root.mainloop()

####END CODE
