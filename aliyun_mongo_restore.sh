#!/bin/bash
#author:apple
#对mongos连接CPU性能 network性能 connection性能有影响

RESTORE=/alidata/mongodb/bin/mongorestore
BACK_DIR=/mnt/mongodbbak
DATE=`date +%F`
DB_USER=root
DB_PASS=aaaaaaaaaaa
log_file=$BACK_DIR/restore.log


echo `date +%F%H:%M:%S` > $log_file
$RESTORE -h s-wz971034.mongodb.rds.aliyuncs.com:3717 --authenticationDatabase=admin -u $DB_USER -p $DB_PASS -d scbd --drop --gzip --dir=$BACK_DIR/$DATE/scbd/ &>> $log_file

cat > afile << ENDF
db.runCommand( { enablesharding : "scbd" } )
db.runCommand( { shardcollection : "scbd.AccessToken",key : { "userId" : 1, "_id" : 1} } )
db.runCommand( { shardcollection : "scbd.attendanceRegister",key : { "employeeId" : 1, "day" : 1} } )
db.runCommand( { shardcollection : "scbd.driverOrder",key : { "_id" : 1} } )
db.runCommand( { shardcollection : "scbd.employeeVisitlog",key : { "_id" : 1} } )
db.runCommand( { shardcollection : "scbd.flow",key : { "typeId" : 1, "_id" : 1} } )
db.runCommand( { shardcollection : "scbd.goodsCirculationLog",key : { "employeeId" : 1, "_id" : 1} } )
ENDF


while read line
do
    echo $line | mongo s-wz971034.mongodb.rds.aliyuncs.com:3717/admin  --authenticationDatabase admin -u $DB_USER  -p $DB_PASS
    #echo $line
done < afile
