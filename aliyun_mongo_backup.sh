#!/bin/bash
#author:apple
#用时45min


DUMP=/alidata/mongodb/bin/mongodump
BACK_DIR=/mnt/mongodbbak
DATE=`date +%F`
DB_USER=root
DB_PASS=1111
DAYS=3
log_file=$BACK_DIR/backup.log

echo `date +%F%H:%M:%S` > $log_file
$DUMP --host s-wz55555ac91f8555.mongodb.rds.aliyuncs.com:3777 --authenticationDatabase admin -u $DB_USER -p $DB_PASS -d scbd --gzip -o $BACK_DIR/$DATE &>> $log_file
find $DUMP -type d -mtime +$DAYS3 -execdir rm -rf {} \;
