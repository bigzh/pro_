# _*_ coding:utf-8 _*_
# @Author   :Mr.Z
# @Version  :1.0.0
# @Time     :2019/2/26 15:10
# @Software :PyCharm
# @Des      :

import json
import pandas as pd
import os
import sys


def get_all_file_list(pro_dir, file_type=None):
    """获取项目目录下所有文件地址"""
    w_list = []
    if not pro_dir.endswith(os.path.sep):
        pro_dir += '/'

    files = os.listdir(pro_dir)

    for file in files:
        fi_path = os.path.join(pro_dir, file)
        if os.path.isdir(fi_path):
            w_li = get_all_file_list(fi_path, file_type)
            if len(w_li) > 0:
                w_list.extend(w_li)
        elif not file.startswith('~') and (not file_type or file.endswith(file_type)):
            w_list.append(pro_dir + file)

    return w_list


def excel_2_csv(excel_path, csv_path):
    excel = pd.read_excel(excel_path)
    excel.to_csv(csv_path, index=False, encoding='utf-8')


def json_check(json_str):
    try:
        json_str = json_str.replace('\n', '').replace('\t', '')
        json.loads(json_str)
    except Exception as e:
        # traceback.print_exc()
        return json_str
    else:
        # print('+'*50 + '\n' + json_str + '\n' + '-'*50)
        return ''


def check_file(file_path):
    # excel = pd.read_excel(file_path, usecols=[4])
    # vals = excel.values
    csv = pd.read_csv(file_path, encoding='utf-8', engine='python')
    vals = csv['OCR结果（标词槽和候选答案）']

    i = 0
    for ids, val in enumerate(vals):
        # print(val)
        s = json_check(val)
        if s:
            i += 1
            print('Type:', type(s))
            print(file_path + '：第' + str(ids) + '行json串有问题\n')
            print('+'*50 + '\n' + s + '\n' + '^'*50)

    return i


if __name__ == '__main__':
    check_dir = r'C:\Users\john\Desktop\docs'

    # file_paths = get_all_file_list(check_dir, ('xlsx', 'xls'))
    # for file_path in file_paths:
    #     ids = file_path.rindex('.')
    #     csv_path = file_path[:ids+1] + 'csv'
    #     print(file_path, ids, csv_path)
    #     excel_2_csv(file_path, csv_path)

    csv_paths = get_all_file_list(check_dir, 'csv')
    count = 0
    for csv_path in csv_paths:
        count += check_file(csv_path)
    print('共有'+ str(count) +'条数据有问题')
