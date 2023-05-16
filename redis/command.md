# 查看redis占用的内存大小
```shell
root@iZ8vb6gwye4at18xg5j961Z:~# redis-cli -p 6888
127.0.0.1:6888> auth password
127.0.0.1:6888> info
# Memory
# used_memory:1004885560 占用内存大小(byte)
# used_memory_human:958.33M 占用的内存大小(人类可读)
# used_memory_rss:1031032832
# used_memory_peak:1034404104 占用内存大小峰值
# used_memory_peak_human:986.48M 占用内存大小峰值(人类可读)
# used_memory_lua:91136
# mem_fragmentation_ratio:1.03 内存碎片比例
# mem_allocator:jemalloc-3.6.0
```

# getset
```python
GETSET can be used together with INCR for counting with atomic reset. For example: a process may call INCR against the key mycounter every time some event occurs, but from time to time we need to get the value of the counter and reset it to zero atomically. This can be done using GETSET mycounter "0":
```
翻译:
```python
GETSET可以与INCR一起用于原子复位计数。例如：每当某个事件发生时，进程可能会对密钥mycounter调用INCR，但我们需要不时地获取计数器的值，并将其原子重置为零。这可以使用GETSET mycounter 0来完成
```

网上看到别人的场景是这样的
需要记录接口的网访问次数, 先通过redis缓存进行计数, 然后每隔一段时间更新到MySQL中, 操作如下
```redis
# 接口产生访问时进行自增
incr "counter"

每个一分钟读取counter, 并将其重置为0
getset counter 0
```

