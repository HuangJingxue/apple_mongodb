## 基本信息

spock:PRIMARY>db.serverStatus()

{

"host" :"h6.corp.yongche.org", //主机名

"version" :"2.6.2", //mongodb版本

"process" :"mongod", //mongodb进程，主要有mongod和mongos(分片集群中)两种

"pid" : NumberLong(4205), //mongod的pid进程号，可用shell的pidof mongod命令验证

"uptime" : 173120, //mongod服务启动后到现在已经存活的秒数

"uptimeMillis" :NumberLong(173119573), / /mongod服务启动后到现在已经存活的毫秒数

"uptimeEstimate" : 172173, //mongod内部计算出来的存活秒数

"localTime" :ISODate("2014-12-31T06:41:01.029Z") //本地时间

 

 

## 锁信息

Mongodb有4种锁：r,R,w,W

R:表示全局读锁

W:全局写锁

r:某个数据库读锁

w：某个数据库写锁

 

spock:PRIMARY>db.serverStatus().locks

{

"." : {

"timeLockedMicros": {

"R" :NumberLong(2532219), //mongod启动后所有库持有全局读锁的总微秒数

"W" :NumberLong(2022505) // mongod启动后所有库持有全局写锁的总微秒数

},

"timeAcquiringMicros": {

"R" :NumberLong(1489378), // mongod启动后所有库全局读锁的锁等待的总微秒数

"W" :NumberLong(361350) // mongod启动后所有库全局写锁的锁等待的总微秒数

}

},

"admin" : {

"timeLockedMicros": {

"r" :NumberLong(277350), // mongod启动后admin数据库持有的读锁时间

"w" :NumberLong(0) // mongod启动后admin数据库持有的写锁时间

},

"timeAcquiringMicros": {

"r" :NumberLong(11011), // mongod启动后admin数据库的读锁的锁等待总时间

"w" :NumberLong(0) // mongod启动后admin数据库的读锁的锁等待总时间

}

},

"local" : {

"timeLockedMicros": {

"r" :NumberLong(29750564),

"w" :NumberLong(737)

},

"timeAcquiringMicros": {

"r" :NumberLong(4074456),

"w" :NumberLong(46)

}

},

"jiangjianjian" : {

"timeLockedMicros": {

"r" :NumberLong(935802), //mongod启动后jiangjianjian数据库持有的读锁时间

"w" :NumberLong(98) // mongod启动后jiangjianjian数据库持有的写锁时间

},

"timeAcquiringMicros": {

"r" :NumberLong(262185), // mongod启动后jiangjianjian数据库的读锁的锁等待总时间

"w" : NumberLong(9) // mongod启动后jiangjianjian数据库的写锁的锁等待总时间

}

},

"test" : {

"timeLockedMicros": {

"r" :NumberLong(719696),

"w" :NumberLong(141)

},

"timeAcquiringMicros": {

"r" :NumberLong(332797),

"w" :NumberLong(10)

}

}

}

 

## 全局锁信息

spock:PRIMARY>db.serverStatus().globalLock

{

"totalTime" :NumberLong("172059990000"), //mongod启动后到现在的总时间，单位微秒

"lockTime" :NumberLong(2031058), //mongod启动后全局锁锁住的总时间，单位微秒

"currentQueue" : {

"total" : 0, //当前的全局锁等待锁等待的个数

"readers" : 0, //当前的全局读锁等待个数

"writers" : 0 //当前全局写锁等待个数

},

"activeClients" : {

"total" : 0, //当前活跃客户端的个数

"readers" : 0, //当前活跃客户端中进行读操作的个数

"writers" : 0 //当前活跃客户端中进行写操作的个数

}

}

 

## 内存信息

bj1-farm1:PRIMARY>db.serverStatus().mem

{

"bits" : 64, //操作系统位数

"resident" : 45792, //物理内存消耗，单位M

"virtual" : 326338, //虚拟内存消耗

"supported" : true, //为true表示支持显示额外的内存信息

"mapped" : 161399, //映射内存

"mappedWithJournal" : 322798 //除了映射内存外还包括journal日志消耗的映射内存

}

关于mongodb内存的介绍可参考我的blog

https://blog.csdn.net/cug_jiang126com/article/details/42264895

 

连接数信息

bj1-farm1:PRIMARY>db.serverStatus().connections

{

"current" : 2581, //当前连接数

"available" : 48619, //可用连接数

"totalCreated" :NumberLong(187993238) //截止目前为止总共创建的连接数

}

可看到当前mongod的最大连接数即为51200=2581+48619

 

额外信息

bj1-farm1:PRIMARY>db.serverStatus().extra_info

{

"note" : "fields vary byplatform", //表示当前这个extra_info的显示信息依赖于底层系统

"heap_usage_bytes" :206033064, //堆内存空间占用的字节数，仅linux适用

"page_faults" : 11718117 //数据库访问数据时发现数据不在内存时的页面数量，当数据库性能很差或者数据量极大时，这个值会显著上升

}

 

索引统计信息

bj1-farm1:PRIMARY>db.serverStatus().indexCounters

{

"accesses" : 35369670951, //索引访问次数，值越大表示你的索引总体而言建得越好，如果值增长很慢，表示系统建的索引有问题

"hits" : 35369213426, //索引命中次数，值越大表示mogond越好地利用了索引

"misses" : 0, //表示mongod试图使用索引时发现其不在内存的次数，越小越好

"resets" : 0, //计数器重置的次数

"missRatio" : 0 //丢失率，即misses除以hits的值

}

 

 

后台刷新信息

bj1-farm1:PRIMARY>db.serverStatus().backgroundFlushing

{

"flushes" : 171675, //数据库刷新写操作到磁盘的总次数，会逐渐增长

"total_ms" : 432943335, //mongod写数据到磁盘消耗的总时间，单位ms，

"average_ms" :2521.8775884665793, //上述两值的比例，表示每次写磁盘的平均时间

"last_ms" : 5329, //当前最后一次写磁盘花去的时间，ms，结合上个平均值可观察到mongd总体写性能和当前写性能

"last_finished" :ISODate("2014-12-31T07:39:11.881Z") //最后一次写完成的时间

}

 

游标信息

bj1-farm1:PRIMARY>db.serverStatus().cursors

{

"note" : "deprecated,use server status metrics", //表示也可使用b.serverStatus().metrics.cursor命令看看

"clientCursors_size" : 2, //mongodb当前为客户端维护的游标个数

"totalOpen" : 2, //和clientCursors_size一样

"pinned" : 0, //打开的pinned类型的游标个数

"totalNoTimeout" : 0, //设置了经过一段不活跃时间以后不设置超时，即参数“ DBQuery.Option.noTimeout”值以后，打开的游标个数

"timedOut" : 11 //从mongod启动以来的游标超时个数，如果这个值很大或者一直在增长，可能显示当前应用程序有错误

}

 

网络信息

bj1-farm1:PRIMARY>db.serverStatus().network

{

"bytesIn" :NumberLong("1391919214603"), //数据库接收到的网络传输字节数，可通过该值观察是否到了预计的期望值

"bytesOut" :NumberLong("1669479449423"), //从数据库发送出去的网络传输字节数

"numRequests" : 5186060375 //mongod接收到的总的请求次数

}

 

副本集信息

bj1-farm1:PRIMARY>db.serverStatus().repl

{

"setName" :"bj1-farm1", //副本集名称

"setVersion" : 4, //当前版本，每修改一次配置会自增1

"ismaster" : true, //当前节点是否为master

"secondary" : false, //当前节点是否为slave

"hosts" : [ //副本集组成

"172.16.0.150:27017",

"172.16.0.152:27017",

"172.16.0.151:27017"

],

"primary" : "172.16.0.150:27017", //master所在的ip地址

"me" :"172.16.0.150:27017" //当前节点的ip地址

}

关于更多的副本集管理和介绍详见我的blog

https://blog.csdn.net/cug_jiang126com/article/details/41943237

 

副本集的操作计数器

bj1-farm1:PRIMARY>db.serverStatus().opcountersRepl

{

"insert" : 599, // mongod replication最近一次启动后的insert次数

"query" : 0,

"update" : 0,

"delete" : 0,

"getmore" : 0,

"command" : 0

}

 

 

操作计数器

bj1-farm1:PRIMARY>db.serverStatus().opcounters

{

"insert" : 17476744, //mongod最近一次启动后的insert次数

"query" : 4923585, // mongod最近一次启动后的query次数

"update" : 445136, // mongod最近一次启动后的update次数

"delete" : 301953, // mongod最近一次启动后的delete次数

"getmore" : 28737548, // mongod最近一次启动后的getmore次数,这个值可能会很高，因为子节点会发送getmore命令，作为数据复制操作的一部分

"command" : 32844821 //// mongod最近一次启动后的执行command命令的次数

}

 

Asserts

bj1-farm1:PRIMARY>db.serverStatus().asserts

{

"regular" : 65, //服务启动后正常的asserts错误个数,可通过log查看更多该信息

"warning" : 1, //服务启动后的warning个数

"msg" : 0, //服务启动后的message assert个数

"user" : 30655213, //服务启动后的user asserts个数

"rollovers" : 0 //服务启动后的重置次数

}

writeBacksQueued

bj1-farm1:PRIMARY>db.serverStatus().writeBacksQueued

false //如果为true表示有需要被重新执行的操作，如果为false表示没有

 

持久化(dur)

bj1-farm1:PRIMARY>db.serverStatus().dur

{

"commits" : 29, //上次分组提交间隔之后，写入journal的commit的次数

"journaledMB" : 1.089536, //上次分组提交间隔之后，写入journal的大小，单位M

"writeToDataFilesMB" :2.035345, //上次分组提交间隔之后，从journal写入到数据文件的大小

"compression" : 0.49237888647866956,//journal日志的压缩率

"commitsInWriteLock" : 0, //提交的时候有写锁的次数，可以用该值判断当前系统的写压力

"earlyCommits" : 0, //在分组提交间隔前，请求commit的次数。用这个值可以判断分组提交间隔，即 journal group commitinterval设置得是否合理

"timeMs" : {

"dt" : 3060, //收集数据所花的时间，单位ms

"prepLogBuffer" :7, //准备写入journal所花的时间，单位ms，该值越小表示journal性能越好

"writeToJournal" :36, //真正写入journal所花的时间，单位ms，该值和文件系统和硬件设备有关

"writeToDataFiles": 34, //从journal写入到数据文件所花的时间，单位ms

"remapPrivateView": 18 //重新映射内存所花的时间，单位ms，值越小表示journal性能越好

}

}

如果设置了分组提交间隔时间，该项还会在后面显示journalCommitIntervalMs信息，即提交间隔，默认100ms。

 

记录状态信息

bj1-farm1:PRIMARY>db.serverStatus().recordStats

{

"accessesNotInMemory" :4444249, //访问数据时发现不在内存的总次数

"pageFaultExceptionsThrown" :22198, //由于页面错误而抛出异常的总次数

"yc_driver" : {

"accessesNotInMemory": 53441,

"pageFaultExceptionsThrown": 18067

},

"yc_foot_print" : {

"accessesNotInMemory": 0,

"pageFaultExceptionsThrown": 0

}

 

工作集配置

bj1-farm1:PRIMARY>db.serverStatus( { workingSet: 1 } ).workingSet

{

"note" :"thisIsAnEstimate", //注释

"pagesInMemory" : 736105, //overseconds时间内在内存中的页的数量，默认页大小4k；如果你的数据集比内存还小，那么该值换算成大小就是数据集的大小；可以用该 值评估实际工作集的大小

"computationTimeMicros" : 232590, //收集working set数据所花的时间，单位微秒，收集这些信息会影响服务器性能，请注意收集working set的频率

"overSeconds" : 502 //内存中从最新数据变到最旧的数据页之间的所花的时间，单位秒。如果该值正在减少，或者值很小，表示working set已经远大于内存值；如 果该值很大，表示data set <=内存值

}

 

metrics

bj1-farm1:PRIMARY>db.serverStatus().metrics

{

"cursor" : { //游标的信息在上面已经介绍过

"timedOut" :NumberLong(12),

"open" : {

"noTimeout": NumberLong(0),

"pinned" :NumberLong(0),

"total" : NumberLong(2)

}

},

"document" : {

"deleted" :NumberLong(4944851), //删除记录的总条数

"inserted" :NumberLong(1066509660), //插入记录的总条数

"returned" :NumberLong("4594388182"), //返回记录的总条数

"updated" :NumberLong(27275088) //更新记录的总条数

},

"getLastError" : {

"wtime" : {

"num" : 0, //w>1的getlasterror次数

"totalMillis": 0 //时间

},

"wtimeouts" :NumberLong(0) //超时个数

},

这部分详细参考官方文档

https://docs.mongodb.org/manual/reference/command/getLastError/#dbcmd.getLastError

https://docs.mongodb.org/manual/reference/command/serverStatus/#metrics

 

"operation" : {

"fastmod" : NumberLong(23990485), //使用$inc操作增加数据记录，而且该列没有使用索引的update次数

"idhack" : NumberLong(0), //使用_id列进行查询的次数，这是mongodb会默认使用_id索引并且跳过查询计划解析

"scanAndOrder" :NumberLong(33042) //无法使用索引进行排序的次数

},

"queryExecutor" : {

"scanned" : NumberLong("334236661328319"),//查询或查询计划中扫描的总行数

"scannedObjects" :NumberLong("776725143947") //

},

"record" : {

"moves" :NumberLong(44166) //文档在硬盘上的移动总次数

},

"repl" : {

"apply" : {

"batches": {

"num": 162, //副本集中slave节点的oplog应用进程个数

"totalMillis": 14 //mongod从oplog中操作所花的总时间

},

"ops" :NumberLong(599) //oplog操作的总个数

},

"buffer" : {

"count" :NumberLong(0), //oplog buffer中的当前操作个数

"maxSizeBytes": 268435456, //oplog buffer的最大值，常量，不可再配置

"sizeBytes": NumberLong(0) //当前oplog buffer的大小

},

"network" : {

"bytes" :NumberLong(282864), //从复制源总读取的数据量总大小

"getmores": {

"num": 164, //执行getmores操作的个数

"totalMillis": 15595 //getmores操作所花的总时间

},

"ops" :NumberLong(599), //从复制源中读取的操作总次数

"readersCreated" : NumberLong(12) //oplog查询线程创建的个数，当发送connection，timeout，或者网络操作，重新选择复制源，该值都会增加

},

"preload" : {

"docs" : {

"num": 0,

"totalMillis": 0

},

"indexes": {

"num": 2396,

"totalMillis": 0

}

}

},

"storage" : {

"freelist" : {

"search" :{

"bucketExhausted": NumberLong(0),

"requests": NumberLong(1091000085),

"scanned": NumberLong(1139483866)

}

}

},

"ttl" : {

"deletedDocuments": NumberLong(1015082231), //使用了ttl索引的次数

"passes" :NumberLong(174032) //后天使用ttl索引删除文档的次数

}

}