import os
import ast
import csv
import glob
import psycopg2
import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk
from tkinter import filedialog as fd

filename=['database.ini','database - Copy.ini']
#Postges Setup
def config(filename, section='postgresql'):
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



##Postgres define function


#Basic
def setup(state):
    global conn
    global cur
    if state==0:
        param = config(filename[0])
    else:
        param = config(filename[1])
    conn = psycopg2.connect(**param)
    cur = conn.cursor()
    return print('connected')
def convert(fetchall):
    c=[fetchall[i][0] for i in range(len(fetchall))]
    return c
def char_id(inp):
    sql = '''SELECT id FROM public.characters WHERE name='%s' '''
    cur.execute(sql % inp)
    log_i  = cur.fetchall();
    log_i = convert(log_i)
    a = len(log_i)
    if a==0:
        return None
    elif a==1:
        return log_i[0]
    else:
        return log_i
def char_name(cid):
    sql = '''SELECT name FROM public.characters where id = %s '''
    cur.execute(sql % cid)
    id_s = cur.fetchone();
    return id_s[0]
def user_id(cid):
    sql = '''SELECT user_id FROM public.characters where id = %s '''
    cur.execute(sql % cid)
    a=cur.fetchone();
    return a[0]
def username(uid):
    sql = '''SELECT username FROM public.users where id = %s '''
    cur.execute(sql % uid)
    a=cur.fetchone();
    return a[0]
    

#Course
def rg_ch(cid,value):
    sql = """ UPDATE public.users SET rights = %s WHERE id = %s """
    cur.execute(sql % (value,user_id(cid)))
    conn.commit()
    
def rg_ch_all(value):
    sql = """ UPDATE public.users SET rights = %s """
    cur.execute(sql % str(value))
    conn.commit()
    
def rg_def(value):
    sql="""ALTER TABLE public.users ALTER COLUMN rights SET DEFAULT %s """
    cur.execute(sql % str(value))
    conn.commit()

    
#GCP
def gcp_id():
    sql = 'SELECT id FROM public.characters WHERE gcp IS NOT NULL'
    cur.execute(sql)
    gcp_n = cur.fetchall();
    return convert(gcp_n)
def gcp_search(cid):
    sql = '''SELECT gcp FROM public.characters where id = %s '''
    cur.execute(sql % cid)
    gcp_s = cur.fetchone();
    return gcp_s[0]
def gcp_ch(cid,value):
    sql = """ UPDATE public.characters SET gcp = %s WHERE id = %s """
    cur.execute(sql % (value,cid))
    conn.commit()
def gcp_ch_all(value):
    sql = """ UPDATE public.characters SET gcp = %s """
    cur.execute(sql % value)
    conn.commit()
def gcp_add(cid,value):
    a = value + gcp_search(cid)
    gcp_ch(cid,a)
def gcp_sub(cid,value):
    a = value - gcp_search(cid)
    if a<0:
        a=0
    gcp_ch(cid,a)
    

#Transmog
def tra_ind(cid):
    hexa = open('skin_hist.bin','rb').read().hex()
    sql = '''UPDATE characters SET skin_hist=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (hexa,cid))
    conn.commit()
def tra_all():
    hexa = open('skin_hist.bin','rb').read().hex()
    sql = '''UPDATE characters SET skin_hist=(decode('%s','hex')) '''
    cur.execute(sql % hexa)
    conn.commit()

#Gacha Coin
def prem_ind(cid,value):
    sql = """ UPDATE public.characters SET gacha_prem = %s WHERE id = %s """
    cur.execute(sql % (str(value),cid))
    conn.commit()
def trial_ind(cid,value):
    sql = """ UPDATE public.characters SET gacha_trial = %s WHERE id = %s """
    cur.execute(sql % (str(value),cid))
    conn.commit()
def prem_all(value):
    sql = """ UPDATE public.characters SET gacha_prem = %s """
    cur.execute(sql % str(value))
    conn.commit()
def trial_all(value):
    sql = """ UPDATE public.characters SET gacha_trial = %s """
    cur.execute(sql % str(value))
    conn.commit()


#Guild
def guild_name():
    sql = 'SELECT name FROM public.guilds'
    cur.execute(sql)
    guild_n = cur.fetchall()
    return convert(guild_n)
def guild_stat(cid):
    sql='''SELECT guild_id FROM public.guild_characters WHERE character_id = %s '''
    cur.execute(sql % cid)
    a = cur.fetchone()
    if a==None:
        return None
    else:
        sql = 'SELECT name FROM public.guilds WHERE id = %s'
        cur.execute(sql % a[0])
        a = cur.fetchone()
        return a[0]
def guild_id(inp):
    sql = '''SELECT id FROM public.guilds WHERE name = '%s' '''
    cur.execute(sql % inp)
    guild_i = cur.fetchone()
    return guild_i[0]
def guild_mem(gid):
    sql1='''SELECT character_id FROM public.guild_characters WHERE guild_id = %s '''
    cur.execute(sql1 % gid)
    a= cur.fetchall() 
    return len(convert(a))
def member_id(gid):
    sql='''SELECT character_id FROM public.guild_characters WHERE guild_id = %s '''
    cur.execute(sql % gid)
    a=cur.fetchall()
    return convert(a)
def guild_pkey():
    sql='''SELECT id FROM public.guild_characters '''
    cur.execute(sql)
    gd_index = cur.fetchall()
    a=convert(gd_index)
    a.sort()
    return a[-1]+1
def leader(cid,gid):
    sql='''UPDATE public.guilds SET leader_id=%s WHERE id=%s '''
    sql1='''UPDATE public.guild_characters SET avoid_leadership=false WHERE character_id=%s '''
    cur.execute(sql % (cid,gid))
    cur.execute(sql1 % cid)
    conn.commit()
def member_add(cid,gid):
    sql = ''' INSERT INTO guild_characters (id,guild_id,character_id,joined_at,avoid_leadership,order_index) VALUES (%s,%s,%s,DEFAULT,true,DEFAULT)'''
    cur.execute(sql % (guild_pkey(),gid,cid))
    conn.commit()    
def change_guild(cid,gid):
    sql='''UPDATE public.guild_characters SET guild_id=%s WHERE character_id=%s '''
    cur.execute(sql % (gid,cid))
    conn.commit()
def guild_ind(gid,value):
    sql = """ UPDATE public.guilds SET rank_rp = %s WHERE id = %s """
    cur.execute(sql % (value,gid))
    conn.commit()
def guild_all(value):
    sql = """ UPDATE public.guilds SET rank_rp = %s"""
    cur.execute(sql % value)
    conn.commit()

#Login Boost
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


#Road Shop
def road_up(road_dir,state):
    file = open(road_dir)
    csvrd = csv.reader(file)
    sql2 = '''TRUNCATE TABLE public.normal_shop_items RESTART IDENTITY'''
    sql = ''' INSERT INTO normal_shop_items (shoptype,shopid,itemhash,itemid,points,tradequantity,rankreqlow,rankreqhigh,rankreqg,storelevelreq,maximumquantity,boughtquantity,roadfloorsrequired,weeklyfataliskills) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    sql1 = ''' INSERT INTO normal_shop_items (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    if (state==1):
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
def road_scan():
    sql = 'SELECT itemhash FROM public.normal_shop_items'
    cur.execute(sql)
    global road_ln
    a = cur.fetchall();
    a=convert(a)
    road_ln=len(a)
    a.sort()
    return a[-1]+1
def road_add(item,price,quant,floor,fata):
    sql = ''' INSERT INTO normal_shop_items (shoptype,shopid,itemhash,itemid,points,tradequantity,rankreqlow,rankreqhigh,rankreqg,storelevelreq,maximumquantity,boughtquantity,roadfloorsrequired,weeklyfataliskills) VALUES (10,5,%s,%s,%s,%s,0,0,1,1,0,1,%s,%s)'''
    cur.execute(sql % (road_scan(),item,price,quant,floor,fata))
    conn.commit()
def road():
    sql = 'SELECT * FROM public.normal_shop_items'
    cur.execute(sql)
    a = cur.fetchall()
    return a
def road_head():
    sql = 'SELECT * FROM public.normal_shop_items'
    cur.execute(sql)
    a = [desc[0] for desc in cur.description]
    return a
def road_down(direc,state):
    a = road()
    f=open(direc,'w')
    wr=csv.writer(f)
    if state==1:
        wr.writerow(road_head())
    for i in range(len(a)):
        wr.writerow(a[i])
    f.close()
#Savefile Edit
def save_save(cid,savefile):
    hexa = open(savefile,'rb').read().hex()
    sql = '''UPDATE characters SET savedata=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (hexa,cid))
    conn.commit()
def save_partner(cid,partner):
    hexa = open(partner,'rb').read().hex()
    sql = '''UPDATE characters SET partner=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (hexa,cid))
    conn.commit()
def download(cid,table):
    sql = '''SELECT %s FROM characters WHERE id= %s '''
    cur.execute(sql % (table,cid))
    a = cur.fetchone();
    if a[0]==None:
        return bytes(0)
    else:
        return bytes(a[0])
def overwrite(direc,data):
    a=open(direc,'wb')
    a.write(data)
    a.close()
def down_all(cid):
    a=['savedata','decomyset','partner','hunternavi','otomoairou','platebox',
       'platedata','platemyset','rengokudata','savemercenary','skin_hist']
    b=['bulk_savefile\\','.bin']
    for i in range(len(a)):
        c=download(cid,a[i])
        overwrite(b[0]+a[i]+b[1],c)
def upload(cid,table,data):
    hexa = open(data,'rb').read().hex()
    sql = '''UPDATE characters SET %s=(decode('%s','hex')) WHERE id= %s '''
    cur.execute(sql % (table,hexa,cid))
    conn.commit()
def up_all(cid):
    a=['savedata','decomyset','partner','hunternavi','otomoairou','platebox',
       'platedata','platemyset','rengokudata','savemercenary','skin_hist']
    b=['bulk_savefile\\','.bin']
    for i in range(len(a)):
        upload(cid,a[i],b[0]+a[i]+b[1])




### Tkinter
#Error Prevention state
state_inp=[0]
err_inp=['nothing','input is not integer','input is not hexadecimal']
state_con=[0]
state_ch=[0]
state9=[0]
state_id=[0]
##Error function
#input error
def err_l():
    if state_inp[0]==0:
        return None
    else:
        l.config(text=err_inp[state_inp[0]])
def int_err(inp):
    try:
        a = int(inp)
        return a
    except ValueError as error:
        state_inp[0]=1
        err_l()
def hex_err(inp):
    try:
        z = ast.literal_eval(inp)
        return z
    except SyntaxError as error:
        state_inp[0]=2
        err_l()
        return None
def connect(state):
    try:
        setup(state)
        state_con[0]=0
    except (Exception, psycopg2.DatabaseError) as error:
        state_con[0]=1
        l.config(text="database error")
def inp_id(inp):
    a = char_id(inp)
    if a==None:
        l.config(text='charachter not found')
    else:
        if isinstance(a,int)==True:
            l.config(text='charachter found with id ='+str(a))
            return a
        else:
            l.config(text='there is some id with same name')
            global pickid
            pickid = tk.Tk()
            pickid.title("pick id")
            tabControl = ttk.Notebook(pickid)
            global poly
            poly=tk.StringVar()
            poly.set(a[len(a)-1])
            for i in range(len(a)):
                tk.Label(pickid, text='id= '+str(a[i])+' have character name ='+char_name(a[i])+' and user name ='+username(user_id(a[i]))
                 ,fg='white',bg='blue').pack()
            tk.OptionMenu(pickid,poly,*a,command=drop_c).pack()
            pickid.mainloop()
def drop_c(ch):
    ch = poly.get()
    l.config(text='you selected id = '+str(ch))
    pickid.destroy()
    if state_id[0]==0:
        global cid
        cid = int(ch)
        state_ch[0]=0
        common_edit()
    else:
        global cid1
        cid1=int(ch)
        guild_prep()
            

###Tkinter Button func
#Button name
sett=['set','set to all']
add=['add','add to all']
sub=['sub','sub to all']
act=['activate','activate all']
deact=['deactivate','deactivate all']

##Button assign
#Course
def set_rg():
    if state_ch[0]==0:
        rg_ch(cid,intend)
        l.config(text='succesfully set id '+str(cid)+'rights to '+str(intend))
    else:
        rg_ch_all(intend)
        l.config(text='succesfully set all rights to '+str(intend))
def default_rg():
    rg_def(intend)
    l.config(text='succesfully set default right to '+str(intend))

#Gcp
def set_gcp():
    inp = gcpx.get(1.0, "end-1c")
    a=int_err(inp)
    if a==None:
        return None
    if state_ch[0]==0:
        gcp_ch(cid,a)
        l.config(text='succesfully set id '+str(cid)+'gcp to '+str(a))
    else:
        gcp_ch_all(a)
        l.config(text='succesfully set all gcp to '+str(a))
def add_gcp():
    inp = gcpx.get(1.0, "end-1c")
    a=int_err(inp)
    if a==None:
        return None
    if state_ch[0]==0:
        gcp_add(cid,a)
        l.config(text='succesfully add id '+str(cid)+'gcp with '+str(a))
    else:
        b=gcp_id()
        for i in range(len(b)):
            gcp_add(b[i],a)
        l.config(text='succesfully add all gcp with '+str(a))
def sub_gcp():
    inp = gcpx.get(1.0, "end-1c")
    a=int_err(inp)
    if a==None:
        return None
    if state_ch[0]==0:
        gcp_sub(cid,a)
        l.config(text='succesfully substract id '+str(cid)+'gcp with '+str(a))
    else:
        b=gcp_id()
        for i in range(len(b)):
            gcp_add(b[i],a)
        l.config(text='succesfully substract all gcp with '+str(a))
        
#Transmog
def set_mog():
    if state_ch[0]==0:
        tra_ind(cid)
        l.config(text='succesfully unlock all id '+str(cid)+' transmog')
    else:
        tra_all()
        l.config(text='succesfully unlock transmog for all charachter')
        
#Login boost
def ton_log():
    if state_ch[0]==0:
        log_ton(cid)
        l.config(text='succesfully unlock all id '+str(cid)+' boost')
    else:
        log_ton_all()
        l.config(text='succesfully unlock boost for all charachter')
def tof_log():
    if state_ch[0]==0:
        log_tof(cid)
        l.config(text='succesfully seal all id '+str(cid)+' boost')
    else:
        log_tof_all()
        l.config(text='succesfully seal boost for all charachter')

#gacha coin:
def set_trial():
    inp = gachax.get(1.0, "end-1c")
    a=int_err(inp)
    if a==None:
        return None
    if state_ch[0]==0:
        trial_ind(cid,a)
        l.config(text='succesfully set trial coin '+str(cid)+'gcp to '+str(a))
    else:
        trial_all(a)
        l.config(text='succesfully set all trial coin to '+str(a))
def set_prem():
    inp = gachax.get(1.0, "end-1c")
    a=int_err(inp)
    if a==None:
        return None
    if state_ch[0]==0:
        prem_ind(cid,a)
        l.config(text='succesfully set premium coin '+str(cid)+'gcp to '+str(a))
    else:
        pre_all(a)
        l.config(text='succesfully set all premium coin to '+str(a))

#Save editor
filetypes = (
                ('binary files', '*.bin'),
                ('All files', '*.*')
                )
def save_upload():
    savefile = fd.askopenfilename(
                title='Open save data',
                initialdir=os.getcwd()+'\\your_savefile',
                filetypes=filetypes)
    if savefile:
        save_save(cid,savefile)
        l.config(text='upload savefile success')
    else:
        l.config(text='you didnt select any file')
def partner_upload():
    savefile = fd.askopenfilename(
                title='Open partner data',
                initialdir=os.getcwd()+'\\your_savefile',
                filetypes=filetypes)
    if savefile:
        save_partner(cid,savefile)
        l.config(text='upload partner file success')
    else:
        l.config(text='you didnt select any file')
def save_download():
    savefile = fd.asksaveasfilename(
                title='create save data',
                initialdir=os.getcwd()+'\\your_savefile',
                defaultextension=".bin",
                filetypes=filetypes)
    if savefile:
        a=download(cid,'savedata')
        overwrite(savefile,a)
        l.config(text='download savefile success')
    else:
        l.config(text='you didnt select any file')
def partner_download():
    savefile = fd.asksaveasfilename(
                title='create partner data',
                initialdir=os.getcwd()+'\\your_savefile',
                defaultextension=".bin",
                filetypes=filetypes)
    if savefile:
        a=download(cid,'partner')
        overwrite(savefile,a)
        l.config(text='download partner file success')
    else:
        l.config(text='you didnt select any file')

def bulk_down():
    down_all(cid)
    l.config(text='download all file to directory success')
def bulk_up():
    up_all(cid)
    l.config(text='upload all file in directory success')

#Guild
def scan_g():
    a=guild_name()
    if a[0]==None:
        l.config(text='there is no guild')
        return None
    global varg
    varg = tk.StringVar()
    varg.set(a[len(a)-1])
    tk.OptionMenu(tab8,varg,*a,command=get_rp).place(x=110,y=50)
    l.config(text=str(len(a))+' guild found')
    tk.Button(tab8,bg='red',fg='white',width=10,text='set RP all',
                 command=set_rp_all).place(x=190,y=130)
    global rpx
    rpx = tk.Text(tab8, height = 1, width = 20)
    tk.Label(tab8, text="rp value input",fg='blue').place(x=70,y=80)
    rpx.place(x=70,y=100)
    
def get_rp(ch):
    ch = varg.get()
    global gid
    gid = guild_id(ch)
    l.config(text=ch+' with id '+str(gid)+'have member='+str(guild_mem(gid)))
    tk.Button(tab8,bg='red',fg='white',width=10,text='set RP',
                 command=set_rp_ind).place(x=40,y=130)
    
def set_rp_ind():
    a=rpx.get(1.0, "end-1c")
    a=int_err(a)
    if a==None:
        return None
    guild_ind(gid,a)
    l.config(text='successfully set RP values')
def set_rp_all():
    a=rpx.get(1.0, "end-1c")
    a=int_err(a)
    if a==None:
        return None
    guild_all(a)
    l.config(text='successfully set RP values for all')

def mem_of_guild():
    a=guildx.get(1.0, "end-1c")
    state_id[0]=1
    a = inp_id(a)
    if a==None:
        return None
    global cid1
    cid1=a
    guild_prep()
def guild_prep():
    b = guild_stat(cid1)
    global butt_add,butt_ch,butt_ld
    if b==None:
        l.config(text='you are not in any guild')
        butt_add=tk.Button(tab8,bg='red',fg='white',width=10,text='add to guild',
                 command=add_to_guild)
        butt_add.place(x=40,y=260)
    else:
        l.config(text='you are in guild '+b)
        global neg
        neg = b
        butt_ch=tk.Button(tab8,bg='red',fg='white',width=10,text='change guild',
                 command=change_gd)
        butt_ch.place(x=40,y=260)
        butt_ld=tk.Button(tab8,bg='red',fg='white',width=10,text='set leader',
                 command=set_leader)
        butt_ld.place(x=190,y=260)
def add_to_guild():
    a=guild_name()
    if a==None:
        l.config(text='there is no guild')
        return None
    global varg1,d1
    varg1 = tk.StringVar()
    varg1.set(a[len(a)-1])
    d1=tk.OptionMenu(tab8,varg1,*a,command=get_guild)
    d1.place(x=40,y=290)
def get_guild(ch):
    ch=varg1.get()
    member_add(cid1,guild_id(ch))
    l.config(text='added to guild')
    d1.place_forget()
    butt_add.place_forget()
def change_gd():
    a=guild_name()
    if len(a)==1:
        l.config(text='there is no other guild')
        return None
    a.remove(neg)
    global varg2,d2
    varg2 = tk.StringVar()
    varg2.set(a[len(a)-2])
    d2=tk.OptionMenu(tab8,varg2,*a,command=get_chage)
    d2.place(x=40,y=290)
def get_chage(ch):
    ch=varg2.get()
    change_guild(cid1,guild_id(ch))
    l.config(text='seccessfully change guild')
    d2.place_forget()
    butt_ch.place_forget()
def set_leader():
    leader(cid1,guild_id(neg))
    l.config(text='successfully set as leader')
    butt_ld.place_forget()
#Road
def calc_f():
    state9[0]=1
    i1 = latex91.get(1.0, "end-1c")
    a = len(list(i1))
    global item_id
    if (a == 4):
        item_id=ferias(i1)
        l91.config(text=str(item_id))
    else:
        l.config(text= "format false")

def calc_u():
    state9[0]=1
    i1 = latex91.get(1.0, "end-1c")
    a = len(list(i1))
    global item_id
    if (a == 4):
        item_id=untranslated(i1)
        l91.config(text=str(item_id))
    else:
        l.config(text= "format false")
def scan_road():
    road_scan()
    l.config(text='road shop has '+str(road_v)+' item')
def add_road():
    if (state9[0]==1):
        i2 = latex92.get(1.0, "end-1c")
        i3 = latex93.get(1.0, "end-1c")
        i4 = latex94.get(1.0, "end-1c")
        i5 = latex95.get(1.0, "end-1c")
        if (i2!='' and i3!='' and i4!='' and i5!=''):
            try:
                i2 = int(i2)
                i3 = int(i3)
                i4 = int(i4)
                i5 = int(i5)
            except ValueError as error:
                l.config(text='input must be integer')
                return None
            road_add(item_id,i2,i3,i4,i5)
            l.config(text='item added')
        else:
            l.config(text='input blank')
    else:
        l.config(text='input blank')
filetypes1 = (("CSV files", "*.csv"),)
def up_road():
    a = cb_head.get()
    road_dir = fd.askopenfilename(
              title='Open a road file',
              initialdir=os.getcwd()+'\\road',
              filetypes=filetypes1)
    if road_dir:
        road_up(road_dir,a)
        l.config(text='road csv success')
    else:
        l.config(text='you didnt select any file')
def down_road():
    a = cb_head.get()
    global road_dir
    road_dir = fd.asksaveasfilename(
              title='Create a road file',
              initialdir=os.getcwd()+'\\road',
              defaultextension=".csv",
              filetypes=filetypes1)
    if road_dir:
        road_down(road_dir,a)
        l.config(text='road csv success')
    else:
        l.config(text='you didnt select any file')


        
##Interface
def change_con():
    connect(1)
    db1.pack_forget()
    global db2
    db2 = tk.Button(root,bg='red',fg='white',width=15,height=1,text='use primary db',
                 command=change_con1)
    db2.pack(side=tk.BOTTOM)
    l.config(text='connected to secondary db')
    tabControl.destroy()
    try:
        tomain.pack_forget()
    except NameError:
        None
    finally:
        mainmenu()
def change_con1():
    connect(0)
    db2.pack_forget()
    global db1
    db1 = tk.Button(root,bg='red',fg='white',width=15,height=1,text='use other db',
                 command=change_con)
    db1.pack(side=tk.BOTTOM)
    l.config(text='connected to primary db')
    tabControl.destroy()
    try:
        tomain.pack_forget()
    except NameError:
        None
    finally:
        mainmenu()
def mainmenu():
    global tabControl
    tabControl = ttk.Notebook(root,height=400,width=300,padding=10)
    global tab1
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text ='Home')
    tabControl.pack(expand = 1, fill ="both")
    tk.Label(tab1,height=2,text='This tab you can choose to edit single charachter\ndata or moderator data').place(x=20,y=20)
    tk.Label(tab1,text='Enter yur charachters name').place(x=70,y=80)
    global latex
    latex = tk.Text(tab1, height = 1, width = 20)
    latex.place(x=70,y=100)

    tk.Button(tab1,bg='blue',fg='white',width=10,height=2,text='search',
                 command=search_char).place(x=70,y=120)
    tk.Label(tab1,text='this button for moderator').place(x=80,y=250)
    tk.Button(tab1,bg='blue',fg='white',width=10,height=2,text='Moderator',
                 command=moderator).place(x=110,y=270)
def common_edit():
    a = state_ch[0]
    global tab2,tab6,tomain
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)
    tab5 = ttk.Frame(tabControl)
    tab6 = ttk.Frame(tabControl)
    tab7 = ttk.Frame(tabControl)
    tabControl.add(tab2, text ='Course')
    tabControl.add(tab3, text ='GCP')
    tabControl.add(tab4, text ='Mog')
    tabControl.add(tab5, text ='Login')
    tabControl.add(tab6, text ='save')
    tabControl.add(tab7, text ='Gacha')
    tabControl.pack(expand = 1, fill ="both")
    tomain=tk.Button(root,bg='yellow',fg='black',width=10,height=1,text='back to main',
                 command=back)
    tomain.pack(side=tk.TOP)
    tab1.destroy()
    
    #course
    for i in range(len(cal)):
        exec(f'''tk.Checkbutton(tab2, text=cal[i] ,variable=var{i}, onvalue=val[i], offvalue=0, command=calc).place(x=10,y=200+i*20) ''')
    global z
    z = tk.Label(tab2, bg='black',fg='white', width=10, text='2')
    z.place(x=150,y=300)
    tk.Button(tab2,bg='red',fg='white',width=12,height=1,text=sett[a],
                 command=set_rg).place(x=110,y=50)
    
    #GCP
    tk.Label(tab3, text="insert gcp value",fg='blue').place(x=70,y=20)
    global gcpx
    gcpx = tk.Text(tab3, height = 1, width = 20)
    gcpx.place(x=70,y=50)
    tk.Button(tab3,bg='red',fg='white',width=12,height=1,text=sett[a],
                 command=set_gcp).place(x=110,y=80)
    tk.Button(tab3,bg='red',fg='white',width=12,height=1,text=add[a],
                 command=add_gcp).place(x=110,y=110)
    tk.Button(tab3,bg='red',fg='white',width=12,height=1,text=sub[a],
                 command=sub_gcp).place(x=110,y=140)

    #transmog
    tk.Label(tab4, text="this tab for unlock transmog",fg='blue').place(x=70,y=20)
    tk.Button(tab4,bg='red',fg='white',width=12,height=1,text=sett[a],
                 command=set_mog).place(x=110,y=110)

    #Login boost
    tk.Label(tab5, text="tris tab for login boost",fg='blue').place(x=70,y=20)
    tk.Button(tab5,bg='red',fg='white',width=12,height=1,text=act[a],
                 command=ton_log).place(x=110,y=110)
    tk.Button(tab5,bg='red',fg='white',width=12,height=1,text=deact[a],
                 command=tof_log).place(x=110,y=140)

    #save
    tk.Button(tab6,bg='red',fg='white',width=12,height=1,text='upload save',
                 command=save_upload).place(x=40,y=50)
    tk.Button(tab6,bg='red',fg='white',width=12,height=1,text='upload partner',
                 command=partner_upload).place(x=40,y=80)
    tk.Button(tab6,bg='red',fg='white',width=12,height=1,text='download save',
                 command=save_download).place(x=190,y=50)
    tk.Button(tab6,bg='red',fg='white',width=12,height=1,text='download partner',
                 command=partner_download).place(x=190,y=80)
    tk.Button(tab6,bg='red',fg='white',width=12,height=1,text='download all',
                 command=bulk_down).place(x=110,y=250)
    tk.Button(tab6,bg='red',fg='white',width=12,height=1,text='upload all',
                 command=bulk_up).place(x=110,y=280)
    tk.Label(tab6, text="this button bellow to mine all data\nto/in directory only use it if you\ncompletely understand",fg='blue',height=3).place(x=70,y=190)

    #Gacha Coin
    tk.Label(tab7, text="insert gcp value",fg='blue').place(x=70,y=20)
    global gachax
    gachax = tk.Text(tab7, height = 1, width = 20)
    gachax.place(x=70,y=50)
    tk.Label(tab7, text="premium gacha coin",fg='blue').place(x=70,y=80)
    tk.Button(tab7,bg='red',fg='white',width=12,height=1,text=sett[a],
                 command=set_prem).place(x=110,y=100)
    tk.Label(tab7, text="trial gacha coin",fg='blue').place(x=70,y=150)
    tk.Button(tab7,bg='red',fg='white',width=12,height=1,text=sett[a],
                 command=set_trial).place(x=110,y=170)
def mod_edit():
    global tab8
    tab8 = ttk.Frame(tabControl)
    tab9 = ttk.Frame(tabControl)
    tabControl.add(tab8, text ='Guild')
    tabControl.add(tab9, text ='Road')
    tabControl.pack(expand = 1, fill ="both")
    tab6.destroy()
    
    #course
    tk.Button(tab2,bg='red',fg='white',width=12,height=1,text='set as default',
                 command=default_rg).place(x=110,y=80)
    #Guild
    global guildx
    tk.Button(tab8,bg='blue',fg='white',width=10,text='scan',
                     command=scan_g).place(x=100,y=20)
    guildx = tk.Text(tab8, height = 1, width = 10)
    tk.Label(tab8, text="insert charachter id",fg='blue').place(x=70,y=180)
    tk.Button(tab8,bg='blue',fg='white',width=10,text='inspect',
                     command=mem_of_guild).place(x=70,y=230)
    guildx.place(x=70,y=200)
    #Road
    global l91,latex91,latex92,latex93,latex94,latex95
    l91 = tk.Label(tab9, text="empty",fg='white',width=5,bg='black')
    tk.Label(tab9, text="Upload csv file",fg='blue').place(x=70,y=20)
    tk.Checkbutton(tab9, text='Header' ,variable=cb_head, onvalue=1, offvalue=0).place(x=70,y=50)
    tk.Button(tab9,bg='red',fg='white',width=10,text='Upload',
                     command=up_road).place(x=70,y=80)
    tk.Button(tab9,bg='red',fg='white',width=10,text='Download',
                     command=down_road).place(x=70,y=110)
    latex91 = tk.Text(tab9, height = 1, width = 5)
    latex92 = tk.Text(tab9, height = 1, width = 10)
    latex93 = tk.Text(tab9, height = 1, width = 10)
    latex94 = tk.Text(tab9, height = 1, width = 10)
    latex95 = tk.Text(tab9, height = 1, width = 10)
    tk.Label(tab9, text="Item id",fg='blue').place(x=20,y=150)
    tk.Label(tab9, text="Item Price",fg='blue').place(x=20,y=180)
    tk.Label(tab9, text="Item quantity",fg='blue').place(x=20,y=210)
    tk.Label(tab9, text="Floor req",fg='blue').place(x=20,y=240)
    tk.Label(tab9, text="Fatalis req",fg='blue').place(x=20,y=270)
    tk.Button(tab9,bg='blue',fg='white',width=10,text='scan',
                     command=scan_road).place(x=100,y=300)
    tk.Button(tab9,bg='red',fg='white',width=10,text='add item',
                     command=add_road).place(x=100,y=330)
    tk.Button(tab9,bg='blue',fg='white',width=10,text='conv ferias',
                     command=calc_f).place(x=200,y=135)
    tk.Button(tab9,bg='blue',fg='white',width=10,text='conv untrans',
                     command=calc_u).place(x=200,y=165)
    l91.place(x=100,y=150)
    latex91.place(x=150,y=150)
    latex92.place(x=100,y=180)
    latex93.place(x=100,y=210)
    latex94.place(x=100,y=240)
    latex95.place(x=100,y=270)
def search_char():
    inp = latex.get(1.0, "end-1c")
    global cid
    state_id[0]=0
    cid=inp_id(inp)
    if cid==None:
        return None
    state_ch[0]=0
    common_edit()
def moderator():
    state_ch[0]=1
    common_edit()
    mod_edit()
def back():
    tabControl.destroy()
    tomain.pack_forget()
    mainmenu()
##Tkinter bind Setup
root = tk.Tk()
root.title("Database Edit")
connect(0)
mainmenu()
#root
l = tk.Label(root, bg='black',fg='white', width=40, text='connected to database')
l.pack(side=tk.BOTTOM)
db1 = tk.Button(root,bg='red',fg='white',width=15,height=1,text='use other db',
                 command=change_con)
db1.pack(side=tk.BOTTOM)
cb_head=tk.IntVar()

##Calculator
#Asset
cal=['Hunter Course','Extra Course','Premium Course','Assist Course','N Course',
      'Hiden Course','Support Course','N boost Course']
val=[4,8,64,256,512,1024,2048,4096]
for i in range(len(cal)):
        exec(f'''var{i} = tk.IntVar()''')

#function
def ferias(inp):
    x = list(inp)
    y = '0x'+x[0]+x[1]+x[2]+x[3]
    y=hex_err(y)
    if y==None:
        return None
    else:
        return y
    
def untranslated(inp):
    x = list(inp)
    y = '0x'+x[2]+x[3]+x[0]+x[1]
    y=hex_err(y)
    if y==None:
        return None
    else:
        return y

def calc():
    global intend
    intend = 2 + var0.get()+ var1.get()+ var2.get()+ var3.get()+ var4.get()+ var5.get()+ var6.get()+ var7.get()
    z.config(text= str(intend))
    
###END
root.mainloop()
