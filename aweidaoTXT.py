from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time


def run(chuanNum, lastPage, queue=None):
    # Set up ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    # chuanNum = input("串号： ")
    # lastPage = input("总页数：")
    for i in range(1, int(lastPage)+1):
        url = f"https://aweidao1.com/t/{chuanNum}?page={i}"
        if queue:
            queue.put(f"正在获取第{i}页……")
        try:
            driver.get(url)
        except WebDriverException:
            error_msg = f"抱歉！第 {i}页加载不出来，请再试一次"
            if queue:
                queue.put(error_msg)
            else:
                print(error_msg)
            driver.quit()  # Close the browser before exiting
            return

        # Wait for the page to load completely
        timeout = 20  # Maximum time to wait for text to appear (in seconds)
        end_time = time.time() + timeout
        while time.time() < end_time:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Check if the desired text is present in the parsed content
            if "排序:正序查看:全部" in soup.text:
                break
            time.sleep(1)
        else:
            # This block will execute if the while loop completes without a break 
            error_msg = f"嗯……无法在 {timeout} 秒内找到有效内容，串号是不是写错了"
            if queue:
                queue.put(error_msg)
            else:
                print(error_msg)
            driver.quit()  # Close the browser before exiting
            return

        # Parse the page source with BeautifulSoup
        # soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all the text information on the page
        texts = soup.get_text()

        # Add a divider line before the character 'No.' whenever it appears in the text                                                                     
        texts = texts.replace('回复', '\n------------------\n').replace('Po','***Po***\n').replace('No.', '\nNo.').replace('(>д<)更多选项标题标题名称名称EmailEmail清空草稿保存草稿发送','').replace('- 阿苇岛You need to enable JavaScript to run this app.登录/注册','').replace('APP中打开','').replace('排序:正序查看:全部','').replace('主题模式[系统]时间线时间线水上芦苇综合欢乐恶搞围炉创意跑团故事(小说)询问怪谈游戏动画漫画购物科技料理(宠物)东方ProjectMinecraft社畜学业水下芦苇亚文化速报血肉竞技场(对线)军武芦苇丛(日记/树洞)兄弟姐妹测试管理城墙版务技术支持值班室博物馆综合版1游戏综合版创意(涂鸦)询问3都市怪谈(灵异)SE(FF14)姐妹1(淑女)围炉1主播(UP)手游暂定(规则怪谈)特摄Steam模型(手办)任天堂NS圆桌眼科(Cosplay)LOL脑洞(推理)声优暴雪游戏女装(时尚)占星(卜卦)New!喵版(主子)偶像买买买(剁手)DOTA&自走棋DNF料理(美食)虚拟偶像(LL)数码(装机)宠物技术(码农)微软(XBOX)New!美漫(小马)国漫科学(理学)索尼轻小说怪物猎人体育育儿摄影2军武彩虹六号舰娘VOCALOID电影/电视精灵宝可梦旅行New!日记(树洞)EVE(Old!)文学(推书)艺人音乐(推歌)战争游戏(WOT)战争雷霆卡牌桌游音乐游戏', '').replace('©2022-2023 CTMVer 0.5.7联系我们:help@aweidao.com免责声明：本站无法保证用户张贴内容的可靠性，投资有风险，健康问题请遵医嘱。','').replace('版规选择饼干','')

        # Append the obtained text to a file named text.txt. If the file does not exist, create it.                                                                            
        with open(f'{chuanNum}.txt', 'a', encoding='utf-8') as f:
            f.write(texts)    

    # Close the browser
    driver.quit()
    if queue:
        queue.put(f"串已可以在{chuanNum}.txt里享用！")