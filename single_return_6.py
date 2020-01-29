#!/usr/bin/env python
# coding: utf-8

# In[23]:


import warnings
warnings.filterwarnings("ignore")


# In[24]:


#此模块用于对日期进行天数移动，包含了年月日修改与闰年修改
def move(s_time,num):
    date_need = int(s_time[-2:]) + num#根据代词移动后时间
    month = int(s_time[5:7])
    year = int(s_time[0:4])
    run = [1,3,5,7,8,10,12]
    f_run = [4,6,9,11]
    if date_need > 31 and month in run:#移动超出月底
        date_need -= 31
        if month != 12:
            month +=1
        elif month == 12:
            year += 1
            month = 1
    elif date_need >30 and month in f_run:
        date_need -= 30
        month +=1
    elif date_need>=29 and month == 2:
        month += 1
        if year % 4 == 0:
            if date_need >29:
                date_need -= 29
            elif date_need == 29:
                date_need = 29
        elif year % 4 !=0:
            date_need -= 28
    if month >=10 and date_need >=10:
        ending = str(year) +"-"+str(month)+"-"+str(date_need)
    elif month <10 and date_need >=10:
        ending = str(year) +"-0"+str(month)+"-"+str(date_need)
    elif month >=10 and date_need <10:
        ending = str(year) +"-"+str(month)+"-0"+str(date_need)
    elif month <10 and date_need <10:
        ending = str(year) +"-0"+str(month)+"-0"+str(date_need)
    return ending


# In[25]:


#此模块为根据日期代词进行日期推测
def dc_move(s_time,d):#已知代词根据代词进行天数移动
    #import time
    #s_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    daici = ["今天","明天","后天","大后天","大大后天"]
    Delayoradvance = [0,1,2,3,4]
    for j in range(len(daici)):
        if daici[j] == d:
            num = Delayoradvance[j]
    ending = move(s_time,num)
    return ending


# In[26]:


#此模块用于识别句中代词并进行日期推测，最多可识别两个日期
def ir_date(str_):
    daici = ["今天","明天","后天","大后天","大大后天"]
    Delayoradvance = [0,1,2,3,4]
    d_date = []
    for i in daici:
        m = str_.find(i)
        if m != -1:
            if i != "后天" and i != "大后天":
                d_date.append(i)
            elif i == "后天" or i == "大后天":
                try:
                    l = str_[m-1]
                    if l != "大":
                        d_date.append(i)
                except:
                    d_date.append(i)
    import time
    s_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = []
    if len(d_date) != 0:#存在天数代词
        if len(d_date) == 1:#只存在一个天数代词
            d = d_date[0]
            date.append(dc_move(s_time,d))
        elif len(d_date) >1:#存在一个以上代词
            for k in d_date:
                date.append(dc_move(s_time,k))       
    return date


# In[28]:


#此模块用于对问句中涉及星期内容进行处理，最多可输入两个
def week(str_):
    week = ["星期","礼拜","周"]
    week_Chi = ["一","二","三","四","五","六","日","1","2","3","4","5","6","天"]
    from datetime import datetime
    today = datetime.now().weekday() + 1
    end = []
    for i in week:
        m = str_.find(i)
        if m != -1:
            #print("first")
            if str_[m:m+2] == i:
                c=str_[m+2]#周几
            elif str_[m:m+1] == i:
                c=str_[m+1]
            try:#是否转周
                n = str_[m-2:m].find("下")
                z = str_[m-2:m].find("转")
            except:
                n = -1
                z = -1
            c_n = week_Chi.index(c)+1
            if c_n >7:
                c_n -= 7
            if c_n >= today:#大于今天
                if n != -1 or z != -1:#是下周
                    delay = c_n+7-today
                elif n == -1 and z == -1:#不是下周
                    delay = c_n-today
                end.append(delay)
            elif c_n < today:
                delay = 7-today+c_n
                end.append(delay)
            #print(end)
            str_1 = str_[m+2:]
            #print("删减",str_1)
            for u in week:
                v = str_1.find(u)
                if v != -1:
                    if str_1[v:v+2] == u:
                        cc=str_1[v+2]#周几
                    elif str_1[v:v+1] == u:
                        cc=str_1[v+1]
                    try:#是否转周
                        n = str_1[v-2:v].find("下")
                        z = str_1[v-2:v].find("转")
                    except:
                        n = -1
                        z = -1
                    try:
                        cc_n = week_Chi.index(cc)+1
                        if cc_n >7:
                            cc_n -= 7
                        if cc_n >= today:#大于今天
                            if n != -1 or z != -1:#是下周
                                delay = cc_n+7-today
                            elif n == -1 and z == -1:#不是下周
                                delay = cc_n-today
                            end.append(delay)
                        elif cc_n < today:
                            delay = 7-today+cc_n
                            end.append(delay)
                    except:
                           pass
    import time
    s_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    ending = []
    for q in end:
        ending.append(move(s_time,q))
    return ending


# In[58]:


#此模块用于对标准输入的时间的提取
def stand_time(text):
    import re
    text_ori = text
    cc = text.find('半')
    if cc > 0 and text[cc-1] == '点':
        text = text.replace("半","30分")
    text = text.replace("一刻","15分").replace("二刻","30分").replace("三刻","45分")
    text = text.replace(" ","")
    text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("号"," ").replace("/", "-").strip()
    text = text.replace("点",":").replace("：",":").replace("时",":")
    text = text.replace("上午","").replace("下午","").replace("晚上","").replace("晚","").replace("夜","")
    chinese = ["零","一","二","三","四","五","六","七","八","九"]
    for i in range(len(chinese)):
        text = text.replace(chinese[i],str(i))
        if chinese[i] in text:
            text = text.replace("十","1")
        else:
            text = text.replace("十","10")
    if "秒" in text:
        text = text.replace("分",":").replace("秒","")
    elif "分" in text and "秒" not in text:
        text = text.replace("分"," ")
    text = re.sub("\s+", " ", text)
    t = ""
    regex_list = [
        # 2013年8月15日 22:46:21
        "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",
        # "2013年8月15日 22:46"
        "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})",
        # "2013年8月15日 22:"
        "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:)",
        # "2014年5月11日"
        "(\d{4}-\d{1,2}-\d{1,2})",
        # "2014年5月"
        "(\d{4}-\d{1,2})",
        #12月15日
        "(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",
        "(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})",
        "(\d{1,2}-\d{1,2} \d{1,2})",
        "(\d{1,2}-\d{1,2})",
        #3号 
        "(\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",
        "(\d{1,2} \d{1,2}:\d{1,2})",
        "(\d{1,2} \d{1,2})",
       
        #22:23
        "(\d{1,2}:\d{1,2} )",
        "(\d{1,2}:)",
        "(\d{1,2} )", 
     ]
    for regex in regex_list:
        t = re.search(regex, text)
        if t:
            t = t.group(1)
            if t[-1] == " ":
                t = t.replace(" ","")
            #print('｜',t,'｜')
            if t.count("-") == 0:#无年月只有日或只有时间
                import time
                st_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))#2019-12-10
                if " " not in t:
                    #print('no space',t)
                    if "日"in text_ori or "号" in text_ori:#只有日期
                        if len(t) == 1:
                            t = st_time[:8]+"0"+t
                        elif len(t) == 2:
                            t = st_time[:8]+t
                        elif " " in t and ":" not in t:#4 2
                            if len(t) == 3:#3 1
                                t = st_time[:8]+"0"+t[:2]+"0"+t[-1]+":00"
                            elif len(t) == 4 and t[1] == " ":#3 12
                                t = st_time[:8]+"0"+t+":00"
                            elif len(t) == 4 and t[2] == " ":#13 2
                                t = st_time[:8]+t[:3]+"0"+t[-1]+":00"
                                return t
                            elif len(t) == 5:
                                t = st_time[:8]+t+":00"
                        elif " " in t and ":" in t:
                            if len(t) == 6:#3 1:22
                                t = st_time[:8]+"0"+t[:2]+"0"+t[2:]
                            elif len(t) == 7 and t[1] == " ":#3 12:22
                                t = st_time[:8]+"0"+t
                            elif len(t) == 7 and t[2] == " ":#13 2:22
                                t = st_time[:8]+t[:2]+"0"+t[2:]
                            elif len(t) == 8:#13 21:22
                                t = st_time[:8]+t
                    if "点" in text_ori or "时" in text_ori:#只有时间
                        #print('11',t)
                        if len(t) == 1:
                            t = st_time+" "+"0"+t+":00"
                        elif len(t) == 2:
                            if ":" in t:
                                t = st_time+" 0"+t+"00"
                            elif ":" not in t:
                                t = st_time+" "+t+":00"
                        elif len(t) == 3:#1:2 12:
                            if t[1] == ":":
                                t = st_time+" 0"+t[:-1]+"0"+t[-1]
                            elif t[-1] == ":":
                                t = st_time+" "+t+"00"
                        elif len(t) == 4:#1:23 21:9
                            if t[1] == ":":
                                t = st_time+" 0"+t
                            elif t[2] == ":":
                                t = st_time+" "+t[:-1]+"0"+t[-1]
                        elif len(t) == 5:
                            t = st_time+" "+t
                elif " " in t:
                    n = t.find(" ")
                    t1 = t[:n]
                    t2 = t[n+1:]
                    if len(t1) == 1:
                        t1 = "0"+t1
                    if len(t2) == 1:
                        t2 = "0"+t2+":00"
                    elif len(t2) == 2:
                        if ":" in t2:
                            t2 = "0"+t2+"00"
                        elif ":" not in t2:
                            t2 = t2+":00"
                    elif len(t2) == 3:#12: 1:3
                        if t2[-1] == ":":
                            t2 = t2+"00"
                        elif t2[1] == ":":
                            t2 = "0"+t2[:-1]+"0"+t2[-1]
                    elif len(t2) == 4:#12:3
                        if t2[2] == ":":
                            t2 = t2[:-1]+"0"+t2[-1]
                        elif t2[1] == ":":
                            t2 = "0"+t2
                    t = st_time[:8]+t1+" "+t2
            elif t.count("-") == 1:
                #print('o',t)
                if " " in t:
                    k = t.find(" ")
                    t1 = t[:k]
                    if t1[-2] == "-":
                        t1 = t1[:-1]+"0"+t1[-1]
                        t = t1+t[k:]
                elif " " not in t:
                    if t[-2] == "-":
                        t = t[:-1]+"0"+t[-1]
                #print('e',t)
                if t.find("-") == 4:#只有年月 2014-2
                    import time
                    st_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    if len(t) == 7:
                        t = t+"-"+st_time[-2:]
                    elif len(t) == 6:
                        t = t[:5]+"0"+t[-1]+"-"+st_time[-2:]
                elif t.find("-") == 2 :#只有月日
                    import time
                    st_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    t = st_time[:5]+t
                elif t.find("-") == 1 :#只有月日
                    import time
                    st_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                    t = st_time[:5]+"0"+t 
                if " " in t:
                    n = t.find(" ")
                    t2 = t[n+1:]
                    if len(t2) == 1:
                        t2 = "0"+t2+":00"
                    elif len(t2) == 2:
                        if ":" not in t2:
                            t2 = t2+":00"
                        elif ":"in t2:
                            t2 = "0"+t2+"00"
                    elif len(t2) == 3:#12: 1:3
                        if t2[-1] == ":":
                            t2 = t2+"00"
                        elif t2[1] == ":":
                            t2 = "0"+t2[:-1]+"0"+t2[-1]
                    elif len(t2) == 4:#12:3
                        if t2[2] == ":":
                            t2 = t2[:-1]+"0"+t2[-1]
                        elif t2[1] == ":":
                            t2 = "0"+t2
                    t = t[:n]+" "+t2
            elif t.count("-") == 2:
                if " " not in t:
                    if len(t) == 8:#2014-2-5
                        t = t[:5]+"0"+t[5:7]+"0"+t[7:]
                    elif len(t) == 9:
                        if t[-2] == "-":
                            t = t[:-1]+"0"+t[-1]
                        else:
                            t = t[:5]+"0"+t[5:]
                    else:
                        t = t
                elif " " in t:
                    n = t.find(" ")
                    t1 = t[:n]
                    t2 = t[n+1:]
                    if len(t1) == 8:#2014-2-5
                        t1 = t1[:5]+"0"+t1[5:7]+"0"+t1[7:]
                    elif len(t1) == 9:
                        if t1[-2] == "-":
                            t1 = t1[:-1]+"0"+t1[-1]
                        else:
                            t1 = t[:5]+"0"+t1[5:]
                    else:
                        t1 = t1
                    if len(t2) == 1:
                        t2 = "0"+t2+":00"
                    elif len(t2) == 2:
                        if ":" not in t2:
                            t2 = t2+":00"
                        elif ":" in t2:
                            t2 = "0"+t2+"00"
                    elif len(t2) == 3:
                        if t2[-1] == ":":
                            t2 = t2+"00"
                        elif t2[-2] == ":":
                            t2 = "0"+t2[:-1]+"0"+t2[-1]
                    #6:15
                    elif len(t2) == 4:
                        if t2[1] == ":":
                            t2 = "0"+t2
                        elif t2[2] == ":":
                            t2 = t2[:-1]+"0"+t2[-1]
                    elif len(t2) == 5:
                        t2 = t2
                    elif len(t2)>5:
                        t2 = t2[:5]
                    t = t1+" "+t2
            return t


# In[50]:


#此模块用于对一句话中的时间进行提取
def time_extract(str_):
    stand = stand_time(str_)
    add = ['下午','晚上','夜']
    if stand:
        if len(stand) == 16:#2019-12-22 19:32
            for i in add:
                if i in str_:
                    hour = int(stand[11:13])
                    if hour<=12:
                        hour += 12
                        stand = stand[:11]+str(hour)+stand[-3:]
    ir_date_lst = ir_date(str_)
    week_lst = week(str_)
    if ir_date_lst == [] and week_lst == []:
        if stand:
            if " " in stand:
                l = stand.split(" ")
                return l
            else:
                if '上午' in str_:
                    return [stand,['08','09','10','11']]
                elif '中午' in str_:
                    return [stand,['12','13','14']]
                elif '下午' in str_:
                    return [stand,['15','16','17','18']]
                elif '晚上' in str_:
                    return [stand,['18','19','20','21','22','23','24']]
                else:
                    return [stand," "]
        elif not stand:
            import time
            st_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if '上午' in str_:
                return [st_time,['08','09','10','11']]
            elif '中午' in str_:
                return [st_time,['12','13','14']]
            elif '下午' in str_:
                return [st_time,['15','16','17','18']]
            elif '晚上' in str_:
                return [st_time,['18','19','20','21','22','23','24']]
            else:
                return [st_time," "]
    elif ir_date_lst != []:
        t1 = ir_date_lst[0]
        if stand:
            if len(stand)>len(t1):
                n = stand.find(" ")
                time = t1+stand[n:]
            else:
                time = t1
        else:
            time = t1
        if " " in time:
            l = time.split(" ")
            return l
        elif " " not in time:
            if '上午' in str_:
                return [time,['08','09','10','11']]
            elif '中午' in str_:
                return [time,['12','13','14']]
            elif '下午' in str_:
                return [time,['15','16','17','18']]
            elif '晚上' in str_:
                return [time,['18','19','20','21','22','23','24']]
            else:
                return [time," "]
    elif week_lst != []:
        t2 = week_lst[0]
        if stand:
            if len(stand)>len(t2):
                n = stand.find(" ")
                time = t2+stand[n:]
            else:
                time = t2
        else:
            time = t2
        if " " in time:
            l = time.split(" ")
            return l
        elif " " not in time:
            if '上午' in str_:
                return [time,['08','09','10','11']]
            elif '中午' in str_:
                return [time,['12','13','14']]
            elif '下午' in str_:
                return [time,['15','16','17','18']]
            elif '晚上' in str_:
                return [time,['18','19','20','21','22','23','24']]
            else:
                return [time," "]


# In[31]:


#此模块用于识别城市与时间
import cpca
import warnings
warnings.filterwarnings("ignore")
def city_distinguish(str_):
    ending = []#最后输出为三元列表，分别为出发地，目的地，时间，时间可能因输入多个时间而形式为列表，请识别类型后处理
    c = [str_]
    df1 = cpca.transform(c,cut=False,open_warning=False)
    prov1 = df1.iloc[0,0]
    city1 = df1.iloc[0,1]
    city2 = df1.iloc[0,2]
    if city2 != "":
        city1 = city2
    if prov1 == city1:
        n = prov1.find("省")
        str_ = str_.replace(prov1[:n],"")
        str_ = str_.replace(prov1[:2],"")
    elif prov1 != city1:
        n = prov1.find("省")
        m = city1.find("市")
        str_ = str_.replace(prov1[:n],"").replace(city1[:m],"")
        str_ = str_.replace(prov1[:2],"").replace(city1[:2],"")
    c1 = [str_]
    #print(c1)
    df2 = cpca.transform(c1,cut=False,open_warning=False)
    #print(df2)
    if df2.iloc[0,0] != '':
        if prov1 != city1:
            start_city = city1
        elif prov1 == city1:
            start_city = prov1
        if df2.iloc[0,0] != df2.iloc[0,1]:
            destination = df2.iloc[0,1]
        elif df2.iloc[0,0] == df2.iloc[0,1]:
            destination = df2.iloc[0,0]
        #print("出发地:",start_city,"目的地:",destination)
        ending.extend([start_city,destination])
    elif df2.iloc[0,0] == '':
        start_city = "您好像没有输入出发地"
        if prov1 != city1 and city1 != "":
            destination = city1
        elif prov1 == city1:
            destination = prov1
        elif prov1 != "" and city1 == "":
            destination = prov1
        #print(start_city,"目的地:",destination)
        ending.extend(["北京市",destination])
    time = time_extract(str_)
    ending.extend(time)
    return ending


# In[32]:


def ticket_dist(str_):
    a = []#最后返回a为数组类型，其中元素代表订票需求，1飞机2火车3汽车
    train = ["火车票","火车","动车","高铁","列车"]
    flight = ["航班","飞机","机票","飞机票","飞","航","东方","奥凯","春秋"]
    bus = ["坐车","汽车","的车"]
    lst_dis = [0,0,0]
    flight_find = [str_.find(i) for i in flight]
    f = 0
    for j in flight_find:
        if j != -1:
            f += 1
    if f > 0:
        #print("flight order need")
        lst_dis[0] = 1
    train_find = [str_.find(i) for i in train]
    t = 0
    for j in train_find:
        if j != -1:
            t += 1
    if t > 0:
        #print("train order need")
        lst_dis[1] = 1   
    bus_find = [str_.find(i) for i in bus]
    b = 0
    for j in bus_find:
        if j != -1:
            b += 1
    if b > 0:
        #print("bus order need")
        lst_dis[2] = 1
    for k in range(len(lst_dis)):
        if lst_dis[k] ==1:
            a.append(k+1)
    if a == []:
        #print("未输入购票意图，返回所有类型票务信息")
        a.extend([1,2,3])
    return a


# In[33]:


def city_aim(str_):
    a = []
    aim = []
    time = 0
    weather = ["天气","气候","天儿","冷","热","暖","升温","降温","刮风","节气","数九","预报","雨",'阳光','风',"霜","露",
               "雪","冰雹","温度","摄氏度","华氏度","舒适","湿度","几度"]
    ording = ["火车","动车","高铁","列车","航班","飞机","机票","飞机票","飞","航","东方","奥凯","春秋","坐车","汽车",
              "的车","前往","去","到","出发","车票"]
    recommend = ["好玩","景","旅游","必去","推荐","去哪","公园","游览","日游","旅游区","山","石窟","博物馆","公馆",
                 "陵","古镇","祠","宫","大院","寺","古城","田园","故居","寨","桥","洞","阁","峰","会馆","古村落",
                 "遗址","公园","岛","旧居","楼群","温泉","遗产","墓","市场","渠","故里","庙","运河","演出","府",
                 "孔林","宅","石头厝","热带雨林","滑雪场","观光塔","峡","瀑布","乡","坪","潭","乐园","湾","岭",
                 "湖","坡","源","文博园","雕塑","峡谷","金顶","塔","亭","署","赤壁","书院","谷"]
    judge_dic = {'weather':weather,'ording':ording,'recommend':recommend}
    for i in judge_dic:
        for j in judge_dic[i]:
            if j in str_:
                if i != 'ording':
                    aim.append(i)
                elif i == 'ording':
                    if 'ording' not in aim:
                        aim.append(i)
    if 'weather' in aim:
        if 4 not in a:
            a.append(4)
        time = time_extract(str_)
    if 'recommend' in aim:
        if 5 not in a:
            a.append(5)
    if 'ording' in aim:
        l = ticket_dist(str_)
        if len(l) == 1:
            a.append(l[0])
        elif len(l) >= 2:
            a.append(l)
        time = time_extract(str_)
    return a,time


# In[34]:


#ording 0,weather 1
"""svmpath = 'bert_svm.pickle.dat'
xgbpath = 'bert_xgboost.pickle.dat'
rpath = '/Users/wangxuefei/Desktop/文本挖掘与自然语言处理/bert_rf.pickle.dat'
def bert_ml(str_,svmpath,xgbpath,rpath):
    import pickle
    svm_model = pickle.load(open(svmpath,'rb'))
    xgb_model = pickle.load(open(xgbpath,'rb'))
    #rf_model = pickle.load(open(rpath,'rb'))
    
    from bert_serving.client import BertClient
    bc = BertClient()
    test_x = bc.encode([str_])
    spre = svm_model.predict(test_x)
    xpre = xgb_model.predict(test_x)
    #rpre = rf_model.predict(test_x)
    return spre[0],xpre[0]#,rpre[0]"""


# In[35]:


#这一模块导入bert进行细粒度分析
import warnings
warnings.filterwarnings("ignore")
"""import os
import sys
#from bert_serving.client import BertClient
#from sklearn.metrics.pairwise import cosine_similarity
import time

#bc = BertClient()

THRESHOLD = 0.89

choice_map = {
    'j_ret_start' : ["从哪站","在哪站","出发站","哪一站","哪些站","可选站","可供选择站","可以出发的火车站","哪个机场",
                   "从哪个机场","哪些机场出发","出发机场","起始机场","哪个机场","到哪","从哪"],
    'instant' : ['现在','当前','此时','实时','此刻','当时'],
    'timelst' : ["时刻","时间","列表","表格","发车表","分布表","列车表","班次","几趟",
               "几列","多少","几班","几次","几点","时候","数"],
    'numlst': ["多少班次","几趟","几列","多少次","多少趟","几班","多少班","几次"]
}

choice_list_raw = []#存放例句
choice_id2tag = {-1:'NO_MATCH'}#句子编号-句子类别
cnt_i = 0
for key in choice_map.keys():
    tag_l = choice_map[key]#tag_1：例句
    if len(tag_l) > 0:
        for i in range(len(tag_l)):
            choice_list_raw.append(tag_l[i])
            choice_id2tag[cnt_i] = key
            cnt_i += 1

choice_list = [' '.join(list(i)) for i in choice_list_raw]


choice_arr = bc.encode(choice_list)

def get_similarity(qs):
    qs_seg = ' '.join(list(qs))
    qs_arr = bc.encode([qs_seg])
    max_score = 0
    max_i = -1
    for i in range(len(choice_list)):
        sim = cosine_similarity(choice_arr[i].reshape(-1, 768), qs_arr)
        # print('[{} | {}]\tsimilarity\t:\t{}'.format(qs, choice_list[i], sim[0][0]))
        if sim[0][0] > max_score:
            max_score = sim[0][0]
            max_i = i
    if max_score > THRESHOLD:
        return max_score, choice_list_raw[max_i], max_i
    else:
        return 0, '不知道你说的啥', -1"""


# In[36]:


def county(str_):
    import jieba                                          
    jieba.load_userdict("CoreNatureDictionary.txt")
    jieba.add_word("台中")
    import jieba.posseg as pg
    w_seg = pg.cut(str_)
    end = ""
    lst = []
    cx = ['nr','ns','s']
    for w in w_seg:
        if w.flag in cx:
            lst.append(w.word)
    for i in lst:
        i = i+"县"
        import cpca
        df = cpca.transform([i])
        if df.iloc[0,2] == i:
            end = i
    if end == "":
        for i in lst:
            end = end+i
    if lst == []:
        end = "北京"
    return end 


# In[37]:


def f_company_des(str_):
    fly_company = ["中国国际航空公司","中国南方航空公司","西部航空有限责任公司","东方航空公司","厦门航空公司",
                   "山东航空公司","成都航空公司","上海航空公司","深圳航空公司","中国新华航空公司","幸福航空责任有限公司",
                   "云南航空公司","新疆航空公司","四川航空公司","中原航空公司","武汉航空公司","贵州航空公司","海南航空公司",
                   "中国通用航空公司","南京航空公司","浙江航空公司","长城航空公司","福建航空公司","长安航空公司",
                   "浙江长龙航空公司","首都航空公司","吉祥航空公司","春秋航空公司","天津航空公司","华夏航空有限公司",
                   "国航","南航","西航","东航","东方航空","厦航","厦门航空","山航","山东航空","成都航空","成航","海航",
                   "深圳航空","深航","新华","幸福","云航","新疆航空","川航","浙江航空","津航","浙航","长龙","首航",
                   "吉祥","春秋","华夏"]
    for i in fly_company:
        if i in str_:
            return i


# In[47]:


def nlu(str_):
    #识别出两个城市则直接认为是输出两个城市间订票信息:1机票2火车票3汽车票
    #只有一个城市需要识别：4天气5目的地是北京：景点推荐
    #多种需求：8
    #需求不明确：7
    import pandas as pd
    cpath = 'city.csv'
    cc = pd.read_csv(cpath)
    abst = {'from_':None,'to_':None,'date':None,'time':None,'return_timelist':None,'return_startloc_ans':None,
            'set_startloc':None,'set_arriveloc':None,'return_num':None,'tag':None,'Y':None,'return_change':None,
            'set_flight':None,'return_startloc':None,'return_G':None,'return_temp':None,'return_how':None}
    city = [cc.iloc[i,0] for i in range(len(cc))]
    #这一模块用来确定是否输出时刻表
    timelst = ["时刻","时间","列表","表格","发车表","分布表","列车表","班次","几趟",
               "几列","多少","几班","几次","几点","时候","数"]
    for i in timelst:
        if i in str_:
            abst['return_timelist'] = True
            
    #这一模块用来决定是否只输出次数
    numlst = ["多少班次","几趟","几列","多少次","多少趟","几班","多少班","几次"]
    for i in numlst:
        if i in str_:
            abst['return_num'] = True
            
    #这一模块用来决定是否只输出高铁
    G_fea = ["高铁","动车","G","城际"]
    for i in G_fea:
        if i in str_:
            abst['return_G'] = True
            
    #这一模块用来决定是否回答有票
    if "有" in str_ and "几" not in str_:
        abst['Y'] = True
    
    #startloc:返回车站，startloc+answer：返回车站+一个回答
    j_ret_start = ["从哪站","在哪站","出发站","哪一站","哪些站","可选站","可供选择站","可以出发的火车站","哪个机场",
                   "从哪个机场","哪些机场出发","出发机场","起始机场","哪个机场","到哪","从哪"]
    for i in j_ret_start:
        if i in str_:
            abst['return_startloc'] = True
    start_ans = ["怎么","如何"]
    for i in start_ans:
        if i in str_:
            abst['return_startloc_ans'] = True
            
    #这一模块用来识别是否输出实时天气
    instant = ['现在','当前','此时','实时','此刻','当时']
    for i in instant:
        if i in str_:
            abst['return_temp'] = True
            
    #这一模块用来识别是否变换天气输出顺序
    change = ['好不好','冷不冷','热不热']
    for i in change:
        if i in str_:
            abst['return_change'] = True
            
    #这一模块调用bert进行细粒度区分
    #ans = get_similarity(str_)
    
    #这一模块调用bert_ml进行意图识别
    #category = bert_ml(str11,svmpath,xgbpath,rpath)
            
    #这一模块用来识别特殊天气需求
    lst = []
    special = {'雨' :['雨'],
    '雪' : ['雪'],
    '雾霾': ['霾'],
    '风':  ['风'],
    '空气': ['空气','质量'],
    '冷不冷':['冷吗']}
    for i in special:
        for j in special[i]:
            if j in str_:
                lst.append(i)
    if len(lst) == 1:
        abst["return_how"] = lst[0]
    elif len(lst) >1:
        abst["return_how"] = lst
            
    #这一模块用来进行机场识别
    fl_com = f_company_des(str_)
    if fl_com:
        l = len(fl_com)
        n = str_.find(fl_com)
        str_new = str_[n+l:]
        try:
            import jieba
            seg = jieba.lcut(str_new)
            a = int(seg[0])
            abst['set_flight'] = fl_com+seg[0]
        except:
            abst['set_flight'] = fl_com
            
            
    city_lst = []
    for i in city:
        n = str_.find(i)
        if n != -1:
            city_lst.append(i)
            
    #这一模块用来调整当识别出两个城市时的先后顺序
    if len(city_lst) == 2 and " " not in city_lst:
        n1 = str_.find(city_lst[0])
        n2 = str_.find(city_lst[1])
        if n2 < n1 and n2 != -1:
            city_lst = [city_lst[1],city_lst[0]]
    
    #这一模块用来识别当只有一个城市时，该城市是出发还是到达
    start = ["从","出发","离开","开始","启程","起步"]
    if len(city_lst) == 1:
        for i in start:
            if i in str_:
                city_lst.append(" ")
    if len(city_lst) == 1:
        city_lst = [" ",city_lst[0]]
        
    #这一模块用来判断用户是否输入了始发站或终点站
    station = []
    judge_station = ["机场","南站","北站","西站","东站","白云","虹桥","云岗","首都","浦东","白云","双流",
                     "宝安","长水","咸阳","江北","萧山","北仑","大兴","新郑","北郊","站"]
    import jieba
    str_seg = jieba.lcut(str_)
    for i in range(len(str_seg)):
        for j in judge_station:
            if j in str_seg[i]:
                if str_seg[i-1] in city:
                    sta = str_seg[i-1]+j
                    station.append(sta)
                elif len(str_seg[i])>=4:
                    station.append(str_seg[i])
    if len(station) == 1:
        abst['set_arriveloc'] = station[0]
    if len(station) == 2:
        abst['set_startloc'] = station[0]
        abst['set_arriveloc'] = station[1]
    #print(city_lst)    
    if len(city_lst) >= 2:#存在城市；按照城市个数进行分类
        #print(city_lst)
        if " " not in city_lst:#两城市直接订票
            ording_type = ticket_dist(str_)
            time = time_extract(str_)
            abst['from_'] = city_lst[0]
            abst['from_'] = abst['from_'].replace("市","").replace("省","").replace("县","")
            abst['to_'] = city_lst[1]
            abst['to_'] = abst['to_'].replace("市","").replace("省","").replace("县","")
            abst['date'] = time[0]
            if time[1] !=" ":
                abst['time'] = time[1]
            if len(ording_type) == 1:
                if ording_type[0] == 1:
                    today = time_extract("今天")
                    if abst['date'] == today[0] and "今" not in str_:
                        abst['date'] = move(today[0],7)
                elif ording_type[0] == 2:
                    today = time_extract("今天")
                    if abst['date'] == today[0] and "今" not in str_:
                        abst['date'] = move(today[0],0)
                elif ording_type[0] == 3:
                    today = time_extract("今天")
                    if abst['date'] == today[0] and "今" not in str_:
                        abst['date'] = move(today[0],1)
                return ording_type[0],abst
            elif len(ording_type) >1:
                return 8,ording_type,abst
        elif city_lst[0] == " " and city_lst[1] != " ":#只有目的地
            aim,time = city_aim(str_)
            if len(aim) == 1:
                if aim[0] == 4:#天气查询
                    abst['from_'] = city_lst[1]
                    abst['from_'] = abst['from_'].replace("市","").replace("省","").replace("县","")
                    abst['date'] = time[0]
                    return 4,abst
                elif aim[0] in [1,2,3]:
                    if city_lst[1] !="北京":
                        abst['from_'] = "北京"
                        abst['to_'] = city_lst[1]
                        abst['to_'] = abst['to_'].replace("市","").replace("省","").replace("县","")
                        time = time_extract(str_)
                        abst['date'] = time[0]
                        if time[1] != " ":
                            abst['time'] = time[1]
                        return aim[0],abst  
                    elif city_lst[1] == "北京":
                        abst['to_'] = '北京'
                        str_return = '您想从哪里出发呀？什么时候出发呢？'
                        return 7,str_return,abst
                elif aim[0] == [1,2,3]:
                    if city_lst[1] !="北京":
                        abst['from_'] = "北京"
                        abst['to_'] = city_lst[1]
                        abst['to_'] = abst['to_'].replace("市","").replace("省","").replace("县","")
                        time = time_extract(str_)
                        abst['date'] = time[0]
                        if time[1] != " ":
                            abst['time'] = time[1]
                        str_return = "那你想从哪里出发呀？还有还有，你想怎么去呢？"
                        return 7,str_return,abst  
                    elif city_lst[1] == "北京":
                        abst['to_'] = '北京'
                        str_return = '您想从哪里出发呀？还有还有，你想怎么去呢?'
                        return 7,str_return,abst  
            elif len(aim)>1:
                abst['from_'] = city_lst[1]
                abst['from_'].replace("市","").replace("省","").replace("县","")
                abst['date'] = time[0]
                return 4,abst
        elif city_lst[0] != " " and city_lst[1] == " ":#只有出发地
            abst['from_'] = city_lst[0]
            abst['from_'].replace("市","").replace("省","").replace("县","")
            return 7,'请问你的目的地是？出发时间是？',abst
    elif city_lst == []:
        a,b = city_aim(str_)
        #print(a,b)
        if a != []:
            if a[0] == 4:
                st = county(str_)
                abst['from_'] = st
                t = time_extract(str_)
                abst['date'] = t[0]
                return 4,abst
            elif a[0] == 5:
                st = county(str_)
                abst['from_'] = st
                return 5,abst
            elif a[0] == 1:
                return 7,'请问你想从哪出发？坐飞机去哪里呀？订票网址：https://jipiao.8684.cn'
            elif a[0] == 2:
                return 7,'请问你想从哪出发？坐火车去哪里呀？订票网址：https://huoche.8684.cn'
            elif a[0] == 1:
                return 7,'请问你想从哪出发？坐汽车去哪里呀？订票网址：http://qiche.114piaowu.com'
            elif a[0] == [1,2,3]:
                return 7,'请问你想从哪里出发，去哪里呢？还有还有，你想怎么去呀？',abst
        elif a == []:
            return 7,'你说了什么，我好像不明白'


# In[57]:


nlu("查一下明天下午10点半从北京飞往珠海的飞机")


# In[ ]:




