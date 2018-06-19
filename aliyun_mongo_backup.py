# -*- coding:utf-8 -*-

# author : kefatong
# __version__ : 1.2.1

import requests
import json
import time
import datetime
import urllib
import os
import multiprocessing

import logging
import config

from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeRegionsRequest, \
    DescribeDBInstanceAttributeRequest, CreateBackupRequest, DescribeDatabasesRequest
from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest



# backup_start_time = datetime.datetime.now()
# backup_end_time = backup_start_time + datetime.timedelta(1)
# StartTime = backup_start_time.strftime('%Y-%m-%dT%H:00Z')
# EndTime = backup_end_time.strftime('%Y-%m-%dT00:00Z')


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='backup.log',
                filemode='a+')


class RdsAPI:
    def __init__(self, access_key, access_secret, region):
        self.clt = client.AcsClient(str(access_key), str(access_secret), str(region))

    def get_DescribeRegions(self):
        '获取所有region'
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeRegions')
        return self.clt.do_action(request)

    def get_DescribeDBInstances(self):
        '获取某地域所有RDS'
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeDBInstances')
        return self.clt.do_action_with_exception(request)

    def get_DescribeDBInstanceAttribute(self, DBInstanceId):
        '获取RDS基本属性'
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeDBInstanceAttribute')
        request.set_DBInstanceId(str(DBInstanceId))
        return self.clt.do_action_with_exception(request)

    def create_CreateBackup(self, DBInstanceId, BackupMethod, DBName=None):
        print DBInstanceId, BackupMethod
        '创建备份'
        request = CreateBackupRequest.CreateBackupRequest()
        request.set_accept_format('json')
        request.set_action_name('CreateBackup')
        request.set_BackupMethod(BackupMethod)
        request.set_BackupType('FullBackup')
        if DBName:
            request.set_DBName(DBName)
        request.set_DBInstanceId(str(DBInstanceId))
        return self.clt.do_action_with_exception(request)

    def get_DescribeDatabases(self, DBInstanceId):
        '获取数据库名'
        request = DescribeDatabasesRequest.DescribeDatabasesRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeDatabases')
        request.set_DBInstanceId(str(DBInstanceId))
        return self.clt.do_action_with_exception(request)

    def get_DescribeBackups(self, DBInstanceId, StartTime, EndTime):
        request = DescribeBackupsRequest.DescribeBackupsRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeBackups')
        request.set_StartTime(StartTime)
        request.set_EndTime(EndTime)
        request.set_DBInstanceId(str(DBInstanceId))
        return self.clt.do_action_with_exception(request)


class RDS():
    def __init__(self, backupInstances=config.backup_instances):
        self.api = RdsAPI(config.access_key, config.access_secret, 'cn-hangzhou')

        self.backupInstances = backupInstances
        if not backupInstances:
            self.backupInstances = self.get_backup_instances()

        self.__StartTime = datetime.datetime.now()
        self.StartTime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
        self.EndTime = (datetime.datetime.utcnow() + datetime.timedelta(1)).strftime('%Y-%m-%dT00:00Z')

        self._success = []
        self._errors = []
        # self._working = []

    def get_regions(self):
        '获取有rds实例区域'
        # print api.get_DescribeDBInstances()
        result = json.loads(self.api.get_DescribeRegions())
        regions = result['Regions']['RDSRegion']

        r = set({})
        for region in regions:
            r.add(region['RegionId'])
        return r

    def get_backup_instances(self):
        '如果用户未定义backup_instances, 默认获取所有实例进行备份'

        if self.backupInstances:
            return self.backupInstances

        regions = self.get_regions()
        backupInstances = []

        for region in regions:
            api = RdsAPI(config.access_key, config.access_secret, region)
            result = json.loads(api.get_DescribeDBInstances())
            if not result['Items']['DBInstance']:
                continue

            # print result['Items']['DBInstance']
            for instance in result['Items']['DBInstance']:
                backupInstances.append({
                    'DBInstanceId': instance['DBInstanceId'],
                    'Engine': instance['Engine'],
                    'BackupMethod': 'Logical' if instance['Engine'] != 'SQLServer' else 'Physical',
                    'BackupDatabases': []
                })

        return backupInstances

    def create_backups(self):
        '创建备份'
        for instance in self.backupInstances:
            if instance['BackupDatabases']:
                logging.info(u'创建实例备份: {0} {1}'.format(instance['DBInstanceId'], instance['BackupDatabases']))
                print self.api.create_CreateBackup(instance['DBInstanceId'], instance['BackupMethod'],
                                                   instance['BackupDatabases'])
            else:
                logging.info(u'创建实例备份: {0}'.format(instance['DBInstanceId']))
                print self.api.create_CreateBackup(instance['DBInstanceId'], instance['BackupMethod'])

    def get_downloads(self):
        '获取可以下载的任务'
        downloads = []
        for instance in self.backupInstances:
            data = json.loads(self.api.get_DescribeBackups(instance['DBInstanceId'], self.StartTime, self.EndTime))['Items'][
                'Backup']
            if not data:
                continue
            downloads.extend(data)
        return downloads

    def do_download(self, instance):

        DBName = None
        for ins in self.backupInstances:
            if ins['DBInstanceId'] == instance['DBInstanceId']:
                if ins['BackupDatabases']:
                    DBName = ins['BackupDatabases']
        download_url = instance['BackupDownloadURL']

        _format = '{0}_{1}'.format(instance['DBInstanceId'], self.__StartTime.strftime('%Y%m%d%H%M'))
        if DBName:
            _format = '{0}_{1}_{2}'.format(instance['DBInstanceId'], DBName, self.__StartTime.strftime('%Y%m%d%H%M'))
            print _format
        logging.info(u'开始下载', instance['DBInstanceId'])
        print u'开始下载', instance['DBInstanceId']

        def Schedule(a, b, c):
            '''''
            a:已经下载的数据块
            b:数据块的大小
            c:远程文件的大小
           '''
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print '%.2f%%' % per

        try:
            local = os.path.join(config.backup_dir, _format)
            urllib.urlretrieve(download_url, local, Schedule)
            self._success.append(instance['DBInstanceId'])
            logging.info(u'%s 已经下载完成' % instance['DBInstanceId'])
        except:
            self._errors.append(instance['DBInstanceId'])
            logging.error(u'%s 已经下载失败' % instance['DBInstanceId'])



    def run(self):
        self.create_backups()  #执行备份任务
        Running = True
        while Running:
            instances = self.get_downloads()
            print '等待中.'
            if not instances:
                time.sleep(10)
                continue
            for instance in instances:
                print instance
                # 如果不在下载队列， 开始下载
                if instance['DBInstanceId'] not in self._success and instance['DBInstanceId'] not in self._errors:
                    self.do_download(instance)

                else:
                    if instance['DBInstanceId'] in self._errors:
                        print u'%s 已经下载失败' % instance['DBInstanceId']
                    else:
                        print u'%s 已经下载完成' % instance['DBInstanceId']

            if len(self._success) + len(self._errors) == len(self.backupInstances):
                Running = False
                print u'下载完成.'
                logging.info(u'下载完成')
            else:
                print u'剩余任务', (len(self.backupInstances) - len(self._success) - len(self._errors))
                logging.info(u'剩余任务')

            time.sleep(10)

        for instance in self.get_downloads():
            if instance['DBInstanceId'] in self._errors:
                print u'失败任务重新下载', instance['DBInstanceId']
                logging.info(u'失败任务重新下载', instance['DBInstanceId'])
                self.do_download(instance)
        else:
            logging.info(u'无失败任务， 所有任务已全部完成.')
            print u'无失败任务， 所有任务已全部完成.'



    def clean(self):
        print u'开始文件清理中。。。'
        f = list(os.listdir(config.backup_dir))
        for i in range(len(f)):
            # print f[i]
            filedate = os.path.getmtime(config.backup_dir + f[i])
            time1 = datetime.datetime.fromtimestamp(filedate).strftime('%Y-%m-%d')
            date1 = time.time()
            num1 = (date1 - filedate)/60/60/24
            expiredfile = 0
            fail = 0
            if num1 >=config.clear:
                expiredfile +=1
                try:
                    os.remove(config.backup_dir + f[i])
                    print (u"已删除文件：%s ： %s" %  (time1, f[i]))
                except Exception as e:
                    fail+=1
                    print (e)
                    print (u"删除失败：%s ： %s" %(time1, f[i]))

        print (u'过期文件已清理完毕：')
        print (u'共找到过期文件%s个，清理成功%s个：\n') %(str(expiredfile),str(expiredfile-fail))


if __name__ == '__main__':
    r = RDS()
    r.run()
    r.clean()
