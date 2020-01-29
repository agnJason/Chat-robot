#!/usr/bin/env python
# coding: utf-8

# In[35]:

 
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from bs4 import BeautifulSoup as bs
import warnings
warnings.filterwarnings("ignore")
import re
import numpy as np
import json
global chaxun
import random
import pickle
chaxun = "您还没有开始查询呢！"

weather_huancun={}
# In[36]:


def get_chaxun():
    global chaxun
    return chaxun
def set_chaxun(type_):
    global chaxun
    if type_==0:
        chaxun = "您还没有开始查询呢！"
    if type_==1:
        chaxun = "正在查询……"
def load_dict(filename):
    '''load dict from json file'''
    with open(filename,"r") as json_file:
	    dic = json.load(json_file)
    return dic

def get_useable_ip():
    import requests
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
            'Host': 'fs.xicidaili.com'
            }
    response = requests.get('https://www.xicidaili.com/nt', headers = headers)
    soup = bs(response.text)
    http = []
    https = []
    lst = soup.find(id='ip_list').find_all('tr')
    for n in lst:
        n_split = n.text.split()
        if n_split[4]=='HTTPS':
            https.append(':'.join(n_split[0:2]))
        elif  n_split[4]=='HTTP':
            http.append(':'.join(n_split[0:2]))
    return http, https
def save_weather_huancun():
    with open("weather_huancun.file", "wb") as f:
        pickle.dump(weather_huancun, f)
def load_weather_huancun():
    with open("weather_huancun.file", "rb") as f:
        b = pickle.load(f)
    return b
def create_weather_huancun():
    print('天气预加载所需时间长（约30分钟），请耐心等待。')
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=option)
    browser.get("https://www.baidu.com")
    def today():
        today = weathers[0].text.strip().split()
        try:
            today_time = ' '.join(today[0:2])
            today_ss = today[3]+today[4]+' '+today[5]
            today_weather = ''.join(today[6:9])+' '+today[9] + ' '+today[10]
            try:
                today_weather=today_weather+" 空气质量：{}{}".format(today[11],today[12])
            except:
                True
        except:
            today_time=' '.join(today[0:2])
            today_ss='暂时无法获取当前温度。'
            today_weather=''.join(today[3:6])+' '+today[6] + ' '+today[7]
        return today_time, today_ss, today_weather
        
    def untoday(n):
        try:
            tommorrow = weathers[n].text.strip().split()
            tommorrow_time = ' '.join(tommorrow[0:2])
            tommorrow_weather = ''.join(tommorrow[2:5])+' '+tommorrow[5] + ' '+tommorrow[6]
            try:
                tommorrow_weather = tommorrow_weather + " 空气质量：{}".format(tommorrow[7])
            except:
                True
            return tommorrow_time, tommorrow_weather
        except:
            True
    china_city =  ['北京市', '天津市', '石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市',\
                     '承德市', '沧州市', '廊坊市', '衡水市', '太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市',\
                     '晋中市', '运城市', '忻州市', '临汾市', '吕梁市', '呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市',\
                     '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市', '乌兰察布市', '兴安盟', '锡林郭勒盟', '阿拉善盟', '沈阳市',\
                     '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦市',\
                     '铁岭市', '朝阳市', '葫芦岛市', '长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '松原市',\
                     '白城市', '延边朝鲜族自治州', '哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市',\
                     '佳木斯市', '七台河市', '牡丹江市', '黑河市', '绥化市', '大兴安岭地区', '上海市', '南京市', '无锡市', '徐州市',\
                     '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市', '杭州市',\
                     '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市', '舟山市', '台州市', '丽水市', '合肥市',\
                     '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市', '阜阳市', '宿州市',\
                     '六安市', '亳州市', '池州市', '宣城市', '福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市',\
                     '龙岩市', '宁德市', '南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市',\
                     '抚州市', '上饶市', '济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市',\
                     '威海市', '日照市', '莱芜市', '临沂市', '德州市', '聊城市', '滨州市', '菏泽市', '长沙市', '株洲市', '湘潭市',\
                     '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市', '湘西土家族苗族自治州',\
                     '广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市',\
                     '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '东莞市', '中山市', '潮州市', '揭阳市', '云浮市', '南宁市',\
                     '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市', '贺州市', '河池市',\
                     '来宾市', '崇左市', '重庆市', '成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市',\
                     '内江市', '乐山市', '南充市', '眉山市', '宜宾市', '广安市', '达州市', '雅安市', '巴中市', '资阳市', '阿坝藏族羌族自治州',\
                     '甘孜藏族自治州', '凉山彝族自治州', '贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市', '黔西南布依族苗族自治州',\
                     '黔东南苗族侗族自治州', '黔南布依族苗族自治州', '昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市',\
                     '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州', '大理白族自治州', '德宏傣族景颇族自治州',\
                     '怒江傈僳族自治州', '迪庆藏族自治州', '拉萨市', '日喀则市', '昌都市', '林芝市', '山南市', '那曲市', '阿里地区', '西安市',\
                     '铜川市', '宝鸡市', '咸阳市', '渭南市', '延安市', '汉中市', '榆林市', '安康市', '商洛市', '兰州市', '嘉峪关市', '金昌市', \
                     '白银市', '天水市', '武威市', '张掖市', '平凉市', '酒泉市', '庆阳市', '定西市', '陇南市', '临夏回族自治州', '甘南藏族自治州',\
                     '西宁市', '海东市', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州', '果洛藏族自治州', '玉树藏族自治州',\
                     '海西蒙古族藏族自治州', '银川市', '石嘴山市', '吴忠市', '固原市', '中卫市', '香港特别行政区', '澳门特别行政区',\
                     '郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河市',\
                     '三门峡市', '南阳市', '商丘市', '信阳市', '周口市', '驻马店市', '武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市',\
                     '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市', '咸宁市', '随州市', '恩施土家族苗族自治州', '海口市', '三亚市',\
                     '三沙市', '儋州市', '乌鲁木齐市', '克拉玛依市', '吐鲁番市', '哈密市', '阿克苏地区', '喀什地区', '和田地区',\
                     '昌吉回族自治州', '博尔塔拉蒙古自治州', '巴音郭楞蒙古自治州', '克孜勒苏柯尔克孜自治州', '伊犁哈萨克自治州',\
                     '塔城地区', '阿勒泰地区']
        #a = get_weather(n)
    from tqdm import tqdm
    bar = tqdm(china_city)
    for location in bar:
        location = location.replace('市','')
        inputwd= browser.find_element_by_name("wd")#搜索输入文本框的name属性值              .text #id="wrapper"的所有文本
        but=browser.find_element_by_xpath('//input[@type="submit"]')#搜索提交按钮
        inputwd.clear()#清楚文本框里的内容
        inputwd.send_keys(u'{}天气'.format(location))#输入关键词
        but.send_keys(Keys.RETURN)#输入回车键  but.click()  #点击按钮
        time.sleep(3)
        weathers = browser.find_elements_by_xpath("//*[@id='1']/div[1]/div[1]/a")
        today_ = today()
        untoday_ = [untoday(n+1) for n in range(4)]
        weather_huancun[str(datetime.datetime.now().date())+location]=[today_, untoday_]
        time.sleep(1)
    save_weather_huancun()
    print('天气预加载成功，已保存易出现城市信息。')
    browser.quit()
    
weather_huancun = load_weather_huancun()

#http, https = get_useable_ip()
# In[37]:

def get_weather(location='北京', return_day=None, return_temp=False, return_how=None, return_change=False):
    global chaxun
    set_chaxun(1)
    try:
        if str(datetime.datetime.now().date())+location in weather_huancun.keys():
            today_=weather_huancun[str(datetime.datetime.now().date())+location][0]
            untoday_=weather_huancun[str(datetime.datetime.now().date())+location][1]
        else:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=option)
            browser.get("https://www.baidu.com")
            #找天气元素
            inputwd= browser.find_element_by_name("wd")#搜索输入文本框的name属性值              .text #id="wrapper"的所有文本
            but=browser.find_element_by_xpath('//input[@type="submit"]')#搜索提交按钮
            inputwd.clear()#清楚文本框里的内容
            inputwd.send_keys(u'{}天气'.format(location))#输入关键词
            but.send_keys(Keys.RETURN)#输入回车键  but.click()  #点击按钮
            time.sleep(3)
            weathers = browser.find_elements_by_xpath("//*[@id='1']/div[1]/div[1]/a")

            def today():
                today = weathers[0].text.strip().split()
                try:
                    today_time = ' '.join(today[0:2])
                    today_ss = today[3]+today[4]+' '+today[5]
                    today_weather = ''.join(today[6:9])+' '+today[9] + ' '+today[10]
                    try:
                        today_weather=today_weather+" 空气质量：{} {}".format(today[11],today[12])
                    except:
                        True
                except:
                    today_time=' '.join(today[0:2])
                    today_ss='暂时无法获取当前温度。'
                    today_weather=''.join(today[3:6])+' '+today[6] + ' '+today[7]
                return today_time, today_ss, today_weather
                
            def untoday(n):
                try:
                    tommorrow = weathers[n].text.strip().split()
                    tommorrow_time = ' '.join(tommorrow[0:2])
                    tommorrow_weather = ''.join(tommorrow[2:5])+' '+tommorrow[5] + ' '+tommorrow[6]
                    try:
                        tommorrow_weather = tommorrow_weather + " 空气质量：{}".format(tommorrow[7])
                    except:
                        True
                    return tommorrow_time, tommorrow_weather
                except:
                    True
                
            #输出——后期需改
            today_ = today()
            untoday_ = [untoday(n+1) for n in range(4)]
            browser.quit()
            weather_huancun[str(datetime.datetime.now().date())+location]=[today_, untoday_]
        if return_day!=None:
            a = (datetime.date(int(return_day.split('-')[0]),int(return_day.split('-')[1]),int(return_day.split('-')[2]))-datetime.datetime.now().date()).days
            if a==0:
                if return_temp:
                    chaxun = "当前温度："+today_[1]+'。'
                else:
                    chaxun = return_day+location+'天气：'+today_[2]+"。当前："+today_[1]
                weather = today_[2]
            elif a<=4 and a>0:
                chaxun = untoday_[a-1][0]+location+'天气'+ '：'+untoday_[a-1][1]
                weather = untoday_[a-1][1]
            good_weather = True
            if 0<=a and a<5:
                if return_how!=None:
                    if "雨" in return_how or "雪" in return_how:
                        if '雨' in weather or '雪' in weather:
                            chaxun = "{}{}会下{}。\n".format(return_day, location, return_how)+chaxun
                        else:
                            chaxun = "{}{}不会下{}。\n".format(return_day, location, return_how)+chaxun
                    elif "雾" in return_how or "霾" in return_how:
                        if '雾' in weather or '霾' in weather:
                            chaxun = "{}{}会有{}。\n".format(return_day, location, return_how)+chaxun
                        else:
                            chaxun = "{}{}不会有{}。\n".format(return_day, location, return_how)+chaxun
                    elif "空气" in return_how:
                        kongqi = weather.split("空气质量：")[-1]
                        if '优' in kongqi or '良' in kongqi:
                            chaxun = "{}{}空气质量较好。\n".format(return_day, location)+chaxun
                        elif '度' in kongqi:
                            chaxun = "{}{}空气{}污染。\n".format(return_day, location, chaxun)+chaxun
                    elif "风" in return_how:
                        feng = weather.split("空气质量：")[0].split()[-1]
                        chaxun = "{}{}刮{}。\n".format(return_day, location, feng)+chaxun
                jianyi = ''
                if int(weather.split('~')[0])<10:
                    jianyi = jianyi + "天气较凉，小乖提醒您出门多加衣物，穿件毛衣保保暖喔～"
                    good_weather = False
                elif int(weather.split('~')[0])>25 and "晴" in weather:
                    jianyi = jianyi + "天气炎热，烈阳当头照，小乖提醒您出门记得涂防晒喔～"
                    good_weather = False
                if '雨' in weather or '雪' in weather:
                    jianyi = jianyi + '您出门记得带雨衣或伞喔～'
                    good_weather = False
                if '霾' in chaxun:
                    jianyi = jianyi + '您出门记得带口罩喔～'
                    good_weather = False
                if good_weather:
                    jianyi = jianyi + '天气适宜，小乖祝您出行愉快！'
                if return_change:
                    chaxun = jianyi + '\n' + chaxun
                else:
                    chaxun = chaxun + '\n' + jianyi
            else:
                chaxun = "超过5天，小乖查不到啦!"
            return chaxun
        chaxun = location+"当前："+today_[0]+' '+today_[1]+'\n今天天气：'+today_[2]+'\n'+'\n'.join([n[0]+'：'+n[1] for n in untoday_])
    except Exception as e:
        print(e.args)
        browser.quit()
        chaxun =  "查询失败，请检查输入！"
    return chaxun
'''print(get_weather('北京',return_day='2019-12-19'))
print(get_weather('北京',return_day='2019-12-17'))'''


# In[39]:


def get_traintickets(from_, to_, day_=None, time_=None, return_timelist=False, 
                     set_startloc=None, set_arriveloc=None, return_num=False,
                     return_startloc=False, return_startloc_ans=False, return_ishaveG=False, return_G=False,
                    return_all=False, return_weather=True, Y=False):
    import requests as requests_train
    '''
    day:y-m-d格式
    time:24小时制，表示几点的车票，比如“…下午5点的车票”，就查询17点内的车票
    输出：字典，key为班次，value仍然是字典，有start_time,start_loc等
    '''
    global chaxun
    set_chaxun(1)
    day = day_.replace('-', '')
    try:
        url = "https://huoche.8684.cn/p_{}_{}?date={}".format(from_, to_, day)
        headers = {
                'Connection': 'close',
                }
        
        response = requests_train.get(url,headers=headers)
        soup = bs(response.text)
        search_list = soup.find('ol',class_='table-body').find_all('li',recursive=False)
        
        information = {}
        url_order = []
        
        for i in range(len(search_list)):
            text = search_list[i].text.split()
            #print(text)
            url_order.append("http://huochepiao.114piaowu.com/tobuy?trainCode={}&fromStation={}&toStation={}&goDate={}".format(text[0],text[1],text[2],day_[0:4]+'-'+day_[5:7]+'-'+day_[8:10]))
            information[text[0]] = {'start_time':text[3][0:5],'start_loc':text[1],'total_time':text[4],
                                    'arrive_time':text[3][5:10], 'arrive_loc':text[2],
                                   'tickets':text[5]+':'+text[6], 'url':url_order[-1]
                                   }
        
            total_minute = 0
            
            for n in information[text[0]]['total_time'].split('小时'):
                if '分' in n:
                    total_minute+=int(n.strip('分'))
                else:
                    if n!='':
                        total_minute += int(n)*60
            
            information[text[0]]['score'] = abs(int(12)-int(information[text[0]]['start_time'][0:2]))*100\
                                        +abs(total_minute)+abs(float((information[text[0]]['tickets'].split('￥')[-1])))
        
        if set_startloc!=None:
            for key in list(information.keys()):
                if set_startloc not in information[key]['start_loc'] and information[key]['start_loc'] not in set_startloc:
                    del information[key]
        if set_arriveloc != None:
            for key in list(information.keys()):
                if set_arriveloc not in information[key]['arrive_loc'] and information[key]['arrive_loc'] not in set_arriveloc:
                    del information[key]
        if time_!=None:
                if len(time_)>1:
                    for key in list(information.keys()):
                        if information[key]['start_time'].split(':')[0]+':00' not in time_:
                            del information[key]
                else:
                    min_banci = None
                    mins = 9999
                    for key in list(information.keys()):
                        if time_[0] == information[key]['start_time']:
                            min_banci = key
                            chaxun = "小乖查到啦！根据您的需求，小乖给您推荐您前往{}搭乘{}班次，该班次将在{}启程，{}到达{}，全程{}，{}，推荐您于{} {}前到达{}进站候车。".format(information[min_banci]['start_loc'],min_banci,\
                                   information[min_banci]['start_time'], information[min_banci]['arrive_time'],\
                                   information[min_banci]['arrive_loc'], information[min_banci]['total_time'],\
                                   information[min_banci]['tickets'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                    +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                            return chaxun
                        else:
                            hour = abs(int(information[key]['start_time'][:2])-int(time_[0][:2]))
                            minute = abs(int(information[key]['start_time'][3:])-int(time_[0][3:]))
                            ttmins = hour*60+minute
                            if mins>ttmins:
                                min_banci = key
                                mins = ttmins
                    #print(mins)
                    chaxun = "很抱歉，根据您的需求，没有{}出发的班次，小乖给您推荐您前往{}搭乘{}班次，该班次将在{}启程，{}到达{}，全程{}，{}，推荐您于{} {}前到达{}进站候车。".format(time_[0],information[min_banci]['start_loc'],min_banci,\
                                   information[min_banci]['start_time'], information[min_banci]['arrive_time'],\
                                   information[min_banci]['arrive_loc'], information[min_banci]['total_time'],\
                                   information[min_banci]['tickets'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                    +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                    return chaxun
        
        if return_num:
            chaxun='{}有{}到{}的火车有{}个班次。'.format(day_, from_, to_, len(information.keys()))\
                    #+"\n--------------------\n详情请点击："+url
            #browser.quit()
            return chaxun
        if return_timelist:
            chaxun='{}有{}到{}的火车有{}个班次。'.format(day_, from_, to_, len(information.keys())) 
            chaxun=chaxun + "\n--------------------\n".join([banci+' '+information[banci]['start_loc']+\
                                                    ' '+information[banci]['start_time'] for banci in information.keys()])
            #chaxun = chaxun +"\n--------------------\n详情请点击："+url
            #browser.quit()
            return chaxun
        
        if return_ishaveG:
            for key in list(information.keys()):
                if 'G' in key:
                    chaxun = '{}有从{}到{}的高铁，如{}班次。'.format(day_, from_, to_, key)+"详情请点击："+url
                    return chaxun
            chaxun = '很遗憾，{}没有从{}到{}的高铁，详情请点击：'.format(day_, from_, to_)+url
            #browser.quit()
            return chaxun
        if return_G:
            for key in list(information.keys()):
                if 'G'not in key:
                    del information[key]
            chaxun = '{}有{}到{}的高铁一共有{}个班次。\n'.format(day_, from_, to_, len(information.keys()))
            for banci in information.keys():
                if len(chaxun)<1000-len("详情请点击："+url):
                    chaxun = chaxun + "班次："+banci+' '+information[banci]['start_loc']+' '+information[banci]['start_time']\
                          +' '+'全程：'+information[banci]['total_time'] +' '+information[banci]['arrive_loc']+' '\
                          +information[banci]['arrive_time']+' '+' '.join(information[banci]['tickets'])+'\n'+'-'*20+'\n'
            if chaxun=='':
                chaxun = '抱歉暂无所查询火车票信息。'
            #chaxun = chaxun +"详情请点击："+url
            #browser.quit()
            return chaxun
        if return_startloc:
            chaxun='{}您可以去'.format(day_)+'、'.join(list(set([information[banci]['start_loc']\
                    for banci in information.keys()])))+'坐车出发去{}。'.format(to_)\
                    #+"--------------------\n详情请点击："+url
            #browser.quit()
            return chaxun
        sorted_information = sorted(information.items(), key=lambda x:x[1]['score'])
        #print(sorted_information)
        chaxun = '小乖帮你查到啦！'
        if Y:
            chaxun = chaxun + '{}{}到{}有票！\n'.format(day_, from_, to_)
        if return_all:
            for banci in information.keys():
                if len(chaxun)<1000-len("详情请点击："+url):
                    chaxun = chaxun + "班次："+banci+' '+information[banci]['start_loc']+' '+information[banci]['start_time']\
                          +' '+'全程：'+information[banci]['total_time'] +' '+information[banci]['arrive_loc']+' '\
                          +information[banci]['arrive_time']+' '+' '.join(information[banci]['tickets'])+'\n'+'-'*20+'\n'
        else:
            i=0
            notickets=True
            while notickets:
                min_banci = sorted_information[i][0]
                #print(information[min_banci]['url'].replace('huochepiao','m'))
                response = requests_train.get(information[min_banci]['url'].replace('huochepiao','m').replace('tobuy','huochepiao/tobuy'))
                #print(soup)
                soup = bs(response.text)
                b = soup.find(class_='yupiao')
                if b==None or b.text == '售完':
                    i = i + 1
                    if i>=len(sorted_information):
                        chaxun = '很遗憾，{}从{}到{}的火车票已售空，请更换日期查询，或关注抢票平台。详情请点击：'.format(day_, from_, to_)+url
                        return chaxun
                else:
                    notickets=False
    
            if return_startloc_ans:
                chaxun = chaxun + "根据综合评分，小乖给您推荐您前往{}搭乘{}班次，该班次将在{}启程，{}到达{}，全程{}，{}，推荐您于{} {}前到达{}进站候车。".format(information[min_banci]['start_loc'],min_banci,\
                                   information[min_banci]['start_time'], information[min_banci]['arrive_time'],\
                                   information[min_banci]['arrive_loc'], information[min_banci]['total_time'],\
                                   information[min_banci]['tickets'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                    +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
            else:
                chaxun = chaxun + "根据综合评分，小乖给您推荐{}班次，该班次将在{}于{}启程，{}到达{}，全程{}，{}，推荐您于{} {}前到达{}进站候车。".format(min_banci, information[min_banci]['start_time'],\
                                   information[min_banci]['start_loc'], information[min_banci]['arrive_time'],\
                                   information[min_banci]['arrive_loc'], information[min_banci]['total_time'],\
                                   information[min_banci]['tickets'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                    +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
            
            chaxun = chaxun + '该车次剩余{}票，请点击 {} 购买。'.format(b.text, information[min_banci]['url'])
    
            if return_weather:
                a = (datetime.date(int(day_.split('-')[0]),int(day_.split('-')[1]),int(day_.split('-')[2]))-datetime.datetime.now().date()).days
                if a < 5:
                    chaxun = chaxun +'\n'+'-'*20+'\n'+"目的地城市天气情况：\n"+get_weather(to_,day_)
            
        if chaxun=='小乖帮你查到啦！':
            chaxun = '抱歉暂无所查询火车票信息。'
        #chaxun = chaxun +'\n'#+'-'*20+'\n'+"车票详情请点击："+url
        #browser.quit()
    
    except Exception as e:
        #browser.quit()
        print(e.args)
        chaxun =  "很遗憾，{}没有从{}到{}的火车票，请检查输入，或尝试其他日期！详情请点击：".format(day_, from_, to_)+url
   
    return chaxun
#print(get_traintickets("北京","郑州","2019-12-20"))


# In[40]:


def get_bustickets(from_, to_, day_=None, time_=None, return_timelist=False, return_all=False,
                     set_startloc=None, set_arriveloc=None, return_num=False, return_startloc=False,return_startloc_ans=False,
                  return_weather=True, Y=False):
    '''
    day:y-m-d格式
    time:24小时制，表示几点的车票，比如“…下午5点的车票”，就查询17点内的车票
    输出：字典，key为班次，value仍然是字典，有start_time,start_loc等
    '''
    
    global chaxun
    set_chaxun(1)
    url = "http://qiche.114piaowu.com/"
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    try:
        browser.find_element_by_xpath("//*[@id='startCity2']").send_keys(from_)
        browser.find_element_by_xpath("//*[@id='endCity2']").send_keys(to_)
        date = browser.find_element_by_xpath("//*[@id='goDate2']")
        date.clear()
        date.send_keys(day_)
        time.sleep(1)
        date.send_keys(Keys.ENTER)
        browser.switch_to.window(browser.window_handles[-1])
        current_url = browser.current_url
        search_list = browser.find_elements_by_name("qicheData")
        if len(search_list)==0:
            chaxun =  "没票啦！！换一个目的地或者换一天出发吧～"+ current_url
            browser.quit()
            return chaxun
        information = {}
        min_score = 999999
        min_banci = None
        for i in range(len(search_list)):
            text = search_list[i].text.split()
            information[text[0]] = {'start_time':text[0],'start_loc':text[1],
                                    'arrive_loc':text[2],
                                   'price':text[4],'type':text[3]
                                   }
            information[text[0]]['score'] = abs(int(12)-int(information[text[0]]['start_time'][0:2]))*100                                        +abs(float((information[text[0]]['price'].split('￥')[-1])))
            if information[text[0]]['score']<min_score:
                min_score = information[text[0]]['score']
                min_banci = text[0]
                
        if set_startloc!=None:
            for key in list(information.keys()):
                if set_startloc not in information[key]['start_loc']  and information[key]['start_loc'] not in set_startloc:
                    del information[key]
        if set_arriveloc != None:
            for key in list(information.keys()):
                if set_arriveloc not in information[key]['arrive_loc']  and information[key]['arrive_loc'] not in set_arriveloc:
                    del information[key]
                    
        if time_!=None:
            if len(time_)>1:
                for key in list(information.keys()):
                    if information[key]['start_time'].split(':')[0]+':00' not in time_:
                        del information[key]
            else:
                min_banci = None
                mins = 9999
                for key in list(information.keys()):
                    if time_[0] == information[key]['start_time']:
                        min_banci = key
                        chaxun = "小乖查到啦！根据您的需求，小乖给您推荐您前往{}搭乘{}的班次，终点站{}，价格为{}￥，推荐您于{} {}前到达{}进站候车。".format(information[min_banci]['start_loc'],min_banci,\
                                                   information[min_banci]['arrive_loc'],\
                                       information[min_banci]['price'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                        +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                        return chaxun
                    else:
                        hour = abs(int(information[key]['start_time'][:2])-int(time_[0][:2]))
                        minute = abs(int(information[key]['start_time'][3:])-int(time_[0][3:]))
                        ttmins = hour*60+minute
                        if mins>ttmins:
                            min_banci = key
                            mins = ttmins
                #print(mins)
                chaxun = "很抱歉，根据您的需求，没有{}出发的班次，小乖给您推荐您前往{}搭乘{}的班次，终点站{}，价格为{}￥，推荐您于{} {}前到达{}进站候车。".format(information[min_banci]['start_loc'],min_banci,\
                                                   information[min_banci]['arrive_loc'],\
                                       information[min_banci]['price'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                        +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                return chaxun
        
        if return_timelist:
            chaxun=''
            chaxun="\n--------------------\n".join([banci+' '+information[banci]['start_loc']+                            ' '+information[banci]['start_time'] for banci in information.keys()])
            #chaxun = chaxun #+"\n--------------------\n详情请点击："+current_url
            return chaxun
        if return_num:
            chaxun='{}有{}到{}的汽车有{}个班次。'.format(day_, from_, to_, len(information.keys()))                   # +"\n--------------------\n详情请点击："+current_url
            return chaxun
        if return_startloc:
            chaxun='{}您可以去'.format(day_)+'、'.join(list(set([information[banci]['start_loc']                    for banci in information.keys()])))+'坐车出发去{}。'.format(to_)                    +'\n'#+"\n--------------------\n详情请点击："+current_url
            return chaxun
        
        browser.quit()
        sorted_information = sorted(information.items(), key=lambda x:x[1]['score'])
        min_banci = sorted_information[0][0]
        chaxun = '小乖帮你查到啦！' 
        if Y:
            chaxun = chaxun + '{}{}到{}有票！\n'.format(day_, from_, to_)
        if return_all:
            for banci in information.keys():
                if len(chaxun)<1000-len("详情请点击："+current_url):
                    chaxun = chaxun + "发车时间："+banci+' 始：'+information[banci]['start_loc']+' 终：'\
                              +information[banci]['arrive_loc']+' 价格：'\
                              +information[banci]['price']\
                              +' 车型：'+information[banci]['type']+'\n'+'-'*20+'\n'
        else:
            if return_startloc_ans:
                chaxun = chaxun + "根据综合评分，小乖给您推荐您前往{}搭乘{}的班次，终点站{}，价格为{}￥，推荐您于{} {}前到达{}进站候车。".format(information[min_banci]['start_loc'],min_banci,\
                                                   information[min_banci]['arrive_loc'],\
                                       information[min_banci]['price'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                        +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
            else:
                chaxun = chaxun + "根据综合评分，小乖给您推荐{}的班次，该班次将在{}于{}启程，终点站{}，价格为{}￥，推荐您于{} {}前到达{}进站候车。".format(min_banci, information[min_banci]['start_time'],\
                                       information[min_banci]['start_loc'], information[min_banci]['arrive_loc'],\
                                       information[min_banci]['price'],day_,str(int(information[min_banci]['start_time'][:2])-1)\
                                        +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
            if return_weather:
                a = (datetime.date(int(day_.split('-')[0]),int(day_.split('-')[1]),int(day_.split('-')[2]))-datetime.datetime.now().date()).days
                if a < 5:
                    chaxun = chaxun +'\n'+'-'*20+'\n'+"目的地城市天气情况：\n"+get_weather(to_,day_)
        if chaxun=='小乖帮你查到啦！':
            chaxun = '抱歉暂无所查询汽车票信息。'
        #chaxun = chaxun +'\n'#+'-'*20+'\n'+"车票详情请点击："+current_url
    except Exception as e:
        print(e.args)
        browser.quit()
        try:
            chaxun = "很遗憾，{}没有从{}到{}的汽车票，请检查输入，请尝试其他日期！可点击此网站查询：".format(day_, from_, to_)+current_url
        except:
            chaxun = "很遗憾，{}没有从{}到{}的汽车票，请检查输入，请尝试其他日期！可点击此网站查询：".format(day_, from_, to_)+url
    return chaxun 
'''print(get_bustickets("宁波","上海","2019-12-16", return_timelist=0, 
                     set_startloc=None, set_arriveloc=None, return_num=False, return_startloc=0,return_all=0))'''


# In[33]:


def get_flighttickets_aboard(from_, to_, day_=None, time_=None, return_all=False, return_weather=True):
    '''
    day:y-m-d格式
    time:24小时制，表示几点的车票，比如“…下午5点的车票”，就查询17点内的车票
    输出：字典，key为班次，value仍然是字典，有start_time,start_loc等
    '''
    global chaxun
    set_chaxun(1)
    url = "https://flights.ctrip.com/international/search/oneway-bjs-hkg"
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    try:
        browser.find_element_by_name("owDCity").send_keys(Keys.CONTROL+'a')
        #time.sleep(1)
        browser.find_element_by_name("owDCity").send_keys(from_)
        time.sleep(1)
        browser.find_element_by_name("owACity").click()
        #time.sleep(1)
        browser.find_element_by_name("owACity").send_keys(to_)
        #browser.find_element_by_name("owDCity").click()
        browser.find_element_by_name("owACity").send_keys(Keys.ENTER)
        time.sleep(1)
        browser.get(browser.current_url.replace(browser.current_url[browser.current_url.find('depdate')+8:browser.current_url.find('depdate')+18],day_))
        time.sleep(4)
        search_list = browser.find_elements_by_class_name('flight-item')
        detail_list = browser.find_elements_by_xpath("//*[@class='flight-detail']")
        information = {}
        min_score = 999999
        min_banci = None
        for n in range(len(search_list[:-2])):
            try:
                text = []
                a=search_list[n].text.split()
                b=detail_list[n].text.split()
                #print(a,b)
                price = browser.find_element_by_id("seatType_{}_0".format(0)).text\
                        +browser.find_element_by_id("price_{}_0".format(0)).text
                if len(b)==5:
                    arrtime = b[2]+b[3]
                else:
                    arrtime = b[2]
                for i in range(len(a)):
                    if '精选' not in a[i]:
                        text.append(a[i])
                information[text[0]+text[1]] = {'start_time':b[0],'start_loc':b[1],
                                                'arrive_time':arrtime, 'arrive_loc':b[-1],
                                               'price':price,'sale':'无折扣'
                                               }
                #print(information)
                bc=text[0]+text[1]
                total_minute = 0
                hour = int(information[bc]['arrive_time'][:2])\
                    -int(information[bc]['start_time'][:2])
                minute = int(information[bc]['arrive_time'][3:])\
                    -int(information[bc]['start_time'][3:])
                while hour<0:
                    hour += 24
                while minute<0:
                    hour -= 1
                    minute += 60
                total_minute = hour*60+minute
                information[bc]['score'] = abs(int(12)-int(information[bc]['start_time'][0:2]))*100\
                                        +abs(float((information[bc]['price'].split('¥')[-1])))+total_minute
                if information[bc]['score']<min_score:
                    min_score = information[bc]['score']
                    min_banci = bc
            except Exception as e:
                #print(e.with_traceback,e.args)
                continue
        url = browser.current_url
        browser.quit()

        if time_!=None:
            for key in list(information.keys()):
                if information[key]['start_time'].split(':')[0] not in time_:
                    del information[key]
        #print(information, min_banci)
        chaxun = ''
        if return_all:
            for banci in information.keys():
                if len(chaxun)<1000-len("详情请点击："+url):
                    chaxun = chaxun + "班次："+banci+' '+information[banci]['start_loc']+' '+information[banci]['start_time']\
                              +' '+information[banci]['arrive_loc']+' '\
                              +information[banci]['arrive_time']+' '+information[banci]['price']\
                              +' 享受'+information[banci]['sale']+'\n'+'-'*20+'\n'
        else:
            chaxun = "根据综合评分，小乖给您推荐{}班次，该班次将在{}于{}启程，{}到达{}，全程{}小时{}分钟，{}，可享受{}，推荐您于{} {}前到达{}机场办理登机手续。".format(min_banci, information[min_banci]['start_time'],\
                                   information[min_banci]['start_loc'], information[min_banci]['arrive_time'],\
                                   information[min_banci]['arrive_loc'], hour, minute,information[min_banci]['price'],\
                                   information[min_banci]['sale'],day_,str(int(information[min_banci]['start_time'][:2])-2)\
                                    +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
            if return_weather:
                a = (datetime.date(int(day_.split('-')[0]),int(day_.split('-')[1]),int(day_.split('-')[2]))-datetime.datetime.now().date()).days
                if a < 5:
                    chaxun = chaxun +'\n'+'-'*20+'\n'+"目的地城市天气情况：\n"+get_weather(to_,day_)
        #chaxun = chaxun +'\n'#+'-'*20+'\n'+"机票详情请点击："+url
    except Exception as e:
        print(e.with_traceback,e.args)
        browser.quit()
        chaxun = "很遗憾，{}没有从{}到{}的飞机票，请检查输入，或已无票，请尝试其他日期！可点击此网站查询：".format(day_, from_, to_)+url
    return chaxun


# In[34]:


def get_flighttickets(from_, to_, day_=None, time_=None, return_timelist=False, 
                     set_startloc=None, set_arriveloc=None, return_num=False, 
                      set_flight= None, return_startloc=False,return_startloc_ans=False, return_all=False,
                     return_weather=True, Y=False):
    '''
    day:y-m-d格式
    time:24小时制，表示几点的车票，比如“…下午5点的车票”，就查询17点内的车票
    输出：字典，key为班次，value仍然是字典，有start_time,start_loc等
    '''
    import requests as requests_flight
    global chaxun
    set_chaxun(1)
    china_city = '北京市天津市石家庄市唐山市秦皇岛市邯郸市邢台市保定市张家口市承德市沧州市廊坊市衡水市太原市大同市阳泉市长治市晋城市朔州市晋中市运城市忻州市临汾市吕梁市呼和浩特市包头市乌海市赤峰市通辽市鄂尔多斯市呼伦贝尔市巴彦淖尔市乌兰察布市兴安盟锡林郭勒盟阿拉善盟沈阳市大连市鞍山市抚顺市本溪市丹东市锦州市营口市阜新市辽阳市盘锦市铁岭市朝阳市葫芦岛市长春市吉林市四平市辽源市通化市白山市松原市白城市延边朝鲜族自治州哈尔滨市齐齐哈尔市鸡西市鹤岗市双鸭山市大庆市伊春市佳木斯市七台河市牡丹江市黑河市绥化市大兴安岭地区上海市南京市无锡市徐州市常州市苏州市南通市连云港市淮安市盐城市扬州市镇江市泰州市宿迁市杭州市宁波市温州市嘉兴市湖州市绍兴市金华市衢州市舟山市台州市丽水市合肥市芜湖市蚌埠市淮南市马鞍山市淮北市铜陵市安庆市黄山市滁州市阜阳市宿州市六安市亳州市池州市宣城市福州市厦门市莆田市三明市泉州市漳州市南平市龙岩市宁德市南昌市景德镇市萍乡市九江市新余市鹰潭市赣州市吉安市宜春市抚州市上饶市济南市青岛市淄博市枣庄市东营市烟台市潍坊市济宁市泰安市威海市日照市莱芜市临沂市德州市聊城市滨州市菏泽市长沙市株洲市湘潭市衡阳市邵阳市岳阳市常德市张家界市益阳市郴州市永州市怀化市娄底市湘西土家族苗族自治州广州市韶关市深圳市珠海市汕头市佛山市江门市湛江市茂名市肇庆市惠州市梅州市汕尾市河源市阳江市清远市东莞市中山市潮州市揭阳市云浮市南宁市柳州市桂林市梧州市北海市防城港市钦州市贵港市玉林市百色市贺州市河池市来宾市崇左市重庆市成都市自贡市攀枝花市泸州市德阳市绵阳市广元市遂宁市内江市乐山市南充市眉山市宜宾市广安市达州市雅安市巴中市资阳市阿坝藏族羌族自治州甘孜藏族自治州凉山彝族自治州贵阳市六盘水市遵义市安顺市毕节市铜仁市黔西南布依族苗族自治州黔东南苗族侗族自治州黔南布依族苗族自治州昆明市曲靖市玉溪市保山市昭通市丽江市普洱市临沧市楚雄彝族自治州红河哈尼族彝族自治州文山壮族苗族自治州西双版纳傣族自治州大理白族自治州德宏傣族景颇族自治州怒江傈僳族自治州迪庆藏族自治州拉萨市日喀则市昌都市林芝市山南市那曲市阿里地区西安市铜川市宝鸡市咸阳市渭南市延安市汉中市榆林市安康市商洛市兰州市嘉峪关市金昌市白银市天水市武威市张掖市平凉市酒泉市庆阳市定西市陇南市临夏回族自治州甘南藏族自治州西宁市海东市海北藏族自治州黄南藏族自治州海南藏族自治州果洛藏族自治州玉树藏族自治州海西蒙古族藏族自治州银川市石嘴山市吴忠市固原市中卫市香港特别行政区澳门特别行政区郑州市开封市洛阳市平顶山市安阳市鹤壁市新乡市焦作市濮阳市许昌市漯河市三门峡市南阳市商丘市信阳市周口市驻马店市武汉市黄石市十堰市宜昌市襄阳市鄂州市荆门市孝感市荆州市黄冈市咸宁市随州市恩施土家族苗族自治州海口市三亚市三沙市儋州市乌鲁木齐市克拉玛依市吐鲁番市哈密市阿克苏地区喀什地区和田地区昌吉回族自治州博尔塔拉蒙古自治州巴音郭楞蒙古自治州克孜勒苏柯尔克孜自治州伊犁哈萨克自治州塔城地区阿勒泰地区'
    if(to_ not in china_city or from_ not in china_city):
        return get_flighttickets_aboard(from_, to_, day_,return_all=return_all,return_weather=return_weather)
    url = "https://jipiao.8684.cn/p_{}_{}?date={}".format(from_, to_, ''.join(day_.split('-')))
    response = requests_flight.get(url)
    soup = bs(response.text)

    try:
        current_url = soup.find('iframe', id = 'ser_iframe')['src']
        response = requests_flight.get(current_url)
        soup = bs(response.text)
        search_list = soup.find('div', class_='jp_list').find_all('div')
        
        if search_list[0].text.strip() == '未查询到相关数据！':
            chaxun = '没票啦！！换一天出发吧～'
            return chaxun+url
        information = {}
        for i in range(len(search_list)):
            text = search_list[i].text.split()
            #print(text)
            try:
                if len(text)>14:
                    information[text[5]] = {'start_time':text[0],'start_loc':text[3],
                                            'arrive_time':text[1]+text[2], 'arrive_loc':text[4],
                                           'price':text[12][:4]+':'+text[13],'sale':str(round(float(text[14][:-1]),1))+text[14][-1]
                                           }
                    total_minute = 0
                    hour = int(information[text[5]]['arrive_time'][:2])-int(information[text[5]]['start_time'][:2])
                    minute = int(information[text[5]]['arrive_time'][3:])-int(information[text[5]]['start_time'][3:])
                    while hour<0:
                        hour += 24
                    while minute<0:
                        hour -= 1
                        minute += 60
                    total_minute = hour*60+minute
                    information[text[5]]['score'] = abs(int(12)-int(information[text[5]]['start_time'][0:2]))*100                                        +abs(float((information[text[5]]['price'].split('￥')[-1])))+total_minute
            except:
                continue
            
        if set_startloc!=None:
            for key in list(information.keys()):
                if set_startloc not in information[key]['start_loc'] and information[key]['start_loc'] not in set_startloc:
                    del information[key]
        if set_arriveloc != None:
            for key in list(information.keys()):
                if set_arriveloc not in information[key]['arrive_loc'] and information[key]['arrive_loc'] not in set_arriveloc:
                    del information[key]
                
        if time_!=None:
            if len(time_)>1:
                for key in list(information.keys()):
                    if information[key]['start_time'].split(':')[0]+':00' not in time_:
                        del information[key]
            else:
                min_banci = None
                mins = 9999
                for key in list(information.keys()):
                    if time_[0] == information[key]['start_time']:
                        min_banci = key
                        chaxun = "小乖查到啦！根据您的需求，小乖给您推荐{}班次，该班a次将在{}于{}启程，{}到达{}，全程{}小时{}分钟，{}，可享受{}，推荐您于{} {}前到达{}机场办理登机手续。".format(min_banci, information[min_banci]['start_time'],\
                                                information[min_banci]['start_loc'], information[min_banci]['arrive_time'],\
                                                information[min_banci]['arrive_loc'], hour, minute,information[min_banci]['price'],\
                                                information[min_banci]['sale'],day_,str(int(information[min_banci]['start_time'][:2])-2)\
                                                +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                        return chaxun
                    else:
                        hour = abs(int(information[key]['start_time'][:2])-int(time_[0][:2]))
                        minute = abs(int(information[key]['start_time'][3:])-int(time_[0][3:]))
                        ttmins = hour*60+minute
                        if mins>ttmins:
                            min_banci = key
                            mins = ttmins
                #print(mins)
                chaxun = "很抱歉，根据您的需求，没有{}起飞的班次，小乖给您推荐世间最近的{}班次，该班次将在{}于{}启程，{}到达{}，全程{}小时{}分钟，{}，可享受{}，推荐您于{} {}前到达{}机场办理登机手续。".format(time_[0],\
                                                  min_banci, information[min_banci]['start_time'],\
                                                information[min_banci]['start_loc'], information[min_banci]['arrive_time'],\
                                                information[min_banci]['arrive_loc'], hour, minute,information[min_banci]['price'],\
                                                information[min_banci]['sale'],day_,str(int(information[min_banci]['start_time'][:2])-2)\
                                                +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                return chaxun

        if return_timelist:
            chaxun=''
            chaxun="\n--------------------\n".join([banci+' '+information[banci]['start_loc']+                            ' '+information[banci]['start_time'] for banci in information.keys()])
            #chaxun = chaxun #+"\n--------------------\n详情请点击："+current_url
            return chaxun
        if return_num:
            chaxun='{}有{}到{}的飞机有{}个班次。'.format(day_, from_, to_, len(information.keys()))                    +'\n'#+"\n--------------------\n详情请点击："+current_url
            return chaxun
        if set_flight!=None:
            for key in list(information.keys()):
                if set_flight not in key:
                    del information[key]
        if return_startloc:
            chaxun='{}您可以去'.format(day_)+'、'.join(list(set([information[banci]['start_loc']                    for banci in information.keys()])))+'坐飞机出发去{}。'.format(to_)                    #+"\n--------------------\n详情请点击："+current_url
            return chaxun
        sorted_information = sorted(information.items(), key=lambda x:x[1]['score'])
        chaxun = '小乖帮你查到啦！'
        if Y:
            chaxun = chaxun + '{}{}到{}有票！\n'.format(day_, from_, to_)
        if return_all:
            for banci in information.keys():
                if len(chaxun)<1000-len("详情请点击："+url):
                    chaxun = chaxun + "班次："+banci+' '+information[banci]['start_loc']+' '+information[banci]['start_time']                              +' '+information[banci]['arrive_loc']+' '                              +information[banci]['arrive_time']+' '+information[banci]['price']                              +' 享受'+information[banci]['sale']+'\n'+'-'*20+'\n'
        else:
            min_banci = sorted_information[0][0]
            if return_startloc_ans:
                chaxun = chaxun + "根据综合评分，小乖给您推荐您前往{}搭乘{}班次，该班次将在{}启程，{}到达{}，全程{}小时{}分钟，{}，可享受{}，推荐您于{} {}前到达{}机场办理登机手续。".format(information[min_banci]['start_loc'],min_banci,\
                                   information[min_banci]['start_time'],information[min_banci]['arrive_time'],\
                                   information[min_banci]['arrive_loc'], hour, minute,information[min_banci]['price'],\
                                   information[min_banci]['sale'],day_,str(int(information[min_banci]['start_time'][:2])-2)\
                                    +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
            else:
                chaxun = chaxun + "根据综合评分，小乖给您推荐{}班次，该班a次将在{}于{}启程，{}到达{}，全程{}小时{}分钟，{}，可享受{}，推荐您于{} {}前到达{}机场办理登机手续。".format(min_banci, information[min_banci]['start_time'],\
                                                information[min_banci]['start_loc'], information[min_banci]['arrive_time'],\
                                                information[min_banci]['arrive_loc'], hour, minute,information[min_banci]['price'],\
                                                information[min_banci]['sale'],day_,str(int(information[min_banci]['start_time'][:2])-2)\
                                                +information[min_banci]['start_time'][2:], information[min_banci]['start_loc'])
                                                
            if return_weather:
                a = (datetime.date(int(day_.split('-')[0]),int(day_.split('-')[1]),int(day_.split('-')[2]))-datetime.datetime.now().date()).days
                if a < 5:
                    chaxun = chaxun +'\n'+'-'*20+'\n'+"目的地城市天气情况：\n"+get_weather(to_,day_)
        #chaxun = chaxun +'\n'#+'-'*20+'\n'+"机票详情请点击："+url
    except Exception as e:
        print(e.with_traceback,e.args)
        chaxun = "很遗憾，{}没有从{}到{}的飞机票，请检查输入，或已无票，请尝试其他日期！可点击此网站查询：".format(day_, from_, to_)+url
    return chaxun

#print(get_flighttickets("北京","宁波","2019-12-12",return_timelist=0, 
#                     set_startloc=None,set_flight='东方航空', set_arriveloc=None, return_num=0, return_startloc=0))
#print(get_flighttickets("北京","澳门","2019-12-17"))


# In[41]:


def get_answers(question):
    '''
    返回字典，key：标题，value：网址
    '''
    global chaxun
    set_chaxun(1)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=option)
    browser.get("http://www.baidu.com")
    #查找问题
    inputwd= browser.find_element_by_name("wd")#搜索输入文本框的name属性值
    but=browser.find_element_by_xpath('//input[@type="submit"]')#搜索提交按钮
    inputwd.clear()#清楚文本框里的内容
    inputwd.send_keys(question)#输入关键词
    but.send_keys(Keys.RETURN)#输入回车键  but.click()  #点击按钮
    time.sleep(1)
    #定位爬取搜索链接
    search_list = browser.find_elements_by_xpath("//*[@id='content_left']//h3")
    search = {}
    for i in range(len(search_list)):
        search[search_list[i].text]= search_list[i].find_element_by_xpath("a").get_attribute('href')
    browser.quit()
    chaxun = '\n'.join([n+'： '+search[n] for n in search.keys()])
    return chaxun
#print(get_answers("对外经济贸易大学李兵"))


# In[43]:


from threading import Thread
def get_weather_thread(location='北京', return_day=None, return_temp=False, return_how=None, return_change=False):
    global chaxun
    loc = location[:]
    t1=Thread(target=get_weather,args=(loc,return_day,return_temp, return_how, return_change))
    t1.start()
    return "正在查询天气信息，请稍后……"
def get_traintickets_thread(from_='北京', to_='上海', day_=datetime.datetime.now().strftime('%Y-%m-%d'), 
                      time_=None, return_timelist=False, 
                     set_startloc=None, set_arriveloc=None, return_num=False,
                     return_startloc=False, return_startloc_ans=False, return_ishaveG=False, return_G=False,
                    return_all=False, return_weather=True, Y=False):
    global chaxun
    t1=Thread(target=get_traintickets,args=(from_.strip('市').strip('省').strip('县'),
                     to_.strip('市').strip('省').strip('县'), day_, time_, return_timelist, 
                     set_startloc, set_arriveloc, return_num,
                     return_startloc, return_startloc_ans, return_ishaveG, return_G,
                    return_all, return_weather, Y))
    t1.start()
    return "正在查询火车票信息，请稍后……"
def get_bustickets_thread(from_='北京', to_='上海', day_=datetime.datetime.now().strftime('%Y-%m-%d'), time_=None,
                     return_timelist=False, return_all=False,
                     set_startloc=None, set_arriveloc=None, return_num=False, 
                     return_startloc=False,return_startloc_ans=False,
                     return_weather=True, Y=False):
    global chaxun
    t1=Thread(target=get_bustickets,args=(from_.strip('市').strip('省').strip('县'),
                     to_.strip('市').strip('省').strip('县'), day_, time_, return_timelist, return_all,
                     set_startloc, set_arriveloc, return_num, return_startloc,
                     return_startloc_ans, return_weather, Y))
    t1.start()
    return "正在查询汽车票信息，请稍后……"
def get_flighttickets_thread(from_='北京', to_='上海', day_=datetime.datetime.now().strftime('%Y-%m-%d'), time_=None, return_timelist=False, 
                     set_startloc=None, set_arriveloc=None, return_num=False, 
                      set_flight= None, return_startloc=False,return_startloc_ans=False, return_all=False,
                     return_weather=True, Y=False):
    global chaxun
    t1=Thread(target=get_flighttickets,args=(from_.strip('市').strip('省').strip('县'),
                     to_.strip('市').strip('省').strip('县'), day_, time_, return_timelist, 
                     set_startloc, set_arriveloc, return_num, 
                      set_flight, return_startloc, return_startloc_ans, return_all, return_weather,Y))
    t1.start()
    return "正在查询机票信息，请稍后……"
def get_answers_thread(question):
    global chaxun
    t1=Thread(target=get_answers,args=([question]))
    t1.start()
    return "正在查询相关信息，请稍后……"


# In[25]:
    

place_re = np.load('all_place.npy',allow_pickle=True).item()#字典保存位置
food_re = np.load('all_food.npy',allow_pickle=True).item()#字典保存位置

def place_rec(location='北京市'):#景点推荐
    try:
        if location in set(place_re.keys()):
            answer=place_re[location]
        elif location+'省' in set(place_re.keys()):
            answer=place_re[location+'省']
        elif location+'市' in set(place_re.keys()):
            answer=place_re[location+'市']  
        elif location+'自治州' in set(place_re.keys()):
            answer=place_re[location+'自治州']
        elif location+'特别行政区' in set(place_re.keys()):
            answer=place_re[location+'特别行政区']
        elif location+'自治区' in set(place_re.keys()):
            answer=place_re[location+'自治区']
        elif location+'地区' in set(place_re.keys()):
            answer=place_re[location+'地区']
        elif location+'壮族自治区' in set(place_re.keys()):
            answer=place_re[location+'壮族自治区']
        elif location+'回族自治区' in set(place_re.keys()):
            answer=place_re[location+'回族自治区']
        elif location+'维吾尔自治区' in set(place_re.keys()):
            answer=place_re[location+'维吾尔自治区']
        return answer
    except:
        return'我在睡觉呢'

def food_rec(location='北京市'):#美食推荐
    try:
        if location in set(food_re.keys()):
            answer=food_re[location]
        elif location+'省' in set(food_re.keys()):
            answer=food_re[location+'省']
        elif location+'市' in set(food_re.keys()):
            answer=food_re[location+'市']  
        elif location+'自治州' in set(food_re.keys()):
            answer=food_re[location+'自治州']
        elif location+'特别行政区' in set(food_re.keys()):
            answer=food_re[location+'特别行政区']
        elif location+'自治区' in set(food_re.keys()):
            answer=food_re[location+'自治区']
        elif location+'地区' in set(food_re.keys()):
            answer=food_re[location+'地区']
        elif location+'壮族自治区' in set(food_re.keys()):
            answer=food_re[location+'壮族自治区']
        elif location+'回族自治区' in set(food_re.keys()):
            answer=food_re[location+'回族自治区']
        elif location+'维吾尔自治区' in set(food_re.keys()):
            answer=food_re[location+'维吾尔自治区']
        return answer
    except:
        return'我在睡觉呢'
def route(location_from='对外经济贸易大学',location_to='故宫'):
    '''
    返回路线
    '''
    global chaxun
    set_chaxun(1)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=option)
    browser.get('https://www.amap.com/')
    try:
        #找路线
        show_input=browser.find_element_by_css_selector('.fa-dir.icontip')
        show_input.click()
        time.sleep(1)
        select_bus=browser.find_element_by_id('busTab')
        select_bus.click()
        input_from=browser.find_element_by_id('dir_from_ipt')
        input_from.clear()#清除文本框里的内容
        input_from.send_keys(location_from)#输入起始地
        input_to=browser.find_element_by_id('dir_to_ipt')
        input_to.clear()#清楚文本框里的内容
        input_to.send_keys(location_to)#输入关键词
        browser.find_element_by_class_name('dir_submit').click()
        time.sleep(0.8)
        forage=browser.find_element_by_xpath("//*[@id='fromPoiList']").find_elements_by_css_selector('.iconfont.icon-whytip.choose_type')
        if forage!=[]:#起点模糊
            start=browser.find_elements_by_xpath("//*[@id='fromPoiList']/div[1]/div[1]/ul[1]/li[1]/h3[1]")
            start[0].click()
        time.sleep(0.5)
        forag_end=browser.find_element_by_xpath("//*[@id='toPoiList']").find_elements_by_css_selector('.iconfont.icon-whytip.choose_type')
        if forag_end!=[]:#终点模糊
            end=browser.find_elements_by_xpath("//*[@id='toPoiList']/div[1]/div[1]/ul[1]/li[1]/h3[1]")
            end[0].click()
        time.sleep(0.8)
        extend=browser.find_element_by_xpath("//*[@id='plantitle_0']/div[1]/a[1]")#展开列表
        extend.click()
        cu_url=browser.current_url
        time.sleep(0.8)
        route=browser.find_element_by_class_name('p_route')
        route_text=route.get_attribute('innerHTML')
        browser.quit()
        route_list=route_text.split()
        incl_chi=[]
        for text in route_list:#将经过站点等无关变量剔除
            r1=re.compile('[\u4e00-\u9fa5]|>[A-G][0-9]{1,4}')
            pattern = r'>首|>末|<li>|</li>|p_icon|title=|station_num|时间|:|/趟|\d站|：'
            list_=r1.findall(text)
            list_2=re.findall(pattern,text)
            if list_!=[] and list_2==[]:
                incl_chi.append(text)
        final=[]#提取中文以及数字
        for text in incl_chi:
            text=text.replace('"0-0-0">','')
            text=re.sub('\d{1,2}px','',text)
            x=re.findall('[\u4e00-\u9fa5]|\d|（|）|\(|\)|\.|[A-G][0-9]{1,4}',text)#第一个为汉字，第二个是数字，后面是基本符号，最后为高铁号或者进出口号
            final.append(x)
        route=''#最终线路
        for str_ in final[:-1]:
            for each in str_:
                route+=each
            route+='-'
        for each in final[-1]:
            route+=each
        str1='小乖告诉你从{}到{}怎么走！'.format(location_from,location_to)
        str2=route
        str3=cu_url
        chaxun=(str1,str2,str3) #chaxun='主人要从{}去{}，小乖为主人推荐路线为{},具体可以参考{}哦，祝主人玩得开心！'.format(location_from,location_to,route,cu_url)
        return chaxun
    except:
        return'我在睡觉呢主人，您的地方小乖也找不到'

def get_route_thread(location_from='对外经济贸易大学',location_to='故宫'):
    global chaxun
    t1=Thread(target=route,args=(location_from,location_to))
    t1.start()
    return "正在查询相关信息，请稍后……"

