import sys
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import jieba
import wordcloud
from imageio.v2 import imread

# 选择统计的小说类型（加了细分类，上千本书）
# 流程：
# get_whole_info.py
# name_1_15.txt
# intro_1_15.txt
# use_jieba.py
# count.txt
# wordcloud_make.py
# the_cloud_name_1_15.png
# the_cloud_intro_1_15.png


# 后面的排序依据
def get_num(elem):
    return elem[1]


def get_tail(url_n):
    # 大分类标签
    kind = ['', 'chanId80', 'chanId81', 'chanId82', 'chanId83', 'chanId84', 'chanId85', 'chanId30083', 'chanId86',
            'chanId88', 'chanId87', 'chanId30120', '', 'chanId21', 'chanId1', 'chanId2', 'chanId22', 'chanId4',
            'chanId15', 'chanId6', 'chanId5', 'chanId7', 'chanId8', 'chanId9', 'chanId20109', 'chanId10', 'chanId12',
            'chanId20076']
    # 小分类标签
    detail = [(), ('-subCateId801-', '-subCateId802-', '-subCateId803-', '-subCateId804-', '-subCateId805-',
                   '-subCateId806-', '-subCateId30094-', '-subCateId30095-', '-subCateId30096-', '-subCateId30097-'),
              ('-subCateId810-', '-subCateId811-', '-subCateId812-', '-subCateId813-', '-subCateId30093-'),
              ('-subCateId821-', '-subCateId822-', '-subCateId823-', '-subCateId824-', '-subCateId825-',
               '-subCateId827-', '-subCateId828-', '-subCateId829-', '-subCateId30098-'),
              ('-subCateId831-', '-subCateId832-', '-subCateId833-', '-subCateId834-'),
              ('-subCateId841-', '-subCateId844-', '-subCateId846-', '-subCateId847-', '-subCateId848-',
               '-subCateId849-', '-subCateId30092-'),
              ('-subCateId850-', '-subCateId851-', '-subCateId852-', '-subCateId853-', '-subCateId854-',
               '-subCateId30099-'), (),
              ('-subCateId862-', '-subCateId863-', '-subCateId864-', '-subCateId866-', '-subCateId867-',
               '-subCateId868-', '-subCateId869-'),
              ('-subCateId880-', '-subCateId881-', '-subCateId882-', '-subCateId883-'),
              ('-subCateId30100-', '-subCateId30101-', '-subCateId30102-', '-subCateId30103-', '-subCateId30104-',
               '-subCateId30105-', '-subCateId30106-', '-subCateId30107-', '-subCateId30108-'),
              ('-subCateId30121-', '-subCateId30122-', '-subCateId30123-', '-subCateId30124-'), (),
              ('-subCateId8-', '-subCateId58-', '-subCateId73-', '-subCateId78-'),
              ('-subCateId38-', '-subCateId62-', '-subCateId201-', '-subCateId202-', '-subCateId20092-',
               '-subCateId20093-'),
              ('-subCateId5-', '-subCateId30-', '-subCateId206-', '-subCateId20099-', '-subCateId20100-'),
              ('-subCateId18-', '-subCateId44-', '-subCateId64-', '-subCateId207-', '-subCateId20101-'),
              ('-subCateId12-', '-subCateId16-', '-subCateId74-', '-subCateId130-', '-subCateId151-', '-subCateId153-'),
              ('-subCateId6-', '-subCateId209-', '-subCateId20104-', '-subCateId20105-', '-subCateId20106-',
               '-subCateId20108-'),
              ('-subCateId54-', '-subCateId65-', '-subCateId80-', '-subCateId230-', '-subCateId231-'),
              ('-subCateId22-', '-subCateId32-', '-subCateId48-', '-subCateId220-', '-subCateId222-', '-subCateId223-',
               '-subCateId224-', '-subCateId225-', '-subCateId226-', '-subCateId20094-'),
              ('-subCateId7-', '-subCateId70-', '-subCateId240-', '-subCateId20102-', '-subCateId20103-'),
              ('-subCateId28-', '-subCateId55-', '-subCateId82-'),
              ('-subCateId21-', '-subCateId25-', '-subCateId68-', '-subCateId250-', '-subCateId251-', '-subCateId2052-',
               '-subCateId253-'),
              ('-subCateId20110-', '-subCateId20111-', '-subCateId20112-'),
              ('-subCateId26-', '-subCateId35-', '-subCateId57-', '-subCateId260-', '-subCateId20095-'),
              ('-subCateId60-', '-subCateId66-', '-subCateId281-', '-subCateId282-'),
              ('-subCateId20079-', '-subCateId20096-','-subCateId20075-', '-subCateId20077-', '-subCateId20078-',
               '-subCateId20097-', '-subCateId20098-'),
              ]
    """"""
    # 男女的大标签不一样
    s = int(input("请选择性别倾向：\n0.女生  1.男生\n"))
    if s == 0:
        k = int(input("请选择小说类型：\n0.全部  1.古代言情  2.仙侠奇缘  3.现代言情\n4.浪漫青春  5.玄幻言情  6.悬疑推理  7.短篇"
                      "\n8.科幻空间  9.游戏竞技  10.轻小说  11.现实生活\n"))
    else:
        k = int(input("请选择小说类型：\n0.全部  1.玄幻  2.奇幻  3.武侠\n4.仙侠  5.都市  6.现实  7.军事\n8.历史  9.游戏  10.体育  11.科幻"
                      "\n12.诸天无限  13.悬疑  14.轻小说  15.短篇\n"))
    if len(detail[k + 12 * s]) == 0:
        tail = [url_n + kind[k + 12 * s]]
    else:
        tail = [url_n + kind[k + 12 * s] + de for de in detail[k + 12 * s]]
    return tail


# 获取url
url0 = 'https://www.qidian.com/all/'
aft = get_tail(url0)
print(aft)

# 选择处理书名还是文案
n_or_i = int(input("请选择要分析的信息：0.书名  1.文案"))

# 付费和更新状态后缀
state = ['action0-vip0', 'action0-vip1', 'action1-vip0', 'action1-vip1']
# 当前页面后缀
page = ['/', '-page2/', '-page3/', '-page4/', '-page5/']
print("\n请等待\n")

# 获取网页源代码
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}

# 4个细分网页，每个网页最多5个页面
for ur in aft:
    for sta in state:
        n = 0
        pg = 1
        # 每个页面有20本书
        for pa in page:
            url = ur + sta + pa
            request = urllib.request.Request(url, headers=headers)
            n = n + 1
            if n > pg:
                # 一个小分类有1~5面，0~100本书
                print("finish")
                break
            print(n)
            response = urllib.request.urlopen(request)
            # 因为一次访问28~140个网页，总是中断，这里输出url好判断程序运行的进度
            print(url)
            if response.status != 200:
                print("爬失败啦")
                continue
            # 获取源代码内容
            content = response.read().decode('utf-8')

            # 将网页源代码存入html文件
            fp = open('s_code.html', 'w', encoding='utf-8')
            fp.write(content)
            fp.close()

            # 提取信息
            soup = BeautifulSoup(open('s_code.html', encoding='utf-8'), 'lxml')

            # 提取当前小分类的页面数
            t_list = soup.find_all(class_="pagination fr")  # 页面数是class="pagination fr"的div标签的data-pagemax属性值
            for t in t_list:
                pg = int(t.get("data-pagemax"))

            if n_or_i == 0:
                # 提取当前页面的书名（0~20个）
                obj1 = soup.select('a[data-eid="qd_B58"]')  # 书名是data-eid="qd_B58"的a标签的值
                fn = open('name.txt', 'a', encoding='utf-8')
                for j in obj1:
                    fn.write(j.get_text() + '\n')
                fn.close()
            elif n_or_i == 1:
                # 提取当前页面的文案（0~20个）
                obj2 = soup.select('p[class="intro"]')  # 文案是class="intro"的p标签的值
                fw = open('intro.txt', 'a', encoding='utf-8')
                for j in obj2:
                    fw.write(j.get_text() + '\n')
                fw.close()
            else:
                print("选择错误！")
                sys.exit()

# 数据预处理
if n_or_i == 0:
    # 处理书名
    r = open('name.txt', 'r', encoding='utf-8').read()
else:
    # 处理文案
    r = open('intro.txt', 'r', encoding='utf-8').read()

# jieba分词多种方法
# names = jieba.cut(r, cut_all=True)
# names = jieba.cut_for_search(r)
# names = jieba.cut(r)
names = jieba.lcut(r)

# 创建初始字典，标点符号基本长度为1，在这里和"你", "我", "的", "是" 等不具有统计意义的单字一同被滤去，不出现在停用词文件
word_dict = {}
for i in names:
    if len(i) == 1:
        continue
    else:
        word_dict[i] = word_dict.get(i, 0) + 1

# 停用词剔除
stopwords = open('stopwords.txt', 'r', encoding='utf-8').read()
stopword = stopwords.split('\n')
for word in stopword:
    try:
        del word_dict[word]
    except:
        continue

# 字典->列表->排序
word_list = list(word_dict.items())
word_list.sort(key=get_num, reverse=True)

# 列表->词频文件
fc = open('count.txt', 'w', encoding='utf-8')
for i in range(len(word_list)):
    ke, v = word_list[i]
    fc.write('{:<8}{:>2}\n'.format(ke, v))
fc.close()

# 根据词频文件生成词云图
f = open('count.txt', 'r', encoding='utf-8').read()

# 白底，800*800，楷体，形状为云
w = wordcloud.WordCloud(background_color='white', width=800, height=800, font_path='C:\Windows\Fonts\simkai.ttf',
                        mask=imread('cloud.png'))
w.generate(f)

if n_or_i == 0:
    # 生成书名词云图
    w.to_file('the_cloud_name.png')
else:
    # 生成文案词云图
    w.to_file('the_cloud_intro_.png')

