#!/bin/bash
#author:apple

log_file=/alidata/backuplog.err
a=`echo 'db.serverStatus().repl' | mongo 127.0.0.1:40000/admin | grep "secondary" | grep true &> /dev/null; echo $?`
echo `date +%F%H:%M:%S` > $log_file

if [ a -eq 0 ]
then
	
	if /alidata/mongodb/bin/mongod --config /alidata/mongodb/conf/mongodb40000.conf --shutdown &>> $log_file && rsync -auvzP /alidata/mongodb/data40000 /alidata/mongobackup/ &>> $log_file
	then
	    echo 'success!' >> $log_file
	else
	    echo 'faild!' >> $log_file
	fi
fi
/alidata/mongodb/bin/mongod --config /alidata/mongodb/conf/mongodb40000.conf &

0 1 * * * bash /alidata/mongobackup/mongo_backup.sh
