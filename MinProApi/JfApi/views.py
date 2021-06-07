from logging import ERROR
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import time
import socket
import re
import urllib.error
# 第三方随机请求头库，贼好用
from fake_useragent import UserAgent
# from soupsieve.css_match import RE_WEEK

# 无界浏览器需要的包
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import copy
from lxml import etree


def mywork(request):
    return render(request,'index.html')

# Create your views here.
# 构造请求头

READ_TIME_OUT="READ TIME OUT"
CON_TIME_OUT="CONCET TIME OUT"
WRONG_EXPRESSION="输入的表达式有误"
NO_POINT="无法积分"
BEYOND_COMPUTATION="无法计算"

# ANS_IMG="http://towxml.vvadd.com/?tex="

headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    # 这个请求头是默认的
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Referer": "https://zh.numberempire.com/integralcalculator.php",
    "Connection":"keep-alive"
}
def enterview(request):
    NUM=request.POST['NUM_CHOIC']
    NUM=int(NUM)
    if NUM==0:
        return render(request,'bdjf.html')
    elif NUM==1:
        return render(request,'hsqd.html')
    elif NUM==2:
        return render(request,'ysfj.html')
    elif NUM==3:
        return render(request,'djf.html')
    elif NUM==4:
        return render(request,'jx.html')
    elif NUM==5:
        return render(request,'hj.html')
    
def indexview(request):
    return render(request,'ENTER.html')


# 
def jfview(request):
    # 定义异常消息
    ERROR_MSG=""

    # 结果图片
    ANS_IMG="http://towxml.vvadd.com/?tex="
    if request.method!="POST":
        ERROR_MSG="COMMIT TYPE ERROR"
        return HttpResponse(ERROR_MSG)
        
    # 获取小程序传来 的NUM参数来选择使用哪个计算器
    # NUM_CHOIC=request.POST['NUM_CHOIC']
    NUM_CHOIC=request.POST.get('NUM_CHOIC')
    NUM_CHOIC=int(NUM_CHOIC)    
    def getUrl(Num):
        Tool_url=[
        "https://zh.numberempire.com/integralcalculator.php",#不定积分工具0
        "https://zh.numberempire.com/derivativecalculator.php",#函数求导工具1
        "https://zh.numberempire.com/factoringcalculator.php",#因式分解工具 2
        "https://zh.numberempire.com/definiteintegralcalculator.php",#定积分 3
        "https://zh.numberempire.com/limitcalculator.php",#极限计算器 4
        "https://zh.numberempire.com/simplifyexpression.php"#表达式化简器5
        ]
        return Tool_url[Num]
    def getPostType(Num):
        if Num==0:
            postdata={
                "function":"",#表达式
                "var":"",#自变量
                "answers":"",#反爬变量
                "_p1":""#反爬参数
            }
        elif Num==1:
            postdata={
                "function":"",#表达式
                "var":"",#自变量
                "order":"",#求导阶数
                "_p1":""#反爬参数
            }
        elif Num==2:
            postdata={
                "function":"",
                "_p1":""
            }
        elif Num==3:
            postdata={
                "function":"",#表达式
                "var":"",#自变量
                "a":"",#积分左端点
                "b":"",#积分右端点
                "answers":"",#反爬变量
                "_p1":""#反爬参数
    
            }
        elif Num==4:
            postdata={
                "function":"",#表达式
                "var":"",#自变量
                "val":"",#展开点
                "answers":"",#反爬变量
                "limit_type":"",#极限类型
                "_p1":""#反爬参数
            }
        elif Num==5:
            postdata={
                "function":"",
                "_p1":""
            }
        return postdata    
    
    
    # 提取出密钥
    def getJM(ch):
        pattern=r"process1\('.*'\)"
        ans=re.findall(pattern, ch)
        ans=ans[0]
        pattern2=r"'(.+?)'"
        ans2=re.findall(pattern2, ans)
        ans2=ans2[0]
        return ans2
    
    def get_p1(process1):
        s=0
        # 将每个字符转换为Unicode编码，然后累加最后得到_p1
        for a in process1:
            s+=ord(a)
        return s
    
    def get_postdata(_p1,Num):
        if Num==0:
            # 不定积分
            postdata['function']=request.POST['function']
            postdata['var']=request.POST['var']
        elif Num==1:
            # 函数求导
            postdata['function']=request.POST['function']
            postdata['var']=request.POST['var']
            postdata['order']=request.POST['order']
        elif Num==2:
            # 因式分解
            postdata['function']=request.POST['function']
        elif Num==3:
            # 定积分
            postdata['function']=request.POST['function']
            postdata['var']=request.POST['var']
            postdata['a']=request.POST['a']
            postdata['b']=request.POST['b']
        elif Num==4:
            # 极限计算器
            limi=request.POST['limi']
            limi=int(limi)
            postdata['function']=request.POST['function']
            postdata['var']=request.POST['var']
            lmType=['two-sided','plus','minus']
            postdata['val']=request.POST['val']
            # selectType=input("极限类型：双侧极限 0\t右侧极限 1\t左侧极限2")
    
            postdata['limit_type']=lmType[limi]
        elif Num==5:
            # 表达式化简
            postdata['function']=request.POST['function']
        postdata['_p1']=_p1
    
    
    # 选择工具链接
    or_url=getUrl(NUM_CHOIC)
    # 选定提交的数据格式
    postdata=getPostType(NUM_CHOIC)

    
    # 获取随机请求头
    headers['User-Agent']=UserAgent().random
    headers['Referer']=or_url
    
    # 建立空列表，为了以指定格式存储头信息
    headall=[]
    for key,value in headers.items():
        item=(key,value)
        headall.append(item)
    
    
    # 设置cookie
    cjar=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar))
    
    # 将指定格式的headers添加上
    opener.addheaders=headall
    # 将opener安装为全局
    urllib.request.install_opener(opener)
    try:
        data_t=urllib.request.urlopen(or_url,timeout=10)
        try:
            data=data_t.read()
        except:
            # print("read time out")
            ERROR_MSG=READ_TIME_OUT
            # 返回读取超时异常
            return HttpResponse(ERROR_MSG)

        soup_obj=BeautifulSoup(data,"html.parser")
        
        # 找出body标签中所有script标签
        scriptList=soup_obj.select("body script")
        i=1
        for sc in scriptList:
            if i==7:
                if sc is not None:
                    str1=sc.contents[0]
            else:
                i=i+1
        
        process1=getJM(str1)
        _p1=get_p1(process1)
        
        
        # 获取提交数据
        get_postdata(_p1,NUM_CHOIC)
        # 对提交的数据进行编码
        postdata=urllib.parse.urlencode(postdata).encode('utf-8')
        # 构造post请求
        req=urllib.request.Request(or_url,postdata)
        try:
            file1=opener.open(req,timeout=10)
            # print(file1)

            try:
                data_text=file1.read()

            except:
                ERROR_MSG=READ_TIME_OUT
                # 返回读取超时异常
                return HttpResponse(ERROR_MSG)
            # file1=open("ans.html","wb")
            # file1.write(data_text)
            # file1.close()
            j=1
            ans_soup=BeautifulSoup(data_text,"html.parser")
            ansScriptList=ans_soup.select("body script")
            # 提取出计算结果的公式代码
            for sc in ansScriptList:
                if j==6:
                    if sc is not None:
                        result_ans=sc.contents[0]
                        result_ans=urllib.parse.quote_plus(result_ans)
                        ANS_IMG=ANS_IMG+result_ans
                    break
                else:
                    j=j+1

            bs_ans=BeautifulSoup(data_text,"html.parser")        
            #提取出计算结果盒子中的内容
            js_ans=bs_ans.find("span",attrs={'id':'result1'})
            if js_ans is not None:
                if js_ans.contents is not None:
                    if len(js_ans.contents)!=0:

                        # 得到计算结果
                       js_ans=js_ans.contents[0]
                       msg={"status":"计算成功","result_text":"","ans_img":""}
                       msg['result_text']=js_ans
                       msg['ans_img']=ANS_IMG
                       #以JSON的数据格式返回给前端
                       return JsonResponse(msg)

                    # 测试用
                    #    return render(request,'result.html',{
                    #        "msg":msg,
                    #        "ANS_IMG":ANS_IMG
                    #    })
                    else:
 
                        ERROR_MSG=NO_POINT
                        return HttpResponse(ERROR_MSG)
                else:
                    ERROR_MSG=WRONG_EXPRESSION
                    return HttpResponse(ERROR_MSG)
            else:
                ERROR_MSG=WRONG_EXPRESSION
                return HttpResponse(ERROR_MSG)
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                ERROR_MSG=e.code
                return HttpResponse(ERROR_MSG)
            if hasattr(e,"reason"):
                ERROR_MSG=e.reason
                return HttpResponse(ERROR_MSG)
            if isinstance(e.reason,socket.timeout):
                ERROR_MSG=CON_TIME_OUT
                return HttpResponse(ERROR_MSG)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):

            ERROR_MSG=e.code
            return HttpResponse(ERROR_MSG)
        if hasattr(e,"reason"):
            ERROR_MSG=e.reason
            return HttpResponse(ERROR_MSG)
        if isinstance(e.reason,socket.timeout):
            ERROR_MSG=CON_TIME_OUT
            return HttpResponse(ERROR_MSG)
    
def yzmViews(request):
    # 设置无界面执行无头浏览器
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    
    
    # 设置无头浏览器的位置
    driver=webdriver.Chrome(executable_path='../static/headless/chromedriver.exe')
    driver.set_page_load_timeout(15)
    # 打开教务系统页面
    driver.get('https://cas.gzhu.edu.cn/cas_server/login')
    
    yzm=driver.find_element_by_xpath('//div[@class="loginBox"]//div[@class="box"]//div[@class="row"]/img')
    # 截取验证码区域的图片
    yzm.screenshot('../static/yzm/yzm.png')
    
    # 模拟登陆
    # username=input('学号')
    # passw=input('密码')
    ma=input('验证码')
    driver.find_element_by_name('username').send_keys('1906200121')
    driver.find_element_by_name('password').send_keys('.@001130@wwmsx')
    driver.find_element_by_name('captcha').send_keys(ma)
    
    # 点击登陆
    try:
       login=driver.find_element_by_name('submit').click()
    except:
        print('直接跳过不加载了')
    
    # 进入教务系统页面
    driver.get('http://jwxt.gzhu.edu.cn/sso/lyiotlogin')
    
    
    try:
         driver.get('http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508&layout=default&su=1906200121')
         alert = driver.switch_to_alert()
         '''添加等待时间'''
         time.sleep(2)
         '''获取警告对话框的内容'''
         alert.accept()   #alert对话框属于警告对话框，这里只能接受弹窗
    except:
        print('第一个链接不行')
    finally:
        driver.get('http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default&su=1906200121')
    
    # 在这里停两秒，否则课表加载不出来
    sleep(2)
    
    def getPage():
        # global driver
        page_data=driver.page_source
        sleep(1)
        page_data=bytes(page_data,encoding='utf-8')
        return page_data
    
    html=getPage()
    selector=etree.HTML(html)
    
    driver.close()
    
    course={
        'cname':'',#课程名称
        'weekNum':'',#周数
        'addr':'',#上课地点
        'teacher':'',#老师
        'testType':'',#考核方式
        'allClass':'',#总学时
    }
    
    
    #有一些存在调课情况的课程，会有两个盒子
    Course=[]
    Change=[]
    
    # 分别创建课程矩阵，和调课矩阵
    for i in range(5):
        Course.append([])
        Change.append([])
        for j in range(7):
            Course[i].append(copy.deepcopy(course))
            Change[i].append(copy.deepcopy(course))
    
    def getLession(num,pianyi):
        # global Course
        # global Change
        for i in range(7):
            try:
                cname=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]//font')
                week=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div//p[1]/font')
                addr=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div//p[2]/font')
                teacher=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div//p[3]/font')
                testType=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div//p[5]/font')
                allClass=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div//p[7]/font')
               
                Course[num-pianyi][i]['cname']=cname[0].text
                Course[num-pianyi][i]['weekNum']=week[0].text
                Course[num-pianyi][i]['addr']=addr[0].text
                Course[num-pianyi][i]['teacher']=teacher[0].text
                Course[num-pianyi][i]['testType']=testType[0].text
                Course[num-pianyi][i]['allClass']=allClass[0].text
    
                try:
                    cname_=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]//div[2]//font')
                    week_=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div[2]//p[1]/font')
                    addr_=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div[2]//p[2]/font')
                    teacher_=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div[2]//p[3]/font')
                    testType_=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div[2]//p[5]/font')
                    allClass_=selector.xpath('//tbody//td[@id="'+str(i+1)+'-'+str(num)+'"]/div[2]//p[7]/font')
    
                    Change[num-pianyi][i]['cname']=cname_[0].text
                    Change[num-pianyi][i]['weekNum']=week_[0].text
                    Change[num-pianyi][i]['addr']=addr_[0].text
                    Change[num-pianyi][i]['teacher']=teacher_[0].text
                    Change[num-pianyi][i]['testType']=testType_[0].text
                    Change[num-pianyi][i]['allClass']=allClass_[0].text
    
                except:
                    print('没有调课情况')      
            except:
                continue
    py=1
    num=1
    for i in range(5):
        getLession(num,py)
        num+=2
        py+=1
    
    print(Course)
    print(Change)
    

