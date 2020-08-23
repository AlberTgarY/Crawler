import html_downloader
from bs4 import BeautifulSoup
import pandas as pd

def export_excel_slack(export):
    try:
        # 将字典列表转换为DataFrame
        pf = pd.DataFrame(list(export))
        # 指定字段顺序
        order = ['name', 'description', 'scope']
        pf = pf[order]

        file_path = pd.ExcelWriter('slackname.xlsx')
        # 替换空单元格
        pf.fillna(' ', inplace=True)
        # 输出
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 保存表格
        file_path.save()
    except Exception as e:
        print(e)


def export_excel(export):
    try:
        # 将字典列表转换为DataFrame
        pf = pd.DataFrame(list(export))
        # 指定字段顺序
        order = ['name', 'bot_scope', 'scope']
        pf = pf[order]

        file_path = pd.ExcelWriter('name.xlsx')
        # 替换空单元格
        pf.fillna(' ', inplace=True)
        # 输出
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 保存表格
        file_path.save()
    except Exception as e:
        print(e)

def down(url):
    downloader = html_downloader.HtmlDownloader()
    html = downloader.download(url)
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    news_content = soup.find_all('a', {'class': 'token_type_'})
    return news_content

def down_bot(url):
    downloader = html_downloader.HtmlDownloader()
    html = downloader.download(url)
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    news_content = soup.find_all('a', {'class': 'token_type_granular_bot'})
    return news_content

def slackapi():
    downloader = html_downloader.HtmlDownloader()
    html_cont = downloader.download("https://api.slack.com/events-api")
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    news_content = soup.find_all('table', {'class': 'table table-bordered full_width'})

    tab = news_content[0]
    dictList = []
    for tr in tab.findAll('tr'):
        List = [('name', ""), ('description', ""), ('scope', "")]
        count = 0
        for td in tr.findAll('td'):
            if count == 0:
                List[0] = ('name', td.getText())
            elif count == 1:
                List[1] = ('description', td.getText())
            else:
                List[2] = ('scope', td.getText())
            count = count + 1
        if List != [('name', ""), ('description', ""), ('scope', "")]:
            dic = dict(List)
            print(dic)
            dictList.append(dic)
    export_excel_slack(dictList)

def api():
    downloader = html_downloader.HtmlDownloader()
    html_cont = downloader.download("https://api.slack.com/methods")
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    news_content = soup.find_all('div', {'class': 'tab_pane selected'})

    tab = news_content[0]
    dictList = []
    for tr in tab.findAll('tr'):
        List = [('name', ""), ('bot_scope', ""), ('scope', "")]
        count = 0
        for td in tr.findAll('a', href = True):
            List[0] = ('name', td.getText())
            url = "https://api.slack.com"+td['href']
            bot_scope = []
            scope = []
            if down_bot(url):
                for a in down_bot(url):
                    bot_scope.append(a.getText())
            if down(url):
                for a in down(url):
                    scope.append(a.getText())
            List[1] = ('bot_scope', bot_scope)
            List[2] = ('scope', scope)
        if List != [('name', ""), ('bot_scope', ""), ('scope', "")]:
            dic = dict(List)
            print(dic)
            dictList.append(dic)
    export_excel(dictList)

# if __name__ == "__main__":
    # slackapi()
