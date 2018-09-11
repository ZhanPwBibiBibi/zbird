from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options


class Zbird:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_window_size(1200, 2400)
        self.diamonds = []

    def get_first_page(self):
        self.browser.get('http://www.zbird.com/diamond/')
        info_page = self.browser.page_source

        return info_page

    def next_page(self):
        try:
            close_tag = WebDriverWait(self.browser, 500).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.fix_yy > div > i"))
            )
            close_tag.click()
        except:
            pass

        d = WebDriverWait(self.browser, 500).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#resultArea > div.page_boder > a.page_boder_a_right"))
        )
        d.click()
        sleep(2)
        info_page = self.browser.page_source
        return info_page



    def find(self, html):
        h = html
        bsobj = BeautifulSoup(h, 'lxml')

        infos = bsobj.find_all('div', {'class': 'diamondList'})
        zhenshus = re.findall('证书</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        zuanzhongs = re.findall('钻重</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        yanses = re.findall('颜色</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        jindus = re.findall('净度</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        qiegongs = re.findall('切工</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        paoguangs = re.findall('抛光</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        duichengs = re.findall('对称</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        yingguangs = re.findall('荧光</font>[\s\t\n](.*?)</div>', str(infos), re.S)
        dianpus = re.findall(
            '荧光.*?diamondListGai2">(.*?)</div>.*?</div><div class="diamondResultListStone3">',
            str(infos), re.S)
        jiages = re.findall('￥</font><font style=".*?">(.*?)[\s\t\n]*</font>', str(infos), re.S)
        for zhenshu, zuanzhong, yanse, jindu, qiegong, paoguang, duicheng, yingguang, dianpu, jiage in zip(zhenshus,
                                                                                                           zuanzhongs,
                                                                                                           yanses,
                                                                                                           jindus,
                                                                                                           qiegongs,
                                                                                                           paoguangs,
                                                                                                           duichengs,
                                                                                                           yingguangs,
                                                                                                           dianpus,
                                                                                                           jiages):
            self.diamonds.append(
                [zhenshu, zuanzhong, yanse, jindu, qiegong, paoguang, duicheng, yingguang, dianpu, jiage])
            print(self.diamonds[-1])

    def start(self):
        print('正在抓取第 1 页')
        self.find(self.get_first_page())
        total_page = 364

        count = 2
        while count < total_page:
            print('正在抓取第 ' + str(count) + ' 页')
            self.find(self.next_page())
            count += 1

        self.__save_to_file(self.diamonds)

    def __save_to_file(self, content):
        with open('data.csv', 'wb') as f:
            for item in content:
                line = ','.join(item) + '\n'
                f.write(line.encode('utf-8'))

    def exit(self):
        self.browser.quit()
        exit()





if __name__ == '__main__':
    z = Zbird()
    z.start()
    z.exit()

