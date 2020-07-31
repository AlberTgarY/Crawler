# coding=utf-8

# HTML 输出器

import pandas as pd


def export_excel(export):
    try:
        # 将字典列表转换为DataFrame
        pf = pd.DataFrame(list(export))
        # 指定字段顺序
        order = ['URL', 'Website', 'Title', 'Value']
        pf = pf[order]

        file_path = pd.ExcelWriter('name.xlsx')
        # 替换空单元格
        pf.fillna(' ', inplace=True)
        # 输出
        pf.to_excel(file_path, encoding='GB2312', index=False)
        # 保存表格
        file_path.save()
    except Exception as e:
        print(e)


class HtmlOutputer(object):

    # 初始化数据集为空
    def __init__(self):

        self.datas = []

    # 收集数据用来最后输出
    def collect_data(self, data):

        if data is None:
            return
        self.datas.append(data)

    # 按照 excel 格式输出
    def output_excel(self):
        dict_list = []
        # construct the dict to a certain format
        try:
            for data in self.datas:
                for key, value, website in zip(data['summary'].keys(), data['summary'].values(), data['website'].values()):
                    temp_dict = {'URL': data['url'], "Website": website, "Title": key, "Value": value}
                    dict_list.append(temp_dict)
        except Exception as e:
            print(e)
        print(dict_list)
        export_excel(dict_list)