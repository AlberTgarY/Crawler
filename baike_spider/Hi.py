import html_downloader
from bs4 import BeautifulSoup


# downloader = html_downloader.HtmlDownloader()
# html_cont = downloader.download("https://api.slack.com/events-api")
# soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
# news_content = soup.find_all('table', {'class': 'table table-bordered full_width'})
#
# tab = news_content[0]
# dictList = []
# for tr in tab.findAll('tr'):
#     list = [('name', ""), ('description', ""), ('scope', "")]
#     count = 0
#     for td in tr.findAll('td'):
#         if count == 0:
#             list[0] = ('name', td.getText())
#         elif count == 1:
#             list[1] = ('description', td.getText())
#         else:
#             list[2] = ('scope', td.getText())
#         count = count + 1
#     dic = dict(list)
#     dictList.append(dic)
downloader = html_downloader.HtmlDownloader()
html_cont = downloader.download("https://api.slack.com/methods")
soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
news_content = soup.find_all('div', {'class': 'tab_pane selected'})

tab = news_content[0]
dictList = []
for tr in tab.findAll('tr'):
    list = [('name', ""), ('description', "")]
    count = 0
    for td in tr.findAll('a',href = True):
        print(td['href'])

    #     if count == 0:
    #         list[0] = ('name', td.getText())
    #     elif count == 1:
    #         list[1] = ('description', td.getText())
    #     count = count + 1
    # dic = dict(list)
    # dictList.append(dic)
print()
print(dictList)
