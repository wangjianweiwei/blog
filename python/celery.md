### celery worker只消费指定Queue中的消息

**问题概述：**
         目前有很多的队列，但是worker只有一台，出于业务的需要，无奈需要加几个任务消息， 但是新加的这几个任务消息的计算速度非常的慢，又不想影响原本的任务消息，所有就新加了一台worker专门消费新的的任务消息。**需要将某些任务消息在固定的worker上被消费**。

**问题解答：**
        celery worker在启动时有两个参数可以解决这个问题
1. `--queues QUEUES, -Q`指定当前启动的worker只从某些队列中获取消息*，多个队列使用逗号间隔即可*
2. `--exclude-queues EXCLUDE_QUEUES, -X`指定当前启动的worker排除某些队列中，不从这些队列中获取消息，*多个队列使用逗号间隔即可*

**示例：**
```shell
python run.py -s task -n worker1 -Q task1,task2
python run.py -s task -n worker2 -exclude task1,task2
```
*我的调用方式可能和celery标准的不太一样，因为我把Flask和Celery的启动封装到了一起*

这样的话task1,task2只在worker1上被消费
