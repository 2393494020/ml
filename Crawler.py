from datetime import datetime

from urllib import parse,request
from urllib.request import urlretrieve
from http import cookiejar

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from PIL import Image
from bs4 import BeautifulSoup

import json
import re
import time

# python -m pip install selenium
# python -m pip install beautifulsoup4
# python -m pip install pillow
# python -m pip install lxml
# http://chromedriver.chromium.org/downloads

def verifyCode(proxy_addr):
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    url = 'http://www.sai9769.com/index.htm'

    cookie = cookiejar.CookieJar()
    cookieHandler = request.HTTPCookieProcessor(cookie)

    if (len(proxy_addr) > 0):
        proxy = request.ProxyHandler({'http': proxy_addr})
        opener = request.build_opener(proxy, request.HTTPHandler, cookieHandler)
    else:
        opener = request.build_opener(cookieHandler)

    request.install_opener(opener)

    req = request.Request(url=url, headers=header_dict)
    res = opener.open(req)
    res = res.read()
    
    token = ''
    
    for line in res.decode(encoding='utf-8').split('\n'):
        it = re.finditer('[a-zA-Z0-9]{32}', line)
        for match in it: 
            token = match.group()


    print(token)

    url = 'http://www.sai9769.com/verifyCodeAjax.htm'
    
    data_dict = {
        'action':'create', 
        'type': 6, 
        'function':1, 
        'sendto':'18802074098', 
        'token':token
    }
    req_data = parse.urlencode(data_dict).encode(encoding='utf-8')

    header_dict['Host'] = 'www.sai9769.com'
    header_dict['Origin'] = 'http://www.sai9769.com'
    header_dict['Referer'] = 'http://www.sai9769.com/index.htm'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'

    req = request.Request(url=url, data=req_data, headers=header_dict)
    res = opener.open(req)
    res = res.read()

    print(json.loads(res))

    log = open('D:\\crawler.log', 'a')
    log.write('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] : ' + json.dumps(json.loads(res)) + '\n')
    log.close()

def get_image_info(browser, img):
    soup = BeautifulSoup(browser.page_source, 'lxml')
    imgs = soup.find_all('div', {'class': 'gt_cut_' + img + '_slice'})    
    img_url = re.findall('url\(\"(.*)\"\);', imgs[0].get('style'))[0].replace('webp', 'jpg')    
    urlretrieve(url=img_url, filename=img + '.jpg')
    image = Image.open(img +'.jpg')
    position = get_position(imgs)
    return image, position

def get_position(img): 
    img_position = []
    for small_img in img:
        position = {}
        position['x'] = int(re.findall('background-position: (.*)px (.*)px;', small_img.get('style'))[0][0])
        position['y'] = int(re.findall('background-position: (.*)px (.*)px;', small_img.get('style'))[0][1])
        img_position.append(position)
    
    return img_position

def Corp(image, position): 
    # 第一行图片信息
    first_line_img = []
    # 第二行图片信息
    second_line_img = []
    for pos in position:
        if pos['y'] == -58:
            first_line_img.append(image.crop((abs(pos['x']), 58, abs(pos['x']) + 10, 116)))
        if pos['y'] == 0:
            second_line_img.append(image.crop((abs(pos['x']), 0, abs(pos['x']) + 10, 58)))
    return first_line_img, second_line_img

def put_imgs_together(first_line_img, second_line_img, img_name):
    image = Image.new('RGB', (260,116))
    # 初始化偏移量为0
    offset = 0
    # 拼接第一行
    for img in first_line_img:
        # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
        image.paste(img, (offset, 0))
        # 偏移量对应增加移动到下一个图片位置,size[0]表示图片宽度
        offset += img.size[0]
    # 偏移量重置为0
    x_offset = 0
    # 拼接第二行
    for img in second_line_img:
        # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
        image.paste(img, (x_offset, 58))
        # 偏移量对应增加移动到下一个图片位置，size[0]表示图片宽度
        x_offset += img.size[0]
    # 保存图片
    image.save(img_name)
    # 返回图片对象

    return image

def is_pixel_equal(bg_image, fullbg_image, x, y):
    bg_pixel = bg_image.load()[x, y]
    # 获取完整图片的像素点(按照RGB格式)
    fullbg_pixel = fullbg_image.load()[x, y]
    # 设置一个判定值，像素值之差超过判定值则认为该像素不相同
    threshold = 60
    # 判断像素的各个颜色之差，abs()用于取绝对值
    if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold) and abs(bg_pixel[2] - fullbg_pixel[2] < threshold)):
        # 如果差值在判断值之内，返回是相同像素
        return True
 
    else:
        # 如果差值在判断值之外，返回不是相同像素
        return False

def get_distance(bg_image, fullbg_image): 
    # 滑块的初始位置
    distance = 57
    # 遍历像素点横坐标
    for i in range(distance, fullbg_image.size[0]):
        # 遍历像素点纵坐标
        for j in range(fullbg_image.size[1]):
            # 如果不是相同像素
            if not is_pixel_equal(fullbg_image, bg_image, i, j):
                # 返回此时横轴坐标就是滑块需要移动的距离
                return i

def get_trace(distance): 
    # 创建存放轨迹信息的列表
    trace = []
    # 设置加速的距离
    faster_distance = distance * (3 / 5)
    # 设置初始位置、初始速度、时间间隔
    start, v0, t = 0, 0, 0.5
    # 当尚未移动到终点时
    while start < distance:
        # 如果处于加速阶段
        if start < faster_distance:
            # 设置加速度为2
            a = 2
        # 如果处于减速阶段
        else:
            # 设置加速度为-3
            a = -3
        # 移动的距离公式
        move = v0 * t + (1 / 2) * a * t * t
        # 此刻速度
        v = v0 + a * t
        # 重置初速度
        v0 = v
        # 重置起点
        start += move
        # 将移动的距离加入轨迹列表
        trace.append(round(move))
    
    return trace

def move_to_gap(browser, trace):
    # print(trace)
    
    slider = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
    # 使用click_and_hold()方法悬停在滑块上，perform()方法用于执行
    ActionChains(browser).click_and_hold(slider).perform()
    for x in trace:
        # 使用 move_by_offset()方法拖动滑块，perform()方法用于执行
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    # 模拟人类对准时间
    time.sleep(2)
    
    ActionChains(browser).release().perform()

def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:1080')
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')

    browser = webdriver.Chrome(executable_path='D:\\github\\ml\\chromedriver.exe', chrome_options=chrome_options)
    # browser = webdriver.Chrome(executable_path='E:\\github\\ml\\chromedriver.exe')
    browser.get('https://www.tianyancha.com')
    # browser.maximize_window()

    try:
        time.sleep(5)
        browser.find_element_by_link_text('登录/注册').click()
        
        time.sleep(2)
        browser.find_element_by_xpath('//div[@id="_modal_container"]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/input').send_keys('18802074098')

        time.sleep(2)
        browser.find_element_by_id('smsCodeBtnPopup').click()

        time.sleep(2)
        retry = 3
        while(browser.find_element_by_id('smsCodeBtnPopup').text == '获取验证码' and retry > 0):
            bg, bg_position = get_image_info(browser, 'bg')
            fullbg, fullbg_position = get_image_info(browser, 'fullbg')

            bg_first_line_img, bg_second_line_img = Corp(bg, bg_position)
            fullbg_first_line_img, fullbg_second_line_img = Corp(fullbg, fullbg_position)

            bg_image = put_imgs_together(bg_first_line_img, bg_second_line_img, 'D:\\bg.jpg')
            fullbg_image = put_imgs_together(fullbg_first_line_img, fullbg_second_line_img, 'D:\\fullbg.jpg')

            distance = get_distance(bg_image, fullbg_image)
            # print(distance)

            trace = get_trace(distance - 10)
            move_to_gap(browser, trace)            

            time.sleep(5)
            retry -= 1
        
        print(browser.find_element_by_id('smsCodeBtnPopup').text)
    except:
        print('error:')
    finally:
        browser.quit()


if __name__ == '__main__':
    # chrome()
    for i in range(100):
        chrome()
        time.sleep(60)

    # verifyCode('http://127.0.0.1:1080')
    
    # for i in range(15):
    #     print(i)
    #     verifyCode('http://127.0.0.1:1080')
    #     time.sleep(90)