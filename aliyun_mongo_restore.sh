#!/bin/bash
#author:apple
#对mongos连接CPU性能 network性能 connection性能有影响

RESTORE=/alidata/mongodb/bin/mongorestore
BACK_DIR=/mnt/mongodbbak
DATE=`date +%F`
DB_USER=root
DB_PASS=111
log_file=$BACK_DIR/restore.log

echo `date +%F%H:%M:%S` > $log_file
$RESTORE -h s-wz98888adae78888.mongodb.rds.aliyuncs.com:3777 --authenticationDatabase=admin -u $DB_USER -p $DB_PASS -d scbd --drop --gzip --dir=$BACK_DIR/$DATE/scbd/ &>> $log_file
