# 数据类型

- 类似JSON
- 6种数据类型
- 保留JSON基本键/值对特性基础上添加了一些数据类型

## 基础数据类型

- null

null用于表示控制或者不存在的字段：

```shell
{"x":null}
```

- 布尔型

布尔类型有两个：

```shell
{"x":true}
```

- 数值

shell默认使用64位浮点型数值。

```shell
{"x":3.14}
{"x":3}
```

对于整形值：

NumberInt类（表示4字节带符号整数）
NumberLong类（表示8字节带符号整数）

- 字符串

UTF-8字符串都可表示为字符串类型的数据：

{"x":"foobar"}

- 日期

日期被存储为自新纪元以来经过的毫秒数，不存储时区：

{"x":new Date()}

- 正则表达式

查询时，使用正则表达式作为限定条件，语法也与JavaScript的正则表达式语法相同：

{"x":/foobar/i}

- 数组

数据列表或数据集可以表示为数组：

{"x":["a","b","c"]}

- 内嵌文档

文档可嵌套其他文档，被嵌套的文档作为父文档的值：

{"x":{"foo":"bar"}}

- 对象id

对象id是一个12字节的ID，是文档的唯一表示。

{"x":objectId()}

- 二进制数据
- 代码

## _id 和 ObjectId

- ObjectId是"_id"的默认类型。轻量型，不同机器都能用全局唯一的同种方法方便生成它。
- ObjectId使用12字节存储空间，由24个十六进制数字组成的字符串。
- ObjectId的12字节按照如下方式生成：

```shell
0 1 2 3|4 5 6|7 8|9 10 11

时间戳  机器   PID  计数器
```

**一秒钟最多允许每个进程拥有16777216个不同的ObjectId**

## shell小贴士

shell内置了帮助文档：

```shell
> help
	db.help()                    help on db methods
	db.mycoll.help()             help on collection methods
	sh.help()                    sharding helpers
	rs.help()                    replica set helpers
	help admin                   administrative help
	help connect                 connecting to a db help
	help keys                    key shortcuts
	help misc                    misc things to know
	help mr                      mapreduce

	show dbs                     show database names
	show collections             show collections in current database
	show users                   show users in current database
	show profile                 show most recent system.profile entries with time >= 1ms
	show logs                    show the accessible logger names
	show log [name]              prints out the last segment of log in memory, 'global' is default
	use <db_name>                set current database
	db.foo.find()                list objects in collection foo
	db.foo.find( { a : 1 } )     list objects in foo where a == 1
	it                           result of the last line evaluated; use to further iterate
	DBQuery.shellBatchSize = x   set default number of items to display on shell
	exit                         quit the mongo shell

```

- db.help() 查看数据库级别帮助
- db.foo.help() 查看集合级别帮助
- db.foo.update 查看函数帮助

## 编辑复合变量

- shell中设置EDITOR变量

```shell
> post = {"title":"this is test"}
{ "title" : "this is test" }
> db.blog.insert(post)
WriteResult({ "nInserted" : 1 })
> EDITOR = "/usr/bin/emacs"
/usr/bin/emacs
> var wap = db.blog.findOne({title:"this is test"})
> wap
{ "_id" : ObjectId("59df2eca8edd92495ec325e5"), "title" : "this is test" }
> edit wap
保存并退出     $ ctrl-x ctrl-c (两个连续的组合按键)
> wap
{ "_id" : ObjectId("59df2eca8edd92495ec325e5"), "title" : "this is tesit" }

```

## 批量插入

- Insert 函数

```shell
> db.blog.insert([{"_id": 0},{"_id": 1},{"_id": 2}])
BulkWriteResult({
	"writeErrors" : [ ],
	"writeConcernErrors" : [ ],
	"nInserted" : 3,
	"nUpserted" : 0,
	"nMatched" : 0,
	"nModified" : 0,
	"nRemoved" : 0,
	"upserted" : [ ]
})
> db.blog.find()
{ "_id" : ObjectId("59df2eca8edd92495ec325e5"), "title" : "this is test" }
{ "_id" : 0 }
{ "_id" : 1 }
{ "_id" : 2 }
```

> 3.2.3 Insert 函数可批量插入 2.4.0 batchInsert函数批量插入

## 删除文档

```shell
> db.blog.find()
{ "_id" : ObjectId("59df2eca8edd92495ec325e5"), "title" : "this is test" }
{ "_id" : 0 }
{ "_id" : 1 }
{ "_id" : 2 }
> 
> db.blog.remove({"title" : "this is test"})
WriteResult({ "nRemoved" : 1 })
> db.blog.find()
{ "_id" : 0 }
{ "_id" : 1 }
{ "_id" : 2 }
> db.blog.remove({"_id" : 1})
WriteResult({ "nRemoved" : 1 })
> db.blog.find()
{ "_id" : 0 }
{ "_id" : 2 }
```

## 删除速度

```shell
> for (var i = 0; i < 100000; i++){
... db.tester.insert({"foo":"bar","baz":i,"z":10 - i})
... }
> db.tester.find()
{ "_id" : ObjectId("59df3d738edd92495ec325e6"), "foo" : "bar", "baz" : 0, "z" : 10 }
{ "_id" : ObjectId("59df3d738edd92495ec325e7"), "foo" : "bar", "baz" : 1, "z" : 9 }
{ "_id" : ObjectId("59df3d738edd92495ec325e8"), "foo" : "bar", "baz" : 2, "z" : 8 }
{ "_id" : ObjectId("59df3d738edd92495ec325e9"), "foo" : "bar", "baz" : 3, "z" : 7 }
{ "_id" : ObjectId("59df3d738edd92495ec325ea"), "foo" : "bar", "baz" : 4, "z" : 6 }
{ "_id" : ObjectId("59df3d738edd92495ec325eb"), "foo" : "bar", "baz" : 5, "z" : 5 }
{ "_id" : ObjectId("59df3d738edd92495ec325ec"), "foo" : "bar", "baz" : 6, "z" : 4 }
{ "_id" : ObjectId("59df3d738edd92495ec325ed"), "foo" : "bar", "baz" : 7, "z" : 3 }
{ "_id" : ObjectId("59df3d738edd92495ec325ee"), "foo" : "bar", "baz" : 8, "z" : 2 }
{ "_id" : ObjectId("59df3d738edd92495ec325ef"), "foo" : "bar", "baz" : 9, "z" : 1 }
{ "_id" : ObjectId("59df3d738edd92495ec325f0"), "foo" : "bar", "baz" : 10, "z" : 0 }
{ "_id" : ObjectId("59df3d738edd92495ec325f1"), "foo" : "bar", "baz" : 11, "z" : -1 }
{ "_id" : ObjectId("59df3d738edd92495ec325f2"), "foo" : "bar", "baz" : 12, "z" : -2 }
{ "_id" : ObjectId("59df3d738edd92495ec325f3"), "foo" : "bar", "baz" : 13, "z" : -3 }
{ "_id" : ObjectId("59df3d738edd92495ec325f4"), "foo" : "bar", "baz" : 14, "z" : -4 }
{ "_id" : ObjectId("59df3d738edd92495ec325f5"), "foo" : "bar", "baz" : 15, "z" : -5 }
{ "_id" : ObjectId("59df3d738edd92495ec325f6"), "foo" : "bar", "baz" : 16, "z" : -6 }
{ "_id" : ObjectId("59df3d738edd92495ec325f7"), "foo" : "bar", "baz" : 17, "z" : -7 }
{ "_id" : ObjectId("59df3d738edd92495ec325f8"), "foo" : "bar", "baz" : 18, "z" : -8 }
{ "_id" : ObjectId("59df3d738edd92495ec325f9"), "foo" : "bar", "baz" : 19, "z" : -9 }
Type "it" for more
> db.tester.count()
100000

> var timeRemoves = function() {
... ... var start = (new Date()).getTime();
... ... db.tester.remove({});
... ... db.tester.findOne();
... ... var timeDiff = (new Date()).getTime() - start;
... ... print("Remove took: "+timeDiff+"ms");
... ... }
> timeRemoves()
Remove took: 2ms
> db.tester.count()
0

```

> 如何恢复数据？