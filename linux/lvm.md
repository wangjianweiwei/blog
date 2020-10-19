公司的一台服务器硬盘满了，mongo数据库存了480G的数据，硬盘只有500G(阿里云单块盘最大500G)，单块盘已经不能再扩容，所以只能通过加盘的方式解决了，很早以前(年代就远了)学过LVM， 这次搞之前也是作了很多准备工作(还不是怕出问题)

先上图，了解下LVM是如果解决磁盘动态扩容这个问题的
![image](https://user-images.githubusercontent.com/41533289/84118419-8e0f2f00-aa65-11ea-9322-256198cd94e0.png)


原理很简单，把一堆物理盘做成一个组，然后再从这个组中割一块，然后进行挂载，就可以用了，
我理解的就是**集中管理，按需分配**
原理就是这么个原理，咋实现的我不知道。。。。

先看下当前服务器下的磁盘
```shell
haima@ubuntu:~$ lsblk 
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0    10G  0 disk 
├─sda1   8:1    0     9G  0 part /
├─sda2   8:2    0     1K  0 part 
└─sda5   8:5    0  1022M  0 part 
sdb      8:16   0     6G  0 disk 
sdc      8:32   0    10G  0 disk 
```

# 创建PV
```shell
haima@ubuntu:~$ sudo pvcreate /dev/sdb
  Physical volume "/dev/sdb" successfully created
```
# 查看创建的PV
```shell
haima@ubuntu:~$ sudo pvdisplay 
  "/dev/sdb" is a new physical volume of "6.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdb
  VG Name               
  PV Size               6.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               sqZVXQ-fNXQ-EBk6-ncy1-Njl6-vcnY-OZVP7K
```

# 创建VG
创建mongo_data卷组, 让/dev/sdb加入
```shell
haima@ubuntu:~$ sudo vgcreate mongo_data /dev/sdb
  Volume group "mongo_data" successfully created
```

# 查看创建的VG
```shell
haima@ubuntu:/tmp$ sudo vgdisplay 
[sudo] password for haima: 
  --- Volume group ---
  VG Name               mongo_data
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                1
  Open LV               1
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               15.99 GiB
  PE Size               4.00 MiB
  Total PE              4094
  Alloc PE / Size       3840 / 15.00 GiB
  Free  PE / Size       254 / 1016.00 MiB
  VG UUID               UK11MD-qVBZ-kxvQ-8pNA-ZD4E-zwOB-1J0yRH
```
**PE Size值得是这个组的最小单元，默认是4M，要想该的话得保证是2的倍数**

刚刚是在创建VG的时候把PV加进去了，那其他的的么加呢， 像下面这个样就可以了
```shell
vgextend mongo_data /dev/sdc 
```

至此**集中管理**已经做完了，下面就是**按需分配了**
# 创建LV
```shell
lvcreate -L 840G -n mongo mongo_data 
```
`-L`: 指定的是需要多个空间
`-l`: 指定需要多少个PE
以上两个参数二选一即可

# 格式化

```shell
mkfs.ext4 /dev/mongo_data/mongo
```

# 挂载
```shell
vim /etc/fstab    # 修改分区表
monut -a
```

整个过程就完了，还算顺利。



