# 一、Core Options
[TOC]

## systemLog Options

```shell
systemLog:
   verbosity: <int>    在3.0版更改，详细级别决定了MongoDB输出的信息量和调试量，默认为0     
   quiet: <boolean>    静默模式，不推荐生产使用，不利于排查问题
   traceAllExceptions: <boolean>    打印详细的调试信息。使用其他日志记录进行支持相关的故障排除。
   syslogFacility: <string>    将消息记录到系统日志时使用的设施级别。
   path: <string>    mongod或mongos应发送所有诊断日志信息的日志文件的路径，在指定的路径上创建日志文件
   logAppend: <boolean>    为true，则在mongos或mongod 实例重新启动时将新条目附加到现有日志文件的末尾
   logRotate: <string>    3.0.0新版功能，三个选项 rename,reopen,logAppend必须为true
   destination: <string>    MongoDB发送所有日志输出的目的地两个选项：file or syslog
   timeStampFormat: <string> Default: iso8601-local 1969-12-31T19:00:00.000-0500
   component:
      accessControl:
         verbosity: <int>
      command:
         verbosity: <int>
         
eg:
systemLog:
   destination: file
   path: "/alidata/mongodb/log/mongod_22001.log"
   logAppend: true
```

>verbosity: 
>
>详细级别的范围可以从0到5：
>
>0是MongoDB默认的日志详细级别，包含 信息性消息。
>
>1到 5增加了详细级别以包含 调试消息。
>
>参考地址：http://docs.mongoing.com/reference/log-messages.html#log-messages-configure-verbosity
>
>logRotate：
>
>rename：重命名日志文件。
>reopen：关闭并重新打开日志文件，遵循典型的Linux / Unix日志旋转行为。使用Linux / Unix的logrotate工具时要重新打开，以避免日志丢失。
>reopen：则还必须将systemLog.logAppend设置为true。

## processManagement Options
```shell
processManagement:
   fork: <boolean>    默认：False 启用在后台运行mongos或mongod进程的守护进程模式
   pidFilePath: <string>
```

## net Options

```shell
net:
   port: <int>    默认：27017
   bindIp: <string>    默认：所有接口。mongos或mongod绑定的IP地址，以侦听来自应用程序的连接要绑定到多个IP地址，请输入逗号分隔值列表。
   maxIncomingConnections: <int>    默认：65536。mongos或mongod可以接受的最大并发连接数。
   wireObjectCheck: <boolean>    默认值：True
   ipv6: <boolean> 在版本3.0中删除。MongoDB 3.0和更高版本中，IPv6始终处于启用状态。
   unixDomainSocket:
      enabled: <boolean>
      pathPrefix: <string>    默认：/ tmp
      filePermissions: <int>    默认：0700 设置UNIX域套接字文件的权限 只适用于基于Unix的系统
   http:
      enabled: <boolean>    Default: False 3.2 版后已移除
      JSONPEnabled: <boolean>
      RESTInterfaceEnabled: <boolean>
   ssl:
      sslOnNormalPorts: <boolean>  2.6版后已移除。在3.0版本更改：大多数MongoDB发行版现在包含对TLS / SSL的支持
      mode: <string>    2.6 新版功能.
      PEMKeyFile: <string>
      PEMKeyPassword: <string>
      clusterFile: <string>
      clusterPassword: <string>
      CAFile: <string>
      CRLFile: <string>
      allowConnectionsWithoutCertificates: <boolean>
      allowInvalidCertificates: <boolean>
      allowInvalidHostnames: <boolean>
      disabledProtocols: <string>
      FIPSMode: <boolean>
```

## security Options

```shell
 security:
   keyFile: <string>
   clusterAuthMode: <string>    2.6新版功能。
   authorization: <string>    默认：禁用 启用或禁用基于角色的访问控制（RBAC）来控制每个用户对数据库资源和操作的访问。
   transitionToAuth: <boolean>    默认：False 3.4 新版功能: 
   javascriptEnabled:  <boolean>    默认值：True 启用或禁用服务器端JavaScript执行
   redactClientLogData: <boolean>    3.4新版功能：仅适用于MongoDB Enterprise。
   sasl:
      hostName: <string>
      serviceName: <string>
      saslauthdSocketPath: <string>
   enableEncryption: <boolean>    默认：False 3.2新版功能：为WiredTiger存储引擎启用加密 仅在MongoDB Enterprise中可用
   encryptionCipherMode: <string>    3.2新版功能 仅在MongoDB Enterprise中可用
   encryptionKeyFile: <string>    仅在MongoDB Enterprise中可用
   kmip:
      keyIdentifier: <string>    3.2新版功能
      rotateMasterKey: <boolean>
      serverName: <string>
      port: <string>
      clientCertificateFile: <string>
      clientCertificatePassword: <string>
      serverCAFile: <string>
   ldap:    3.4新版功能：仅适用于MongoDB Enterprise。
      servers: <string>
      bind:
         method: <string>
         saslMechanism: <string>
         queryUser: <string>
         queryPassword: <string>
         useOSDefaults: <boolean>    3.4新版功能：仅适用于Windows平台的MongoDB Enterprise。
      transportSecurity: <string>
      timeoutMS: <int>
      userToDNMapping: <string>
      authz:
         queryTemplate: <string>
```





