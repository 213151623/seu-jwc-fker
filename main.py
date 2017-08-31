#!/usr/bin/python
# -*- coding: utf-8 -*-

import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import io
import re
import time
import sys
import PIL
from PIL import Image

reload(sys)
sys.setdefaultencoding("utf-8")


STANDARD = [
    [18.714286, 27.142857, 32.857143, 36.714286, 38.285714, 41.571429, 43.000000, 44.714286, 46.285714, 48.285714,
     48.285714, 36.428571, 27.714286, 24.714286, 23.285714, 22.285714, 21.428571, 19.428571, 19.285714, 19.000000,
     18.857143, 18.714286, 19.714286, 20.571429, 20.714286, 22.714286, 26.571429, 28.000000, 35.571429, 46.714286,
     46.714286, 44.857143, 43.000000, 41.285714, 39.571429, 36.142857, 34.428571, 31.000000, 26.000000, 18.714286],
    [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
     0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
    [8.333333, 8.333333, 16.166667, 23.166667, 24.166667, 26.000000, 27.000000, 27.833333, 27.500000, 29.000000,
     29.500000, 30.333333, 30.000000, 30.000000, 28.666667, 27.666667, 27.333333, 27.833333, 28.000000, 28.333333,
     29.833333, 31.333333, 33.333333, 35.166667, 38.000000, 43.000000, 41.833333, 40.833333, 39.666667, 37.666667,
     36.833333, 34.500000, 32.333333, 29.500000, 26.500000, 21.500000, 7.333333, 7.166667, 7.166667, 7.333333],
    [8.200000, 8.400000, 8.400000, 8.200000, 13.200000, 18.800000, 19.000000, 19.400000, 19.000000, 26.000000,
     26.200000, 26.400000, 25.400000, 26.200000, 26.000000, 26.400000, 27.400000, 27.200000, 28.400000, 29.200000,
     31.200000, 33.200000, 36.400000, 41.400000, 46.800000, 48.800000, 52.600000, 51.200000, 49.200000, 48.200000,
     45.200000, 40.600000, 37.600000, 33.600000, 25.800000, 18.000000, 13.800000, 7.000000, 7.000000, 7.200000],
    [17.250000, 19.000000, 20.500000, 21.875000, 24.125000, 25.375000, 26.375000, 28.250000, 28.500000, 28.125000,
     28.000000, 27.750000, 25.875000, 25.250000, 25.125000, 26.250000, 25.000000, 24.625000, 25.625000, 24.750000,
     24.500000, 24.500000, 25.375000, 24.500000, 52.000000, 52.250000, 52.750000, 52.875000, 53.750000, 55.375000,
     55.125000, 55.000000, 54.625000, 18.625000, 18.375000, 18.375000, 18.250000, 17.750000, 17.375000, 9.875000],
    [8.428571, 8.285714, 8.142857, 8.285714, 8.428571, 8.285714, 14.000000, 36.285714, 36.142857, 35.857143, 36.000000,
     36.000000, 36.142857, 31.714286, 27.000000, 26.857143, 27.714286, 27.571429, 27.714286, 28.714286, 27.857143,
     29.142857, 29.714286, 31.000000, 34.142857, 41.000000, 40.142857, 39.285714, 38.000000, 37.857143, 36.428571,
     35.000000, 33.571429, 32.000000, 28.428571, 15.714286, 8.285714, 8.285714, 8.285714, 8.142857],
    [8.142857, 20.571429, 27.857143, 32.285714, 35.857143, 38.428571, 40.857143, 44.000000, 46.000000, 46.857143,
     47.571429, 49.142857, 37.000000, 32.857143, 29.857143, 27.428571, 25.714286, 26.285714, 25.571429, 24.714286,
     25.428571, 24.285714, 24.714286, 24.285714, 26.142857, 27.428571, 28.571429, 31.142857, 34.285714, 41.142857,
     40.857143, 39.142857, 37.571429, 36.571429, 34.571429, 32.857143, 24.000000, 21.714286, 16.428571, 8.000000],
    [8.428571, 8.285714, 8.142857, 8.285714, 8.285714, 8.285714, 16.285714, 16.285714, 19.000000, 21.857143, 24.000000,
     25.285714, 25.857143, 27.714286, 29.857143, 31.000000, 32.857143, 34.571429, 35.285714, 32.714286, 30.142857,
     29.571429, 29.142857, 28.142857, 27.285714, 27.000000, 26.000000, 26.857143, 26.428571, 26.285714, 26.428571,
     26.714286, 25.142857, 24.571429, 23.571429, 21.571429, 20.857143, 18.714286, 17.571429, 17.000000],
    [7.500000, 7.500000, 13.833333, 18.833333, 21.333333, 29.666667, 36.500000, 40.333333, 43.333333, 47.166667,
     49.833333, 52.833333, 48.666667, 45.833333, 37.500000, 33.500000, 30.833333, 30.000000, 28.000000, 27.500000,
     28.666667, 27.666667, 28.500000, 29.166667, 32.833333, 33.833333, 36.000000, 40.333333, 47.666667, 52.166667,
     49.166667, 47.166667, 44.166667, 40.666667, 37.166667, 32.500000, 27.000000, 18.833333, 14.833333, 8.000000],
    [8.142857, 15.857143, 20.285714, 24.142857, 30.428571, 32.571429, 34.142857, 36.285714, 38.142857, 38.000000,
     39.571429, 32.428571, 29.571429, 27.571429, 26.571429, 25.714286, 25.714286, 23.714286, 23.857143, 23.428571,
     24.428571, 23.142857, 23.000000, 26.285714, 26.285714, 26.428571, 30.000000, 33.857143, 39.000000, 50.142857,
     49.285714, 47.857143, 47.428571, 45.571429, 44.285714, 41.142857, 38.714286, 34.142857, 29.428571, 20.714286]
]


def getCheckCode():
    for i in range(10):
        try:
            image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode', timeout = 10)
            break
        except Exception, e:
            print e
            continue
    else:
        print u'网络连接失败，请重试'
        return

    img = Image.open(io.BytesIO(image.read()))
    start = [13, 59, 105, 151]
    result = ''
    for i in start:
        sample = []
        for i in xrange(i, i + 40):
            temp = 0
            for j in xrange(0, 100):
                temp += (img.getpixel((i, j))[1] < 40)
            sample.append(temp)
        min_score = 1000
        max_match = 0
        for idx, val in enumerate(STANDARD):
            diff = []
            for i in xrange(len(sample)):
                diff.append(sample[i] - val[i])
            avg = float(sum(diff)) / len(diff)

            for i in xrange(len(sample)):
                diff[i] = abs(diff[i] - avg)
            score = sum(diff)
            if score < min_score:
                min_score = score
                max_match = idx

        result = result + str(max_match)
    return (result, img)


def loginIn(userName, passWord):
    #设置cookie处理器
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
    urllib2.install_opener(opener)
    
    (code, img) = getCheckCode()
    while len(code) != 4:
        (code, img) = getCheckCode()
    print u"验证码识别为： " + code

    #构造post数据
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
    header ={   
        'Host' : 'xk.urp.seu.edu.cn',   
        'Proxy-Connection' : 'keep-alive',
        'Origin' : 'http://xk.urp.seu.edu.cn',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
        'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
        }
    data = {
        'userId' : userName,
        'userPassword' : passWord, #你的密码，  
        'checkCode' : code,           #验证码 
        'x' : '33',     #别管
        'y' : '5'       #别管2
        }
    
    #post登录数据
    (state, text) = postData(posturl,header,data)
    url = ''
    if state == True:
        if (text.find('选课批次') != -1):  # a bad label; the url returned should be the best
            print u"登录成功"
            function = re.search(r'onclick="changeXnXq.*\)"', text); # find the function whose parameter are desired
            function = function.group()     
            parameters = re.search(r"'(.*)','(.*)','(.*)'\)", function) # fetch url parameters
            url = "http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=" + parameters.group(1) + "&selectXq=" + parameters.group(2) + "&selectTime=" + parameters.group(3)
        else:
            state = False
            errorMessage = re.search(r'id="errorReason".*?value="(.*?)"', text)
            text = errorMessage.group(1)
    else:
        text = "网络错误，登录失败" 
    return (state, text, url)

def selectSemester(semesterNum, url):
    print u"切换学期菜单中......"
    time.sleep(5)

    geturl = re.sub('selectXq=.', 'selectXq='+str(semesterNum), url)
    
    header = {  'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',        
    }
    data = {}
    #get获取学期课程
    (state, text) = getData(geturl,header,data)
    if state == True:
        if text.find("数据异常") != -1:  # switched to an unavailable semester
            state = False
            text = "目前无法选择学期" + str(semesterNum)
    return (state, text)

def postData(posturl,headers,postData):
    postData = urllib.urlencode(postData)  #Post数据编码   
    request = urllib2.Request(posturl, postData, headers)#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
    text = ''
    for i in range(10):
        try:
            response = urllib2.urlopen(request, timeout = 5)
            text = response.read()
            break
        except Exception, e:
            print 'fail to get response'
            print 'trying to open agian...'
            continue
    else:
        return (False, "数据发送失败")
    return (True, text)

def getData(geturl,header,getData, returnUrl = False):
    getData = urllib.urlencode(getData)
    request = urllib2.Request(geturl, getData, header)
    text = ''
    url = ''
    for i in range(10):
        try:
            response = urllib2.urlopen(request, timeout = 5)
            text = response.read()
            url = response.geturl()
            break
        except Exception, e:
            print e
            print 'trying to open agian...'
            continue
    else:
        if returnUrl == False:
            return (False, "获取数据失败")
        else:
            return (False, "获取数据失败", '')

    if returnUrl == False:
        return (True, text)
    else:
        return(True, text, url)

def stateCheck(textValue):    
    text = textValue
    if (text.find('成功选择') != -1)or(text.find('服从推荐') != -1):
        return 0
    if text.find('已满') != -1:
        return 1
    if text.find('失败') != -1:
        return 2

def Mode1(semesterNum, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    #寻找可以“服从推荐”的课程
    print u"==============\n模式1，开始选课\n=============="
    courseList = []
    pattern = re.compile(r'\" onclick=\"selectThis\(\'.*\'')
    pos = 0
    m = pattern.search(text,pos)
    while m:
        pos = m.end()
        tempText = m.group()
        parameters = re.search(r"selectThis\('(.*?)','(.*?)','(.*?)'", tempText)
        course = [parameters.group(1),parameters.group(2),parameters.group(3),1]
        courseList.append(course)
        m=pattern.search(text,pos)  #寻找下一个
    times = 0
    success = 0
    total = len(courseList)
    while True:
        if total == 0:
            print u"目前没有课可以选择"
            break
        time.sleep(3)#sleep
        times = times +1
        print u"\n第"+str(times)+u"次选课，已经成功选择"+str(success)+u"门"
        for course in courseList:
            if course[3] == 1:
            #构造选课post
                posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+course[1]+'&select_xkkclx='+course[2]+'&select_jhkcdm='+course[0]
                headers = { 'Host' : 'xk.urp.seu.edu.cn',
                        'Proxy-Connection' : 'keep-alive',
                        'Content-Length' : '2',
                        'Accept' : 'application/json, text/javascript, */*',
                        'Origin':'http://xk.urp.seu.edu.cn',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        }
                data = {'{}':''
                }
                #post选课包，并获取返回状态
                (state, text) = postData(posturl,headers,data)
                if state == False:
                    text = '网络错误'
                else:
                    if text.find('isSuccess":"false') != -1:
                        state = False
                        text = re.search(r'errorStr":"(.*?)"', text).group(1)
                if state == True:
                    course[3] = 0
                    success += 1
                    total -= 1
                    print u"Nice, 课程"+str(course[0])+u" 选择成功"
                else:
                    print u"课程"+str(course[0])+u" 选课失败，" + text.decode('utf-8')
       
def Mode2(semesterNum,courseName, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    print u"==============\n模式2，开始选课\n=============="
    #获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    (state, text) = getData(geturl1,header1,data1)
    if state == False:
        print u"打开课程列表页面失败"
        return
    #构造RE  
    #print text

    pattern = (courseName + '.*?(\"8%\" id=\"(.{0,20})\" align)')  # possible problem here??
    #获取课程编号
    courseNo = re.findall(pattern,text,re.S)[0][1]
    #构造数据包
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    print u"我开始选课了,课程编号："+courseNo
    times = 0
    while True :
        #判断是否选到课
        times = times+1
        (state, text) = getData(geturl1,header1,data1)
        if state == False:
            print "打开课程列表页面失败"
            return
        pattern2 = ('已选(.{0,200})align=\"')
        result = re.findall(pattern2,text,re.S)
        #print result
        success = len(result) #为0为不成功 继续
        if (success != 0)and(result[0].find(courseNo)!=-1):
            print u"Nice，已经选到课程:"+courseNo
            break
        #发送选课包
        print u"第"+str(times)+"次尝试选择课程"+courseNo+u",但是没选到！"
        (state, text) = postData(posturl,headers,data)
        time.sleep(3)#sleep
    return 
def postRw(courseNo):
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    (state, text) = postData(posturl,headers,data)
    return (state, text)
def checkRwState(text):
    if text.find('true') != -1:  #选课成功
        return 0
    if text.find('名额已满') != -1:
        return 1
    if text.find('冲突') != -1:
        return 2
    return -1
def Mode3(semesterNum, url):    
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print text.decode('utf-8')
        print u'切换到学期' + str(semesterNum) + u"失败"
        return
    else:
        print u'切换到学期' + str(semesterNum) + u"成功"
    print u"==============\n模式3，开始选课\n=============="
    #获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    (state, text) = getData(geturl1,header1,data1)
    if state == False:
        print u"打开课程列表页面失败"
        return

    #获取所有的课程编号
    pattern = ('\"8%\" id=\"(.{0,20})\" align')
    courseList = re.findall(pattern,text,re.S)
    #print courseList 
    courseCtList =[]
    #找出并去掉冲突的课程
    for course in courseList:
        (state, backText) = postRw(course)
        if state == True:  # ewww bad name here
            state = checkRwState(backText)
        else:
            state = -1  # network error or something else
        if state == 2:
            courseCtList.append(course)
        if state == 0:
            print u"Nice 选到了一门课："+course
            return   #成功了
    #print courseCtList
    courseTemp = [i for i in courseList if (i not in courseCtList)]
    #print courseTemp
    times = 0
    while True:
        times = times + 1
        #找出已满的课程
        pattern = ('已满.+?(\"8%\" id=\")(.{0,20})\" align')
        courseYmList = [i[1] for i in re.findall(pattern,text,re.S)]
        #print courseYmList
        #找出可以选的课程编号
        courseAva = [i for i in courseTemp if (i not in courseYmList) ]
        #选课了
        if len(courseAva) == 0:
            print u"第"+str(times)+u"次刷新，每门课都选不了.."
        else:
            for course in courseAva:
                (state, text) = postRw(course)
                if state == True:
                    state = checkRwState(text)
                else:
                    state = -1
                if state == 0:
                    print u"Nice 选到了一门课："+course
                    return
                if state == 1:
                    print u"人品不好 眼皮子底下的课被抢了"
        #刷新人文选课界面
        (state, text) = getData(geturl1,header1,data1)
        if text.count('已选') == 3:  # in case of multi-instances
            print u"已经选到一门课了"
            break

        if state == False:
            print u"打开课程列表页面失败"
            return


if __name__ == "__main__":
    print u"\n\n\n\n"
    print u"===================================================================== "
    print u"                 Seu_Jwc_Fker 东南大学选课助手变态版"
    print u"===================================================================== "
    print u"请选择模式："
    print u"1. 同院竞争臭表脸模式：只值守主界面本院的所有“服从推荐”课程"
    print u"2. 孤注一掷模式：只值守子界面“人文社科类”中你指定一门课程"
    print u"3. 暴力模式：值守子界面“人文社科类”任意一门课程，有剩余就选上"
    
    mode = input(u'\n请输入模式编号(如:1)：')
    userId = raw_input(u'请输入一卡通号(如:213111111)：')
    passWord = raw_input(u'请输入密码(如:65535)：')
    semester = input(u'请输入学期编号(短学期为1，秋季学期为2，春季学期为3)：')

    (state, text, url) = loginIn(userId,passWord)
    while state == False:
        print text.decode('utf-8')
        (state, text, url) = loginIn(userId, passWord)

    if state == True:
        if 1 == mode:
            Mode1(semester, url)
        if 2 == mode:
            courseName = raw_input(u'请输入你想值守的人文课名称或者其关键词（如:音乐鉴赏）：')
            try:
                courseName.decode('utf-8')
            except:
                courseName.decode('gbk').encode('utf-8')
            Mode2(semester,courseName, url)
        if 3 == mode:
            Mode3(semester, url)
    else:
        print u"要不试试退出后重启一下本程序？"
    raw_input(u'按任意键退出')
