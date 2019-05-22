from datetime import datetime
from urllib import parse,request
from http import cookiejar
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import json
import re
import time

# python -m pip install selenium
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
        opener = request.build_opener(handler)

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

    log = open('E:\\crawler.log', 'a')
    log.write('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] : ' + json.dumps(json.loads(res)) + '\n')
    log.close()

def chrome():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--proxy-server=http://127.0.0.1:1080")

    browser = webdriver.Chrome(executable_path='E:\\github\\ml\\chromedriver.exe', chrome_options=chrome_options)
    browser.get('http://www.sai9769.com/index.htm')
    browser.maximize_window()

    browser.find_element_by_class_name('regBtn').click()
    browser.find_element_by_id('ir_phone').send_keys('18802074098')
    browser.quit()


if __name__ == '__main__':
    
    for i in range(15):
        print(i)
        verifyCode('http://127.0.0.1:1080')
        time.sleep(60)