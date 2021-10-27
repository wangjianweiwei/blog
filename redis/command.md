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

