# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
import datetime
from aliyunsdkcore import client
from aliyunsdkdds.request.v20151201 import DescribeBackupsRequest
from aliyunsdkdds.request.v20151201 import CreateBackupRequest


class MongodbApi(object):
    def __init__(self):
        self.access_key = ''
        self.access_secret = ''
        self.region = 'cn-shenzhen'
        self.DBInstanceId = ''
        self.NodeId = ['', '', '']

    def create_backup(self):
        clt = client.AcsClient(self.access_key, self.access_secret, self.region)
        request = CreateBackupRequest.CreateBackupRequest()
        request.set_accept_format('json')
        request.set_action_name('CreateBackup')
        request.set_DBInstanceId(self.DBInstanceId)

        response = clt.do_action_with_exception(request)
        print response

    def description_backup(self, start_time, end_time):
        link = []
        clt = client.AcsClient(self.access_key, self.access_secret, self.region)
        for node in self.NodeId:
            request = DescribeBackupsRequest.DescribeBackupsRequest()
            request.set_accept_format('json')
            request.add_query_param('DBInstanceId', self.DBInstanceId)
            request.add_query_param('StartTime', start_time)
            request.add_query_param('EndTime', end_time)
            request.add_query_param('NodeId', node)
            response = clt.do_action_with_exception(request)
            in_json = json.loads(response)
            for backup_info in in_json['Backups']['Backup']:
                link.append(backup_info['BackupDownloadURL'])
            return link, backup_info


def get_time():
    now_time = datetime.datetime.now()
    end_time = (now_time - datetime.timedelta(hours=8)).strftime('%Y-%m-%dT%H:%MZ')
    start_time = (now_time - datetime.timedelta(hours=12)).strftime('%Y-%m-%dT%H:%MZ')
    print(start_time, end_time)
    return start_time, end_time


def write_download_log(current_time, backinfo):
    backinfo_log = []
    backinfo_log.append({"备份开始时间：": "%s" % (backinfo['BackupStartTime'])})
    backinfo_log.append({"备份结束时间：": "%s" % (backinfo['BackupEndTime'])})
    backinfo_log.append({"下载地址：": "%s" % (backinfo['BackupDownloadURL'])})
    backinfo_log.append({"备份ID：": "%s" % (backinfo['BackupId'])})

    with open('log-%s.txt' % current_time, 'wb+') as f:
        for i in backinfo_log:
            for key in i:
                f.write(key)
                f.write(i[key])
                f.write("\n")


def download_backups(current_time, Link):
    print("正在下载......")
    start_time = datetime.datetime.now()
    file_name = "data_%s.tar.gz" % start_time.strftime("%Y%m%d")

    print("Downloading file:%s" % file_name)
    """以流的方式下载文件"""
    r = requests.get(Link, stream=True)

    # download started
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=6 * 1024):
            if chunk:
                f.write(chunk)

    print("%s downloaded!\n" % file_name)

    end_time = datetime.datetime.now()
    using_time = (end_time - start_time).seconds
    print("开始时间：%s，结束时间：%s,下载用时：%s 单位（s）" % (start_time, end_time, using_time))
    time_log = "开始时间：%s，结束时间：%s,下载用时：%s 单位（s）" % (start_time, end_time, using_time)

    with open('log-%s.txt' % current_time, 'a') as f:
        f.write(time_log)

    print("下载结束！")


URL_test = 'https://image.baidu.com/search/detail?ct=503316480&z=' \
           'undefined&tn=baiduimagedetail&ipn=' \
           'd&word=%E7%BE%8E%E5%A5%B3&step_word=&ie=utf-8&in=&cl=undefined&lm=' \
           'undefined&st=undefined&cs=3313054931,3702206715&os=1654817609,2977550961&simid=' \
           '4181469098,505377511&pn=13&rn=1&di=179319452400&ln=3980&fr=&fmq=1529075865205_R&fm=&ic=' \
           'undefined&s=undefined&se=&sme=&tab=0&width=undefined&height=undefined&face=undefined&is=0,' \
           '0&istype=0&ist=&jit=&bdtype=0&spn=0&pi=0&gsm=0&objurl=http%3A%2F%2Fdynamic-image.yesky.com%2F740x-' \
           '%2FuploadImages%2F2015%2F171%2F21%2F184VN2ZUW10T.jpg&rpstart=0&rpnum=0&adpicid=0'


if __name__ == '__main__':
    """在创建备份后一个小时执行，时差问题已经解决，查询时间为：当前时间的前两个小时"""
    """具体用法有待商榷，有些问题需要确认"""

    start_time, end_time = get_time()
    # MongodbApi().create_backup()
    Link, backup_info = MongodbApi().description_backup(start_time, end_time)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    write_download_log(current_time, backup_info)
    download_backups(current_time, URL_test)
    # os.system('cat xx.ar| mongorestore -h xxx --port xxx -u xxx -p xxx --drop --gzip --archive -vvvv --stopOnError')
