import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from config import userlist,urllist

chrome_options = Options()
# 个人资料路径
user_data_dir = r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
chrome_options.add_argument(user_data_dir)
# 启动浏览器配置
driver = webdriver.Chrome(chrome_options=chrome_options)
#设置隐性等待30秒
driver.implicitly_wait(30)

#获取用户名和密码
def user_pwd(user_list):
    namelist = []
    pwdlist = []
    for i in user_list:
        reult = i.split()
        user = reult[0]
        namelist.append(user)
        pwd = reult[1]
        pwdlist.append(pwd)
    return namelist,pwdlist

def login(driver,username,password):
    driver.get("https://www.amazon.it/dp/B07CM3655D")
    time.sleep(2)
    print("登录的用户名：" + username)
    print("登录的密码：" + password)
    # 判断页面是否登录(如果登录了先退出登录，如果没登录跳转登录页面)
    try:
        # 识别需要悬停的元素
        ele = driver.find_element_by_class_name('nav-line-2')
        # 鼠标移到悬停元素上
        ActionChains(driver).move_to_element(ele).perform()
        time.sleep(1)
        # 点击退登按钮
        driver.find_element_by_xpath("//*[@id='nav-item-signout']/span").click()
        print("退出当前账号，跳转登录页面")
    except:
        time.sleep(1)
        driver.find_element_by_class_name('nav-action-inner').click()
        print("跳转登录页面")

    # 登录账号并使窗口最大化
    # 输入用户名和密码
    time.sleep(1)
    js = 'document.querySelector("#ap_email").value="";'
    driver.execute_script(js);
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='ap_email']").send_keys(username)
    driver.find_element_by_xpath("//*[@id='continue']").click()
    time.sleep(1)
    js = 'document.querySelector("#ap_password").value="";'
    driver.execute_script(js);
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='ap_password']").send_keys(password)
    driver.find_element_by_xpath("//*[@id='signInSubmit']").click()
    time.sleep(1)
    # driver.get("https://www.amazon.it/dp/B07CM3655D")
    # time.sleep(3)

#添加购车操作
def addshop(driver,urllist):
    for i in urllist:
        try:
            driver.get(i)
            #判断秒杀是否达到90%
            numberstr = str(driver.find_element_by_xpath('//*[@class="a-size-small a-color-base a-text-bold"]').text)
            numberint = int(numberstr.strip("%"))
            print(numberint)
            if(numberint>=90):
                print("秒杀已达到90%，不进行点击")
            else:
                #点击加入购物车
                driver.find_element_by_xpath('//*[@id="a-autoid-0-announce"]').click()
                time.sleep(2)
                print("添加购物车成功")

        except:
            print("未找到该秒杀按钮，可能秒杀已结束")

def test1(driver,userlist,urllist):
    #获取用户名和密码列表
    namelist,pwdlist = user_pwd(userlist)

    for i in range(len(namelist)):
        login(driver,namelist[i],pwdlist[i])
        addshop(driver,urllist)


test1(driver,userlist,urllist)