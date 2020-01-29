#!/usr/bin/env python
# coding: utf-8
# In[2]:


import warnings
warnings.filterwarnings("ignore")


def date(train_path):
    with open(train_path, encoding='utf-8') as f:
        content = f.read()
    b = content.split("\n")
    b.remove("")
    return b


# In[7]:


def main(train_path):
    
    import single_return_6 as sr
    import inquiry as iq
    txtName = "{}_answer.txt".format(train_path.split('.')[0])
    f=open(txtName, "w+", encoding='utf-8')
    lst = date(train_path)
    from tqdm import tqdm 
    bar = tqdm(range(len(lst)))
    bar.set_description(train_path.split('.')[0])
    for j in bar: 
        i=lst[j]
        print("输入:",i)
        f.write("输入:"+i+'\n')
        nlu = sr.nlu(i)
        a = nlu[0]
        abst = nlu[1]
        #print(a,abst)
        ending='搜索失败'
        if a == 1:
            from_ = abst['from_'].replace('市','').replace('省','').replace('县','')
            to_ = abst['to_'].replace('市','').replace('省','').replace('县','')
            day_ = abst['date']
            time_ = abst['time']
            set_startloc=abst['set_startloc']
            set_arriveloc = abst['set_arriveloc']
            return_num = abst['return_num']
            set_flight = abst['set_flight']
            return_startloc_ans = abst['return_startloc_ans']
            Y =abst['Y']
            return_timelist=abst['return_timelist']
            return_startloc = abst['return_startloc']
            ending = iq.get_flighttickets(from_, to_, day_, time_=time_, return_timelist=return_timelist, 
                     set_startloc=set_startloc, set_arriveloc=set_arriveloc, return_num=return_num, 
                      set_flight= set_flight, return_startloc=return_startloc,return_startloc_ans = abst['return_startloc_ans'],Y =abst['Y'])
        elif a == 2:
            from_ = abst['from_']
            to_ = abst['to_']
            day_ = abst['date']
            time_ = abst['time']
            return_timelist = abst['return_timelist']
            set_startloc=abst['set_startloc']
            set_arriveloc = abst['set_arriveloc']
            return_num = abst['return_num']
            return_G = abst['return_G']
            return_startloc = abst['return_startloc']
            return_startloc_ans = abst['return_startloc_ans']
            Y =abst['Y']
            ending = iq.get_traintickets(from_, to_, day_, time_=time_, return_timelist=return_timelist, 
                     set_startloc=set_startloc, set_arriveloc=set_arriveloc, return_num=return_num,
                     return_startloc=return_startloc, return_G=return_G,
                     return_all=False, return_weather=True,return_startloc_ans = abst['return_startloc_ans'],Y =abst['Y'])
        elif a == 3:
            from_ = abst['from_']
            to_ = abst['to_']
            day_ = abst['date']
            time_ = abst['time']
            return_timelist = abst['return_timelist']
            set_startloc=abst['set_startloc']
            set_arriveloc = abst['set_arriveloc']
            return_num = abst['return_num']
            return_startloc = abst['return_startloc']
            return_startloc_ans = abst['return_startloc_ans']
            Y =abst['Y']
            ending = iq.get_bustickets(from_, to_, day_, time_=time_, return_timelist=return_timelist, return_all=False,
                     set_startloc=set_startloc, set_arriveloc=None, return_num=False, return_startloc=False,
                     return_weather=True,return_startloc_ans = return_startloc_ans, Y =Y)
        elif a == 4:
            ending = iq.get_weather(location=abst['from_'],return_day=abst['date'],return_temp = abst['return_temp'], return_how=abst['return_how'],return_change=abst['return_change'])
        elif a == 5:
            ending = iq.place_rec(location='北京市')
        elif a == 7:
            ending = abst
        #print('输出',end=':')
        f.write('输出：')
        #print(ending)
        f.write(ending+'\n')
        #print('-'*60)
        f.write('-'*100+'\n')
    f.close()
    print(train_path.split('.')[0],'done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

# In[8]:
from threading import Thread
def main_thread(path):
    t1=Thread(target=main,args=([path]))
    t1.start()
    

#train_path = 'train_weather.txt'
#main_thread('test_bus.txt')
#main_thread('train_weather.txt')
#main_thread('train_train.txt')
main_thread('test_flight.txt')
# In[ ]:
def sentence(i):
    import single_return_6 as sr
    import inquiry as iq
    print("输入:",i)
    nlu = sr.nlu(i)
    a = nlu[0]
    abst = nlu[1]
    #print(a,abst)
    if a == 1:
        from_ = abst['from_'].replace('市','').replace('省','').replace('县','')
        to_ = abst['to_'].replace('市','').replace('省','').replace('县','')
        day_ = abst['date']
        time_ = abst['time']
        set_startloc=abst['set_startloc']
        set_arriveloc = abst['set_arriveloc']
        return_num = abst['return_num']
        set_flight = abst['set_flight']
        return_startloc_ans = abst['return_startloc_ans']
        Y =abst['Y']
        return_timelist=abst['return_timelist']
        return_startloc = abst['return_startloc']
        ending = iq.get_flighttickets(from_, to_, day_, time_=time_, return_timelist=return_timelist, 
                 set_startloc=set_startloc, set_arriveloc=set_arriveloc, return_num=return_num, 
                  set_flight= set_flight, return_startloc=return_startloc,return_startloc_ans = abst['return_startloc_ans'],Y =abst['Y'])
    elif a == 2:
        from_ = abst['from_']
        to_ = abst['to_']
        day_ = abst['date']
        time_ = abst['time']
        return_timelist = abst['return_timelist']
        set_startloc=abst['set_startloc']
        set_arriveloc = abst['set_arriveloc']
        return_num = abst['return_num']
        return_G = abst['return_G']
        return_startloc = abst['return_startloc']
        return_startloc_ans = abst['return_startloc_ans']
        Y =abst['Y']
        ending = iq.get_traintickets(from_, to_, day_, time_=time_, return_timelist=return_timelist, 
                 set_startloc=set_startloc, set_arriveloc=set_arriveloc, return_num=return_num,
                 return_startloc=return_startloc, return_G=return_G,
                 return_all=False, return_weather=True,return_startloc_ans = abst['return_startloc_ans'],Y =abst['Y'])
    elif a == 3:
        from_ = abst['from_']
        to_ = abst['to_']
        day_ = abst['date']
        time_ = abst['time']
        return_timelist = abst['return_timelist']
        set_startloc=abst['set_startloc']
        set_arriveloc = abst['set_arriveloc']
        return_num = abst['return_num']
        return_startloc = abst['return_startloc']
        return_startloc_ans = abst['return_startloc_ans']
        Y =abst['Y']
        ending = iq.get_bustickets(from_, to_, day_, time_=time_, return_timelist=return_timelist, return_all=False,
                 set_startloc=set_startloc, set_arriveloc=None, return_num=False, return_startloc=False,
                 return_weather=True,return_startloc_ans = return_startloc_ans, Y =Y)
    elif a == 4:
        ending = iq.get_weather(location=abst['from_'],return_day=abst['date'],return_temp = abst['return_temp'], return_how=abst['return_how'],return_change=abst['return_change'])
    elif a == 5:
        ending = iq.place_rec(location='北京市')
    elif a == 7:
        ending = abst
    print('输出',end=':')
    print(ending)
    print('-'*60)
