import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re
import xlwt
import wordcloud
import jieba
from tqdm import tqdm

def main():
    baseUrl = "https://music.douban.com/subject/24859695/comments/?start=1"
    # 爬取网页
    dataList = getData(baseUrl)
    # 保存数据
    savePath = "僕が死のうと思ったのは 短评.xls"
    saveData(savePath, dataList)

    # saveDataToDb(dataList)

def getData(baseurl):
    datalist =[]
    judgelist=[]
    for i in range(0,5):
        url =baseurl + str(i*20)
        html = askURL(url)

        #解析数据
        soup = BeautifulSoup(html, "html.parser")
        # findcount = re.compile(r'<span id="" class="vote-count">(\d*)</span>')
        for j in range(1, 21):
            for item in soup.find_all("div", class_="comment-list new_score"):

                data = []  # 存放一首歌都有的短评
                judgedata = []
                item = str(item)

                try:
                    name = (re.findall(r'<a href="(.*?)">(.*)</a>', item)[j]) # 用户姓名
                    data.append(name[0])
                    data.append(name[1])
                    num = re.findall(r'<span class="(.*?)" title="(.*)"></span>',item)
                    x = (num[0])
                    data.append(x[1])
                    rateday = re.findall(r'<span class="comment-time">(\d{4}-\d{1,2}-\d{1,2})</span>', item)[j]  # 评价日期
                    data.append(rateday)
                    judge = re.findall(r'<span class="short">(.*?)</span>', item)[j]  # 评价
                    judgedata.append(judge)
                    data.append(judge)

                    # count = re.findall(findcount,item)[j]
                    # # count = re.findall(r'<span id="" class="vote-count">(\d*)</span>', item)  # 觉得有用的人数
                    # # print(type(count))
                    # data.append(count)
                    datalist.append(data)
                    judgelist.append(judgedata)
                except IndexError:
                    pass
#将评论列表数据写入到txt文件中
    for i in tqdm(judgelist):
        f = open('./a.txt','a',encoding='utf-8')
        f.write(str(i) + '\n')
        f.close()
        # f.write(judgelist)

    print(len(datalist))  #打印列表长度，检测爬取多少


    return datalist



def askURL(url):

    head = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 91.0.4472.124Safari / 537.36Edg / 91.0.864.70',
        'Host': 'music.douban.com',
        'sec-ch-ua': 'Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Upgrade-Insecure-Requests': 1,
        'Cookies': 'll="118259"; bid=xWmee1ivHF0; __utmz=30149280.1626659394.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=266659602.1626743589.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); viewed="24859695"; _vwo_uuid_v2=D8A33789F437A56DF7F34359DC5A93346|061df83e9621221ac9abe3f8c0d65815; douban-fav-remind=1; _ga=GA1.2.1079547870.1626621943; _gid=GA1.2.244380732.1626764803; __utma=266659602.491372755.1626743589.1626743589.1626764806.2; _pk_ref.100001.afe6=["","",1626849535,"https://www.douban.com/misc/sorry?original-url=https%3A%2F%2Fmusic.douban.com%2Fsubject%2F24859695%2Fcomments%2F%3Fstart%3D1"]; _pk_ses.100001.afe6=*; ap_v=0,6.0; __utmc=30149280; __utma=30149280.1079547870.1626621943.1626833021.1626849535.9; __utmt=1; dbcl2="242523978:186GmjEWy0w"; ck=dFax; push_noty_num=0; push_doumail_num=0; __utmv=30149280.24252; _pk_id.100001.afe6=cd872a519c9a8005.1626743573.6.1626849636.1626833020.; __utmb=30149280.7.10.1626849535'
    }

    req = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')

    except urllib.error.URLError as a:
        if hasattr(a, 'code'):
            print(a.code)
        if hasattr(a, 'reason'):
            print(a.reason)
    return html

def saveData(savePath, dataList):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet("僕が死のうと思ったのは 短评", cell_overwrite_ok=True)
    col = ("用户超链接", "用户名", "rating", "评价时间", "评价")
    for i in range(0, 5):
        worksheet.write(0, i, col[i])
    for i in range(0, 94):
        data = dataList[i]
        for j in range(0, 5):
            worksheet.write(i+1, j, data[j])
    workbook.save(savePath)

# def get_cut_words(conten_series):
#     stop_word = []
#
#     with open(r'./哈工大停用词表.txt','r',encoding='gb18030') as f:
#         lines = f.readlines()
#         for line in lines:
#             stop_word.append(line.strip())
#
#     my_word = ['中岛美嘉','一首歌']
#     for i in my_word:
#         jieba.add_word(i)
#
#
#     word_num = jieba.Lcut(conten_series.str.cat(sep='。'), cut_all=False)
#     word_num_selected = [i for i in word_num if i not in stop_word and len(i)>=2]
#     return word_num_selected
def wordAnalysis():
    f = open('./a.txt','r',encoding= 'utf-8')
    content = f.read()
    f.close()
    ls = jieba.lcut(content)
    txt = ' '.join(ls)
    w = wordcloud.WordCloud(font_path='./经典综艺体简.TTF', width=1000, height=700, background_color='white')
    w.generate(txt)
    w.to_file('评论.png')



if __name__ == '__main__':
    main()
    wordAnalysis()
