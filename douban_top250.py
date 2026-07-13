from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time
import random


# =========================
# 1. 安全获取文本的函数
# =========================
def safe_get_text(driver, by, value, default=""):
    """
    尝试获取某个元素的文本。
    如果元素不存在，就返回默认值，避免程序报错中断。
    """
    try:
        return driver.find_element(by, value).text.strip()
    except Exception:
        return default


# =========================
# 2. 初始化浏览器
# =========================
chrome_options = Options()

# 调试阶段建议不要开启无头模式，方便看到浏览器操作过程
# chrome_options.add_argument("--headless=new")

chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 15)


# =========================
# 3. 准备保存数据的列表
# =========================
result_list = []


# =========================
# 4. 打开豆瓣 Top250 首页
# =========================
start_url = "https://movie.douban.com/top250"
driver.get(start_url)


# =========================
# 5. 遍历 10 页
# =========================
for page in range(10):
    print(f"正在爬取第 {page + 1} 页...")

    # 等待当前页面的电影条目加载出来
    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".grid_view .item"))
    )

    # 找到当前页所有电影条目
    movie_items = driver.find_elements(By.CSS_SELECTOR, ".grid_view .item")

    # 当前页的电影链接列表
    movie_link_list = []

    # =========================
    # 6. 先在列表页提取每部电影的基础信息
    # =========================
    for item in movie_items:
        try:
            rank = item.find_element(By.CSS_SELECTOR, ".pic em").text.strip()
            title = item.find_element(By.CSS_SELECTOR, ".hd .title").text.strip()
            link = item.find_element(By.CSS_SELECTOR, ".hd a").get_attribute("href")

            try:
                quote = item.find_element(By.CSS_SELECTOR, ".quote .inq").text.strip()
            except Exception:
                quote = ""

            movie_link_list.append({
                "rank": rank,
                "list_title": title,
                "link": link,
                "quote": quote
            })

        except Exception as e:
            print("列表页某个电影条目解析失败：", e)

    # =========================
    # 7. 逐个打开详情页，爬取详情信息
    # =========================
    for movie in movie_link_list:
        data_dict = {
            "排名": movie["rank"],
            "列表页标题": movie["list_title"],
            "标题": "",
            "评分": "",
            "评价人数": "",
            "导演": "",
            "编剧": "",
            "主演": "",
            "类型": "",
            "制片国家/地区": "",
            "语言": "",
            "上映日期": "",
            "片长": "",
            "又名": "",
            "IMDb": "",
            "简介": "",
            "热门短评": "",
            "一句话短评": movie["quote"],
            "详情页链接": movie["link"]
        }

        try:
            print(f"正在进入详情页：{movie['rank']} - {movie['list_title']}")

            # 打开一个新的标签页
            driver.execute_script("window.open(arguments[0]);", movie["link"])

            # 切换到最新打开的标签页
            driver.switch_to.window(driver.window_handles[-1])

            # 等待详情页标题加载出来
            wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            # 随机等待，降低访问频率
            time.sleep(random.uniform(1, 2))

            # 获取电影标题
            data_dict["标题"] = safe_get_text(
                driver,
                By.CSS_SELECTOR,
                'span[property="v:itemreviewed"]'
            )

            if not data_dict["标题"]:
                data_dict["标题"] = safe_get_text(driver, By.TAG_NAME, "h1")

            # 获取评分
            data_dict["评分"] = safe_get_text(
                driver,
                By.CSS_SELECTOR,
                ".rating_num"
            )

            # 获取评价人数
            data_dict["评价人数"] = safe_get_text(
                driver,
                By.CSS_SELECTOR,
                'span[property="v:votes"]'
            )

            # 获取详情信息区
            info_text = safe_get_text(driver, By.ID, "info")

            # 获取简介
            summary = safe_get_text(
                driver,
                By.CSS_SELECTOR,
                'span[property="v:summary"]'
            )
            data_dict["简介"] = " ".join(summary.split())

            # 获取热门短评
            data_dict["热门短评"] = safe_get_text(
                driver,
                By.CSS_SELECTOR,
                ".short"
            )

            # 解析详情信息
            for line in info_text.split("\n"):
                line = line.strip()

                if line.startswith("导演:"):
                    data_dict["导演"] = line.replace("导演:", "").strip()

                elif line.startswith("编剧:"):
                    data_dict["编剧"] = line.replace("编剧:", "").strip()

                elif line.startswith("主演:"):
                    data_dict["主演"] = line.replace("主演:", "").strip()

                elif line.startswith("类型:"):
                    data_dict["类型"] = line.replace("类型:", "").strip()

                elif line.startswith("制片国家/地区:"):
                    data_dict["制片国家/地区"] = line.replace("制片国家/地区:", "").strip()

                elif line.startswith("语言:"):
                    data_dict["语言"] = line.replace("语言:", "").strip()

                elif line.startswith("上映日期:"):
                    data_dict["上映日期"] = line.replace("上映日期:", "").strip()

                elif line.startswith("片长:"):
                    data_dict["片长"] = line.replace("片长:", "").strip()

                elif line.startswith("又名:"):
                    data_dict["又名"] = line.replace("又名:", "").strip()

                elif line.startswith("IMDb:"):
                    data_dict["IMDb"] = line.replace("IMDb:", "").strip()

            # 把一部电影的数据保存到结果列表中
            result_list.append(data_dict)

            print(f"已完成：{data_dict['排名']} - {data_dict['标题']}")

        except Exception as e:
            print(f"详情页爬取失败：{movie['link']}")
            print("错误原因：", e)

        finally:
            # 关闭详情页标签
            if len(driver.window_handles) > 1:
                driver.close()

                # 切回列表页标签
                driver.switch_to.window(driver.window_handles[0])

            # 每爬完一部电影，随机等待
            time.sleep(random.uniform(1, 3))

    # =========================
    # 8. 点击下一页
    # =========================
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".paginator .next a")
        next_button.click()
        time.sleep(random.uniform(2, 4))

    except Exception:
        print("没有下一页了，爬取结束。")
        break


# =========================
# 9. 保存为 Excel
# =========================
df = pd.DataFrame(result_list)

df.to_excel("douban_top250.xlsx", index=False)

print("爬取完成！")
print(f"共爬取 {len(result_list)} 条电影信息。")
print("数据已保存到 douban_top250.xlsx")


# =========================
# 10. 关闭浏览器
# =========================
driver.quit()