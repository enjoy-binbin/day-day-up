*系统演示是基于mac下的redis4.0.14环境*



Redis作为一个C语言编写的内存型kv高性能的单线程nosql数据库，在运行情况下，Redis 以数据结构的形式将数据维持在内存中， 为了让这些数据在 Redis 重启之后仍然可用，就需要对这些数据进行持久化操作。



Redis为持久化提供了两种方式：

- RDB：Redis Database 是默认开启的持久化方式，通过rdb程序将当前内存中的数据库快照保存到磁盘文件中。默认会将数据库快照保存在名字为dump.rdb的二进制文件中。在重启的时候通过加载RDB文件来还原数据库的状态。
- AOF：Append Only File 默认关闭的，记录每次对服务器写的操作，以追加写的方式将这些写操作命令写入磁盘，当服务器重启的时候会重新执行这些命令来恢复原始的数据。



## RDB

**1. rdb原理是什么**

原理是redis会单独fork创建一个与当前进程一样的子进程来进行持久化，这个子进程的所有数据（变量、环境变量、程序计数器等）都和原进程一样。之后在这个`redis-rdb-bgsave`进程中进行持久化。持久化会先将数据写入到一个临时文件中，等持久化结束后，会用这个临时文件替换之前持久化好的文件。

整个过程中，原进程不进行任务的io操作，以此来保障性能。

save命令和bgsave命令。前者是会阻塞掉redis的，因为redis是单线程，所以都是使用basave（background save）来在后台进行rdb的持久化。

```
# 可以找个大点数据量的redis来触发rdb, 然后用下面命令查看进程
ps -ef | grep redis
```



核心功能就是*rdbSave和rbdLoad*了，前者用来生成rbg文件到磁盘，后者用来将磁盘数据加载回内存。

`rdbSave` 函数负责将内存中的数据库数据以 RDB 格式保存到磁盘中， 如果 RDB 文件已存在， 那么新的 RDB 文件将替换已有的 RDB 文件。

在保存 RDB 文件期间， 主进程会被阻塞， 直到保存完成为止。

[SAVE](http://redis.readthedocs.org/en/latest/server/save.html#save) 和 [BGSAVE](http://redis.readthedocs.org/en/latest/server/bgsave.html#bgsave) 两个命令都会调用 `rdbSave` 函数，但它们调用的方式各有不同：

- [SAVE](http://redis.readthedocs.org/en/latest/server/save.html#save) 直接调用 `rdbSave` ，回阻塞 Redis 主进程，直到保存完成为止。在主进程阻塞期间，服务器不能处理客户端的任何请求。
- [BGSAVE](http://redis.readthedocs.org/en/latest/server/bgsave.html#bgsave) 则 `fork` 出一个子进程，子进程负责调用 `rdbSave` ，并在保存完成之后向主进程发送信号，通知保存已完成。因为 `rdbSave` 在子进程被调用，所以 Redis 服务器在 [BGSAVE](http://redis.readthedocs.org/en/latest/server/bgsave.html#bgsave) 执行期间仍然可以继续处理客户端的请求。



**2. 持久化文件存在哪？**

这跟配置文件中的几个参数有关，其中dbfiename指定了持久化的文件名，dir 指定了持久化文件所在的目录（默认是在启动redis-server的当前目录）。目录最好就还是自己指定一个，因为如果在不同目录启动了redis-server，会缺少之前的部数据，因为数据是存在dump.rdb中，在启动时加载进去的。

相关配置项，最好就是可以去看官方原文件里的相关英语注释拉

```
# 文件保存的名称
dbfilename dump.rdb

# 文件保存的路径, 默认是启动server时的当前目录
dir ./

# 进行快照的时间策略, xx 秒钟 有 几个key 发生变动
#   In the example below the behaviour will be to save:
#   after 900 sec (15 min) if at least 1 key changed
#   after 300 sec (5 min) if at least 10 keys changed
#   after 60 sec if at least 10000 keys changed
save 900 1
save 300 10
save 60 10000

# 如果持久化出错，主进程是否停止写入，默认是yes，为了数据一致性
stop-writes-on-bgsave-error yes

# 是否压缩, 默认也是yes, 可以不开启, 相对硬盘, 可能cpu更划算
rdbcompression yes

# 导入时是否检查
rdbchecksum yes

# 如果想要禁用rbd
# save ""
```



**3. 什么时候触发rdb?**

- 在服务正常shutdown的时候，如果没有开启AOF，会触发。
- 主从全量复制时候，主节点会发送rdb文件给从，会触发
- 使用save或者bgsave命令，当然前者会阻塞，后者会在后台子进程异步进行持久化 同时不影响主进程响应客户端请求
- 当满足上面配置文件里设置的快照策略的时候
- 使用flushall命令清库的时候



**4. rdb的优缺点**

**优点:**

完全备份，不同时间的数据集备份可以做到多版本恢复（会覆盖 手动写脚本扫描目录拿走不同阶段备份，异地备份）

紧凑的单一文件，方便网络传输，适合灾难恢复

恢复大数据集速度较AOF快

**缺点:**

会丢失最近写入、修改的而未能持久化的数据

fork过程非常耗时，会造成毫秒级不能响应客户端请求

**生产环境:**

创建一个定时任务cron job，每小时或者每天将dump.rdb复制到指定目录

确保备份文件名称带有日期时间信息，便于管理和还原对应的时间点的快照版本

定时任务删除过期的备份

如果有必要，跨物理主机、跨机架、异地备份



## AOF

**1. aof原理**

默认是关闭的。原理是将Redis的操作日志以追加的方式写入文件末尾，行为有点类似Mysql中statement的binblog二进制逻辑日志文件吧，不过记录的是redis协议AOF命令。记录了所有的写操作命令，在服务恢复的时候就可以使用这些命令还原redis。类似与Mysql中的redo log和redo buf，redis也会将增量的aof先写入到aof buf中，再通过fsync写入到aof磁盘中，提高性能。

同时aof有重写的机制，重写是为了减少aof文件的大小，可以手动或者自动触发，关于自动触发的规则请看下面配置部分。fork的操作也是发生在重写这一步，同rdb一样会fork个子进程来负责重写aof文件。子进程会创建一个临时文件写入AOF信息，父进程会开辟一个内存缓冲区接收新的写命令，子进程重写完成后，父进程会获得一个信号，将父进程接收到的新的写操作由子进程写入到临时文件中，新文件替代旧文件。注：如果写入操作的时候出现故障导致命令写半截，可以使用redis-check-aof工具修复

fork一个子进程负责重写AOF文件

子进程会创建一个临时文件写入AOF信息

父进程会开辟一个内存缓冲区接收新的写命令，并将这些改动追加写到现有的AOF文件中（防止宕机）

子进程重写完成后，父进程会接受到一个信号，将内存缓存中的数据写到新的AOF临时文件中

新AOF临时文件替代旧文件（rename操作）



**2. 持久化文件在哪里和触发机制？**

跟上面rdb存放的地方一样，根据配置文件里的`dir`来设置存放路径，触发机制也有配置项可以控制或者手动发送`BGREWRITEAOF`命令

```
# 是否开启aof，默认是关闭的
appendonly no

# 持久化文件名称
appendfilename "appendonly.aof"

# 文件保存的路径, 默认是启动server时的当前目录
dir ./

# 同步方式，默认是每秒一次，表明最多会丢失一秒内的数据
# 其中always表示每次变更都进行（性能慢，安全），no表示由操作系统来控制（性能快，持久化不受我们控制）
# appendfsync always
appendfsync everysec
# appendfsync no

# aof重写期间是否同步
no-appendfsync-on-rewrite no

# 重写触发配置，一般会把这个触发的最小体积size调大
# 触发重写所需的AOF文件体积百分比：当AOF文件的体积大于auto-aof-rewrite-min-size指定的体积，并且超过上一次重写之后的AOF文件体积的percent时，就会触发AOF重写，将这个值设置为0表示关闭自动AOF重写
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# 加载aof时如果有错会发log给客户端同时继续
aof-load-truncated yes

# 文件重写策略
aof-rewrite-incremental-fsync yes
```



aof文件示例，里面记录了友好可读的redis协议命令，下面是我执行了`set name binbin 和 set age 22`后的aof文件内容。默认进来是选择了第0库

```
*2					# select 0, 分成两段
$6
SELECT			# select 6个字符
$1
0						# 0 1个字符
*3					# set name binbin, 分成三段
$3
set					# set 3个字符
$4
name				# name 4个字符
$6
binbin			# binbin 6个字符
*3
$3
set
$3
age
$2
22
```



**3. aof的优缺点**

**优点:**

写入机制，默认fysnc是每秒执行，性能很好不阻塞服务，最多丢失一秒的数据

有重写机制，可以优化aof文件，采用的文本协议，追加方便可读性高兼容性好

如果误操作了（FLUSHALL等），只要AOF未被重写，停止服务移除AOF文件尾部FLUSHALL命令，重启Redis，可以将数据集恢复到 FLUSHALL 执行之前的状态

**缺点：**

相同数据集，AOF文件体积较RDB会大了很多

恢复数据库速度叫RDB慢（文本，命令重演）逻辑日志恢复肯定没物理日志快



课后延伸阅读：redis的设计与实现