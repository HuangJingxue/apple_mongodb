# mongodb

MongoDB 是一款强大，灵活，且易于扩展的通用性数据库，**面向文档的数据库**。

- 二级索引
- 范围查询
- 排序
- 聚合
- 地理空间索引

丰富的功能：

- 索引（indexing）

MongoDB支持通用二级索引，允许多种快速查询，且提供唯一索引、复合索引、地理空间索引，以及全文索引。

- 聚合（aggregation）

MongoDB支持“聚合管道”。用户能通过简单的片段创建复杂的聚合，并通过数据库自动优化。

- 特殊的集合类型

MongoDB支持存在时间有限的集合，适用于那些将在某个时刻过期的数据，如会话。固定大小的集合，用于保存近期数据，如日志。

- 文件存储

MongoDB支持一种非常医用的协议，用于存储大文件和文件元数据。

基本概念：

- 文档是MongoDB中数据的基本单元，非常类似于关系型数据库管理系统中的行，但更具有表现力。
- 集合是一个拥有动态模式的表。
- MongoDB的一个实例可以拥有多个相互独立的数据库，每一个数据库都拥有自己的集合。
- 每一个文档都有一个特殊的键“_id”,这个键在文档所属的集合中是唯一的。
- MongoDB自带了一个简单但功能强大的JavaScript shell，可用于管理MongoDB的实例或数据操作。

## 基础知识

集合命名：

- 集合名不能使空字符串（""）
- 集合名不能包含\0字符（空字符），这个字符表示集合名的结束。
- 集合名不能以"system."开头，这是为系统集合保留的前缀。
- 用户创建的集合不能在集合名中包含保留字符'$'。

子集合：

组合集合的一种惯例是使用“.”分隔不同命名空间的子集合。

- GridFS使用自己和来存储文件的元数据，这样就可以与文件内容块很好地隔离开来。
- 大多数驱动程序都提供了一些语法糖，用于访问指定集合的子集合。

数据库：

- 多个文档组成集合，多个集合可以组成数据库。
- 一个MongoDB实例可以承载多个数据库，每个数据库拥有0个或者多个集合。
- 每个数据库斗殴独立的权限，即便是在磁盘上，不同的数据库也放置在不同的文件中。

数据库命名：

- 不能空字符串（""）
- 基本只能使用ASCII中的字母和数字。
- 数据库名区分大小写（不区分大小写的文件系统也是如此，建议全部小写）。
- 数据库名最多为64字节。

## 启动关闭MongoDB

- mongod默认数据目录/data/db（Windows系统中为C:\data\db）。
- 启动前，创建数据目录（mkdir -p /data/db）,确保对改目录有写权限。
- 默认MonoDB监听27017端口。

## MonogDB客户端

- 启动时，mongodb shell会练到MongoDB服务器的test数据库，并将数据库连接赋值给全局变量db。
- 这个变量是通过shell访问MongoDB的主要入口点。

## shell中的基本操作

1、创建

- insert函数可将一个文档添加到集合中。
- 创建一个名为post的局部变量，用来表示我们的文档。
- 它会有几个键："title"、"content"、“date”。

```shell
> post = {"title":"this is test,"}
{ "title" : "this is test," }
> post = {"title":"this is test",
... "content" :"here's my blog test",
... "data":new Date()}
{
	"title" : "this is test",
	"content" : "here's my blog test",
	"data" : ISODate("2017-10-12T03:20:09.121Z")
}
> show dbs
local  0.000GB
> use hjxdb
switched to db hjxdb
> db.blog.insert(post);
WriteResult({ "nInserted" : 1 })
> db.blog.find()
{ "_id" : ObjectId("59dedf7ecb7cf32013d3da35"), "title" : "this is test", "content" : "here's my blog test", "data" : ISODate("2017-10-12T03:20:09.121Z") }
```

2、读取

find和findOne方法可以用于查询集合里的文档。若只想查看一个文档，可用findOne：

```shell
> db.blog.findOne()
{
	"_id" : ObjectId("59dedf7ecb7cf32013d3da35"),
	"title" : "this is test",
	"content" : "here's my blog test",
	"data" : ISODate("2017-10-12T03:20:09.121Z")
}
```

3、更新

- update至少两个参数
- 一个是限定条件,匹配待更新的文档
- 一个是新的文档
- 之前的文章增加平冷功能，新增一个键，用来保存评论数组

增加"comments"键：

```shell
> post.comments = []
[ ]
> db.blog.update({title:"this is test"},post)
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.blog.find()
{ "_id" : ObjectId("59dedf7ecb7cf32013d3da35"), "title" : "this is test", "content" : "here's my blog test", "data" : ISODate("2017-10-12T03:20:09.121Z"), "comments" : [ ] }
```

4、删除

- remove方法可将文档从数据库中永久删除。
- 没有任何参数，将删除集合内的所有文档全部删除。
- 接受一个限定条件的文档作为参数。

```shell
> db.blog.remove({title:"this is test"})
WriteResult({ "nRemoved" : 1 })
> db.blog.find()
```



