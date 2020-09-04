# coding=utf-8

# HTML 输出器

import pandas as pd
from Logger import get_log
import configparser
import datetime
import os
import openpyxl

logger = get_log()
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")


def export_excel(export):
    try:
        time = str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
        EXCEL_PATH = str(config.get("path", "excel_path"))
        filename = EXCEL_PATH+time+".xlsx"
        # 指定字段顺序
        order = ['URL', 'Website', 'Type', 'Title', 'Value']
        # 将字典列表转换为DataFrame
        pf = pd.DataFrame(list(export))
        pf = pf[order]
        if not os.path.exists(filename):
            writer = pd.ExcelWriter(filename, mode='w')
            # 替换空单元格
            pf.fillna(' ', inplace=True)
            # 输出
            pf.to_excel(writer, encoding='utf-8', index=False, sheet_name='d1')
            # 保存表格
            writer.save()
            writer.close()
            logger.info("Excel file " + filename + " created")

        else:
            writer = pd.ExcelWriter(filename, mode='a', engine='openpyxl')
            writer.book = openpyxl.load_workbook(filename)
            # 替换空单元格
            pf.fillna(' ', inplace=True)
            # 输出
            pf.to_excel(writer, encoding='utf-8', index=False, sheet_name='d2')
            # 保存表格
            writer.save()
            writer.close()
            logger.info("Excel file " + filename + " exists and news have been added")


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
                for Type, key, value, website in zip(data['type'].values(), data['summary'].keys(),
                                                     data['summary'].values(), data['website'].values()):
                    temp_dict = {'URL': data['url'], "Website": website, "Type": Type, "Title": key, "Value": value}
                    dict_list.append(temp_dict)
        except Exception as e:
            print(e)
        export_excel(dict_list)
