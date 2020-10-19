
ansible常常被定义为**配置管理工具**，常与Chef, Puppet以及Salt相提并论
# 安装Ansible
```shell
yum install ansible
# 或者
pip install ansible
```

## 查看ansible的模块文档

```shell
ansible-doc service
```



## command

```shell
ansible test -m command -a uptime
# command是非常常用的模块，ansible将他设置为默认使用的模块，所以可以简化上面的命令
ansible test -a uptime
```

如果命令中包含空格，那么就需要使用引号括起来，这样shell才会将整个字符串作为一个参数传给ansible，例如

```shell
ansible test -a "tail /var/log/dmesg"
```

如果需要使用root来执行，需要传入参数**-b**告诉ansible使用sudo以root的身份来执行，例如

```shell
ansible test -b -a "tail /var/log/boot.log"
```

## apt

使用apt包管理器安装或删除软件包

## copy

将一个文件从本地复制到远程的主机上

## file

设置文件，符号链接或目录的属性

## service

启动，停止或重启一个服务

## template

从模板生成一个文件并复制到远程主机上

# playbook

playbook其实就是一个字典列表，明确的讲一个playbook就是一个play列表

每一个paly中需要包含如下两项

- hosts 主机
- 需要在主机上执行的任务

可以把play想想层连接到主机上执行的任务

**示例playbook**

```yaml
- name: Configure webserver with Nginx
  hosts: ubuntu
  become: True
  tasks:
    - name: install Nginx
      apt: name=nginx update_cache=yes 

    - name: copy Nginx config file
      copy: src=files/nginx.conf dest=/etc/nginx/sites-available/default

    - name: enable configuration
      file: dest=/etc/nginx/sites-enabled/default src=/etc/nginx/sites-available/default state=link
    
    - name: copy index.html
      template: src=templates/index.html.j2 dest=/usr/share/nginx/html/index.html mode=0644

    - name: restart Nginx
      service: name=nginx state=restarted
```



除了声明hosts和tasks以外, play还支持一些可选的配置，常见的配置项如下

- name

  描述这个play的制单文字注释。ansible将会在play开始执行的时候打印出来

- become

  如果为真，ansible会在运行每个任务的时候后切换为root用户，在管理ubuntu服务器的时候这个配置非常有用，因为ubuntu默认不允许root用户进行SSH登录

- vars

  一系列变量和值

## task

在示例中playbook是一个包含5个task的play，下面是play的第一个task

```yaml
- name: install Nginx
  apt: name=nginx update_cache=yes
```

name是可选的，所以像下面的task也是合法的

```yaml
- apt: name=nginx update_cache=yes
```

尽管name是可选的，还是建议加以配置，因为他对于task有非常好的提示作用。

每个任务必须要包含一个键值对，键是模块名称，值时要传到模块的参数，就像示例中的task，模块名是apt，参数是name=nginx update_cache=yes， 这写参数告诉apt模块安装一个nginx的软件并在安装软件之前更新软件包缓存。

有一点很重要：从ansible前端使用yaml解释器角度出发，参数将按照字符串处理，而不是字典，这意味着如果想将参数分割成多行，就需要像如下这样的方式使用分行语法：

```yaml
- name: install Nginx
  apt: >
  	name=nginx
  	update_cache=yes
```



**关于handler几件需要记住的事情**

handler只会在**所有task执行完成后**执行，哪怕被通知多次，他只执行一次，当play中定义了个多个handler时，handler的执行顺序是按照定义的顺序，而不是通知的顺序。

ansible官方文档中提到，handler唯一常见的用途就是重启服务或服务器，因为handler是一个很优雅的选择。



# YAML

## 文档起始

yaml文档使用三个减号开头用于标记文档的开始, *不过在playbook开头忘记写三个减号并不会影响ansible的执行*

```shell
---
```

## 注释

注释使用#号

```shell
# 这是一行注释
```

## 字符串

一般而言，yaml的字符串是不需要使用引号的，当然如果你喜欢使用引号也没有问题，即便字符串中存在村空也不需要使用引号

```shell
this is YAML string
```

在ansible中有几种比较特殊的情况，需要对字符串使用引号，在这些情况下，通常会使用{{braces}}用于变量替代

## 布尔型

yaml具有内置的布尔类型，并且提供了很多种释义为true或false的字符串，我个人一直在使用True和False

```shell
True
False
```

## 列表

yaml中的列表就好像json和ruby中的数组或者python中的列表，严格说，在yaml中他被叫做序列，但是在这里，为了和ansible官方文档保持一致，我们还是叫他列表。

列表使用减号“-”作为界定符

```yaml
- my fair lady
- ok
- the pirates penzance
```

yaml还支持内联列表

```yaml
[my fair lady, ok, the pirates penzance]
```

## 字典

yaml中的字典就想json中的对象，python中的字典或ruby中的哈希，严格来说，在yaml中应该叫映射，同样为了与ansible官方文档保持一致，我们好是叫他字典。

```yaml
address: 5号楼303
city: BeiJing
state: North Takome
```

yaml也支持内联字典

```yaml
{address: 5号楼303, city: BeiJing, state: North Takome}
```

## 分行

编写playbook时，你经常会碰到向模块传递若干个参数的场景，为了美观起见，你或许希望将这些很长的参数的区段拆分成多行，同时ansible又视为单行字符串。

这完全可以在yaml中实现，yaml中使用大等于号（>）来标记分行，运作时yaml解释器将会把换行符替换为空格

```yaml
address: >
		Department of Computer Science,
		A.V Williams Building,
		University of Maryland
city: BeiJing
state: Maryland

# 相当于json
{
"address": "Department of Computer Science, A.V Williams Building,
						University of Maryland",
"city": "BeiJing",
"state": "Maryland"
}
```

# inventory(主机集合)

到目前为止，我们都是对一台服务器进行操作和管理，但是在显示情况中，肯定要管理更多的机器，ansible可管理的主机集合叫做inventory。

## inventory文件

在ansible中，描述你的主机的默认方法是将他们列咋一个文本文件中，这个文本文件叫做inventory文件，一个简单的inventory文件可能只包含一组主机名称的列表，就像下面这个例子。

```shell
www.baidu.com
blog.baidu.com
mall.baidu.com
```

**inventory指的就是hosts文件，一般情况下我喜欢使用默认的/etc/anisble/hosts**

ansible默认使用本地的ssh客户端，这意味着你在ssh配置文件中设置的任何别名都可以被识别，但是如果你将ansible配置为使用paramiko链接插件代替默认的ssh插件的话，那别别名就不能被识别了。



ansible默认会自动将localhost添加到inventory中，ansible明白localhost代表你的本机，所以他会直接与本家通信而不使用sshl链接。

尽管ansible会自动将localhost添加到inventory中，你还是要在inventory文件中至少添加一台其他主机。

在这种inventory文件中没有其他主机的情况下，你可以显式的添加localhost，如下：

```shell
localhost ansible_connection=local
```

我的inventory文件如下

```shell
[web]
192.168.2.104
[local]
127.0.0.1
[ubuntu]
192.168.2.105
```

除了简单的指定下ip，分下组，还有一些其他的参数：

inventory中的配置可以覆盖默认的配置ansible.cfg中的配置

**ansible_host**

主机名，ssh目标主机名或IP

**ansible_port**

ssh目标端口， 默认22



**ansible_user**

ssh登录时使用的用户，默认root

**ansib_password**

ssh认证时使用密码

**ansible_connection**

ansible使用哪一种链接方式了连接到主机，默认smart

ansible默认支持多种传输机制，所谓传输机制，就是ansible连接到主机的机制，默认使用smart(智能传输模式)，智能传输模式将会检测本地安装的ssh客户端是否支持一个名为`ControlPersist`的特性，如果本地客户端支持ControlPersist，ansible将使用本地ssh客户端，如果本地的ssh客户端不支持ControlPersist，那么执行传输模式将更换为paramiko的python ssh客户端。

**ansible_shell_type**

ansible是通过建立到远程机器的ssh链接，然后调用脚本来工作，默认情况下，ansible假定远程shell是位于/bin/sh的Bourne shell，并且会生成适用于Bourne shell的命令行参数。

ansible还支持csh，fish和windows上的powershell，作为参数的合法值，一般都没有修改的需求。

**ansible_python_interpreter**

由于ansible附带的模块是使用python2编写的，因此ansible需要之慈宁宫远程主机上python解释器的路径，如果远端的python解释器路径不是/usr/bin/pyhthon，那就需要使用这个参数来指定python解释器在远端的路径。

**ansible_*_interpreter**

如果你使用了非python的自定义模块，可以使用这个参数来指定解释器的路径(/usr/bin/ruby)



## 群组

在执行任务的时候，我们更希望针对一组主机来执行操作而不是只对一台主机，ansible自动定义了一个群组叫all或*，他包括inventory中的所有主机，例如：我们可以通过如下命令来检测主机上的时钟是否大致上同步

```shell
# 方式一
ansible "*" -a "date"
# 方式二
ansible all -a date
# 输出如下
127.0.0.1 | SUCCESS | rc=0 >>
Sat Sep 14 06:13:45 EDT 2019

39.106.15.4 | SUCCESS | rc=0 >>
Sat Sep 14 18:13:47 CST 2019

192.168.2.104 | SUCCESS | rc=0 >>
Sun Sep 15 02:13:25 CST 2019

192.168.2.105 | SUCCESS | rc=0 >>
Sun Sep 15 02:13:25 CST 2019
```

可以在inventory文件中定义自己的群组，ansible的inventory文件是ini格式，在ini中，同类的配置值归类在一起组成区段。

例如我的inventory文件（/etc/ansible/hosts）

```ini
[centos]
39.106.15.4
192.168.2.105
192.168.2.104
[local]
127.0.0.1
```

也可以像下面这种形式

```ini
ali ansible_host=39.106.15.4
vm-centos-1 ansible_host=192.168.2.104
vm-centos-2 ansible_host=192.168.2.105
local-mac ansible_host=127.0.0.1

[centos]
ali
vm-centos-1
vm-centos-2
[local]
local-mac
```

**ansible的inventory只能将一台主机与127.0.0.1相联**



## 群组的群组

ansible也允许定义有群组组成的群组，例如，web服务器和任务队列都需要安装django以及其依赖包，如果定义一个名为django的群组，他包括一个名为django的群组，他包括web和task两个群组的话，那么解决这个问题将会很简单，可以在inventory文件中添加一下内容来实现刚才有群组组成的群组的想法。

```ini
[web]
web-1 ansible_host=127.0.0.1 ansible_port=2022 ansible_user=root
web-2 ansible_host=127.0.0.1 ansible_port=2023 ansible_user=root

[nginx]
nginx-1 ansible_host=127.0.0.1 ansible_port=2024 ansible_user=root

[docker:children]
web
nginx
```

**需要注意的事：**对比只有主机的群组，指定群组的群组在语法上会有变化，这是为了让ansible知道应该将web和task解释为群组，而不是主机。

## 为主机编号

例如你有20台服务器，命名为web1.example.com......web20.example.com，这样的话你就可以使用下面编号的形式来指代他们：

```ini
[web]
web[1:20].example.com
```

如果你习惯以零开头，例如web01.example.com，那么指定一个以0开头的范例如下：

```ini
[web]
web[01:20].example.com
```

ansible也支持使用字母序的方式来指定范围，如果你希望使用字母序列规则的20台服务器的名为web-a.exapmle.com那么可以这样来指定：

```ini
[web]
web-[a-t].exapmle.com
```

## 在inventory内部的主机和组变量

回顾下我们在inventory中指定的指定的参数

```ini
ali ansible_host=39.106.15.4 ansible_port=22
```

这些参数就是具有特殊意义的ansible变量，我们也可以针对主机定义任意的变量名并制定对应的值，例如，我们需要定义一个名为color的变量并为每一台服务器设定这个变量的值。

```ini
[web]
quebec.example.com color=red
abc.example.com color=green
```

该变量就可以像其他变量一样在playbook中使用

就我个人来说，我并不经常针对主机设置变量，相应的，我经常针对群组设置组变量。

### 在群组中设置组变量

```ini
[all:vars]
ntp_server=ntp.ubuntu.com
[production:vars]
db_primary_host=rhodsisland.example
db_primary_post=5432
db_replica_host=virginia.example.com
db_name=widght_production
db_user=widgetuser
db_password=asdhSDdji8sd7SD
[ataging:vars]
...
```

需要注意的事，组变量通过**[group:vars]**关键字组成若干去区段，另外也要注意我们如何利用ansible自动创建的all群组来指定所有主机都要使用的到的变量。

## 在各自文件中的主机和组变量

如果你你所管理的主机不太多，将主机和组变量放到inventory文件中是合理的，但是当你的inventory文件越来越大的时候，仍然使用这种方式就会越来越难以管理变量。

此外，尽管ansible变量支持布尔类型，字符串，字典，列表，但是**在inventory文件中执行将变量指定为布尔类型或字符串类型**

ansible提供扩展性更好的方法来玩转主机和变量，可以为每台主机和每个群组创建独立的变量文件，ansible使用Yaml格式来解析这些变量文件。

ansible会在名为host_vars目录中寻找主机变量文件，在名为group_vars的目录中寻找组变量文件，**ansible假设这些目录这些目录与playbook文件平级或者和inventory文件平级**

举个例子：

如果我存放playbook的目录是/home/sath/playbook， inventory文件的路径是/home/sath/playbook/hosts， 那么我会将quebec.example.com主机的变量放在/home/sath/playbooks/host_vars/quebec.example.com文件中，而production的组变量会放在/home/sath/playbooks/group_vars/production文件中



/home/sath/playbooks/group_vars/production文件如下：

```ini
db_primary_host=rhodsisland.example
db_primary_post=5432
db_replica_host=virginia.example.com
db_name=widght_production
db_user=widgetuser
db_password=asdhSDdji8sd7SD
```

**注意：**我们也可以使用YAML字典来组织这些数据的值，如下

```ini
db:
  user: widgetuser
  password: asdhSDdji8sd7SD
  name: widght_production
  primary:
    host: rhodsisland.example
    port: 5432
  replica:
    host: virginia.example.com
    port: 5432
rabbitmq:
  host: pennsylvania.example.com
  port: 5672
```

如果使用YAML字典，那么访问变量的方式也要跟着进行改变

由

```shell
{{db_primary_user}}
```

改为

```shell
{{db.primary.user}}
```

如果你想更进一步进行拆分，ansible还允许将group_vars/production定义为一个目录，而不是一个文件，然后将个包含变量定义的YAML文件存放在这个目录中，例如我们可以将与数据库相关的变量放在一个文件中，而将与rabbitmq想关的文件放在另一个目录中，如下：

group_vars/produection/db

```ini
db:
  user: widgetuser
  password: asdhSDdji8sd7SD
  name: widght_production
  primary:
    host: rhodsisland.example
    port: 5432
  replica:
    host: virginia.example.com
    port: 5432
```

group_vars/produection/rabbitmq

```ini
rabbitmq:
  host: pennsylvania.example.com
  port: 5672
```

通常来说，将变量分割到太多文件会代理管理上的问题，保持配置足够简单才是更好的选择



## 动态inventory

到目前为止，我们已经在inventory文件中定义了所有的主机，但是， 你可能在使用ansible以外的某个系统来记录你得主机。你肯定不希望手动将这些信息复制一份到你的主机文件中，因为这些文件中的信息最终很难与真正管理你主机信息的外部系统保持一致，ansible支持动态的inventory功能可以帮助你避免复制这些信息。

如果inventory文件被标记为**可执行**，那么ansible会假设这是一个动态的inventory脚本，并且是要执行它而不是读取它。

### 动态inventory脚本接口

一个动态inventory脚本必须支持如下两个命令行参数

```shell
--host=<hostname>: 列出主机的详细信息
--list：列出群组
```

### 主机详细信息展示

ansible会按照如下形式调用inventory脚本来获取单台主机的详细信息

```shell
./dynamic.py --host=vagrant2
```

c输出应该包括主机特定的变量，也包括行为参数，类似下面这样：

```shell
{"ansible_ssh_host": 127.0.0.1, "ansible_ssh_port": 22, "ansible_ssh_user": root}
```

输出是一个名字为变量，值为变量值得json数据

### 列出群组

动态inventory脚本需要能够列出所有群组以及每台主机的详细信息，举例如下，

```shell
./dynamic.py --list
```

输出的结果应该类似下面这样

```json
{"production": ["a.example.com", "b.example.com"],
"staging": ["c.example.com", "d.example.com"],
"lb": ["e.example.com"],
"web": ["web.example.com"],
"task": ["task.example.com"]}
```

输出的一个json文件，该json对象的名字为群组名字，值为有群组内主机组成的数组

从优化角度来看，--list命令可以包含所有主机的变量值，这将会免去ansible挨个调用--host去获取每个主机的变量的工作。

想达到这个优化效果，--list命令应该返回一个名为_meta的键，值包括每台主机的变量，形式如下：

```shell
"_meta": {
"hostvars": [vagrant1: {
						"ansible_host": "127.0.0.1", "ansible_port": 22, "ansible_user": "root"
						vagrant2: {
						"ansible_host": "127.0.0.1", "ansible_port": 22, "ansible_user": "root"
}]
}
}
```





## 预装inventory脚本

可以使用ansible附带的那几个动态inventory脚本，如果不知道ansible安装在你电脑的哪一个位置，可以直接从github上[获取](https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/inventory/)

### 将inventory分割成多个文件

如果你想同时使用常规inventory文件和动态inventory文件，或者说动态和静态任意组合，只需要将所有这些文件放在同一个目录下并且配置ansible使用这个目录作为inventory即可，可以通过修改ansible.cfg文件中的inventory参数或者在命令行中使用-i都可以实现，ansible将会处理所有的文件并将结果合并为一个inventory

Ansible.cfg

```shell
inventory      = /etc/ansible/hosts
# 修改即可
```

### 使用add_host和group_by在运行是添加条目

ansible允许在执行playbook的时候向inventory中添加主机和群组

#### add_host

Add_host模块可以像inventory中添加主机，如果你在iaas云中使用ansible提供的新的虚拟机示例，这个模块会有用。

#### add_host和动态inventory有什么区别

如果在playbook执行的时候，创建一个新的主机，动态inventory脚本是没办法把这个新主机添加进来的，因为动态inventory是在playbook执行之前执行的，所以如果在playbook执行过程产生新主机，ansible是无法感知的，可以使用如下方式调用add_host模块：

```shell
add_host name=hostname group=web,staging myvar=myval
```

下面是一个add_host应用实例

```yaml
- name: add_host
  host: local
  vars:
       box: trusty64
  tasks:
  	- name: create new host
  	  command: vagrant init {{box}} creates=Vagrantfile
  	- name: bring up a new host
  		command: vagrant up
  	- name: add the vagent to inventory
  		add_host: >
  						name=vagrant
  						ansible_host=127.0.0.1
  						ansible_port=2222
  						ansible_user=vagrant
  						ansible_private_key_file=/user/sath/.vatgent.d/insecure_private_key
```

**add_host模块添加主机仅在playbook执行过程中生效，并不会修改你的inventory文件**

#### group_by

ansible也允许你在playbook执行的行首使用group_by模块来创建新分组，它允许你基于已经为每台主机自动设定好的变量的值来创建群组，ansible将这些变量叫做**fact**

如果ansible的fact gathering处于启用的状态，那么ansible会自动为主机设置一组变量，例如ansible_machine变量在32位机器上的值为i386，而在64位机器上值为x86_64，如果ansible同事管理这两种主机，我们就可以在task中创建i386和x86_64两个群组。

亦或我们想按照linux的发行版，来划分群组，就可以使用fact中的ansible_distribution变量

```yaml
- name: create groups based on linux distribution
	group_by: key={{ansible_distribution}}
```

# 变量与fact

在playbook中定义变量

```yaml
vars:
    host_file: /etc/nginx/ssl/nginx.key
    cert_file: /etc/nginx/ssl/nginx.crt
    conf_file: /etc/nginx/sites/default
    server_name: localhost
```

ansible也允许通过定义名为**vars_files**的区段把变量放到一个多个文件中，我把上面例子中的变量从playbook中挪出来放到名为nginx.yml的文件中，需要将vars改为vars_files，就想下面这样：

```yaml
vars_files:
    - nginx.yml
```

## 检查变量的值

为了便于调试，ansible可以很方便地查看变量的值，类似于debug

```yaml
- debug: var=myvarname
```

## registering变量

你会发现经常基于task执行的结果来设置变量的值，想要实现这个操作，我们以在调用模块的时候使用registering语句来创建registering变量，例如下面的实例，如何捕获whoami命令的输出到名为login的变量中



为了以后使用login变量，需要了解该变量的类型，使用register语句设置的变量总是被设置为字典类型，但是这个字典具体的键名是不同的，这取决与使用的模块。

不幸的是，ansible官方模块文档并没有包含每个模块返回值的信息，但是模块文档一般都包括register语句分范例，这些范例反倒更有帮助，我已经发现确认模块返回值最简单的方法就是设置一个register变量，然后使用debug模块输出这个变量

```yaml
- name: registering
  hosts: ubuntu
  tasks:
        - name: create output of whoami
          command: whoami
          register: login
        - debug: var=login
```

输出如下

```shell
PLAY [registering] ***********************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************
ok: [vm-ubuntu-1]

TASK [create output of whoami] ***********************************************************************************************************************************************
changed: [vm-ubuntu-1]

TASK [debug] *****************************************************************************************************************************************************************
ok: [vm-ubuntu-1] => {
    "login": {
        "changed": true, 
        "cmd": [
            "whoami"
        ], 
        "delta": "0:00:00.002622", 
        "end": "2019-09-15 11:06:40.152507", 
        "failed": false, 
        "rc": 0, 
        "start": "2019-09-15 11:06:40.149885", 
        "stderr": "", 
        "stderr_lines": [], 
        "stdout": "root", 
        "stdout_lines": [
            "root"
        ]
    }
}

PLAY RECAP *******************************************************************************************************************************************************************
vm-ubuntu-1                : ok=3    changed=1    unreachable=0    failed=0 
```



如果你想控制stdout的内容，可以在command模块中使用register语句

```yaml
- name: stdout
  hosts: ubuntu
  tasks:
      - name: in stdout
        command: whoami
        register: login
      - dubug: msg="logged in as user {{login.stdout}}"
```



### 引用字典变量的方法

```shell
{{login.stdout}}
{{login['stdout']}}
# 使用“.”或“[]”都可以
# 也可以混合使用
{{login['out'].stdout}}
```

## fact

之前我们就看到，当ansible运行playbook时，在开始执行第一个task时候有如下输出

```shell
[root@localhost 变量与fact]# ansible-playbook registering.yml 

PLAY [registering] ***********************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************
ok: [vm-ubuntu-1]
```



当ansible收集fact的时候，他会链接到主机收集各种详细信息，CPU架构，操作系统类型，IP地址，内存信息，磁盘信息等，这些信息保存在被称作fact的变量中，他与其他变量并没有什么区别。

下面这个playbook会打印每台服务器的操作系统信息

```yaml
- name: fact
  hosts: all
  gather_facts: True
  tasks:
        - debug: var=ansible_distribution
```

输出如下

```shell
PLAY [fact] ******************************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************
ok: [local-mac]
ok: [vm-ubuntu-1]
fatal: [vm-centos-1]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host 192.168.2.104 port 22: No route to host\r\n", "unreachable": true}
fatal: [vm-centos-2]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host 192.168.2.105 port 22: No route to host\r\n", "unreachable": true}
ok: [ali]

TASK [debug] *****************************************************************************************************************************************************************
ok: [ali] => {
    "ansible_distribution": "CentOS"
}
ok: [vm-ubuntu-1] => {
    "ansible_distribution": "Ubuntu"
}
ok: [local-mac] => {
    "ansible_distribution": "CentOS"
}
        to retry, use: --limit @/etc/ansible/playbooks/变量与fact/fact.retry

PLAY RECAP *******************************************************************************************************************************************************************
ali                        : ok=2    changed=0    unreachable=0    failed=0   
local-mac                  : ok=2    changed=0    unreachable=0    failed=0   
vm-centos-1                : ok=0    changed=0    unreachable=1    failed=0   
vm-centos-2                : ok=0    changed=0    unreachable=1    failed=0   
vm-ubuntu-1                : ok=2    changed=0    unreachable=0    failed=0
```

可以查阅ansible[官方文档](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variables-discovered-from-systems-facts)来获取fact列表，或者另外一个[更全面的版本](https://github.com/lorin/ansible-quickref/blob/master/facts.rst)

###查看与某台服务器关联的所有fact

ansible使用特殊模块setup来实现fact的收集，你不需要在playbook中调用这个模块，因为ansible会在收集fact是自动调用，不过，如果你想使用ansible命令行工具手动收集fact信息，可像像下面这样

```shell
ansible local -m setup
```

该模块返回的是一个字典，字典的键名是ansible_facts，而值仍是一个字典，他由实际fact的名字和对应的值组成

### 查看fact子集

由于ansible收集了非常多的fact，setup模块支持filter参数帮助通过通配符来对fact名进行过滤，例如

```shell
ansible local -m setup -a 'filter=ansible_default_ipv*'
```

输出

```shell
local-mac | SUCCESS => {
    "ansible_facts": {
        "ansible_default_ipv4": {
            "address": "192.168.2.108", 
            "alias": "enp0s3", 
            "broadcast": "192.168.2.255", 
            "gateway": "192.168.2.1", 
            "interface": "enp0s3", 
            "macaddress": "08:00:27:ff:23:0f", 
            "mtu": 1500, 
            "netmask": "255.255.255.0", 
            "network": "192.168.2.0", 
            "type": "ether"
        }, 
        "ansible_default_ipv6": {}
    }, 
    "changed": false
}
```

### 任何模块都可以返回fact

如果你仔细观察上面的输出，也可以看到输出的是一个键名为ansible_facts的字典，在返回值中使用ansible_facts字典是ansible的特定语法，如果模块返回一个字典且其中包括ansible_facts键，那么ansible会为主机自动创建相应的变量。

对于返回的fact模块，并不需要register变量，因为ansible会自动创建，举个例子, 直接使用ansible_facts中的键值对

```yaml
- name: get facts
  hosts: local
  tasks:
        - name: test
          command: whoami
        - debug: var=ansible_enp0s3.ipv4
```

删除如下

```shell
PLAY [get facts] *************************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************
ok: [local-mac]

TASK [test] ******************************************************************************************************************************************************************
changed: [local-mac]

TASK [debug] *****************************************************************************************************************************************************************
ok: [local-mac] => {
    "ansible_enp0s3.ipv4": {
        "address": "192.168.2.108", 
        "broadcast": "192.168.2.255", 
        "netmask": "255.255.255.0", 
        "network": "192.168.2.0"
    }
}

PLAY RECAP *******************************************************************************************************************************************************************
local-mac                  : ok=3    changed=1    unreachable=0    failed=0
```

### 本地fact

ansible还提供了另一个为某个主机设定fact的机制，还可以将一个或多个文件放置字目标主机的/etc/ansible/facts.d目录下，如果目录中的文件是以下形式

- ini
- json
- 可以直接不加参数直接运行的可执行文件，他的输出为标准的json格式

以这种形式加载的fact是键名为ansible_local的特殊变量

下面是一个实例

远端主机上的ansible_local文件

/etc/ansible/facts.d/exapmle.fact

```ini
[book]
title=ansible: up and running
author=SATH
publisher=beijing
```

playbook文件

```yaml
- name: local fact
  hosts: ali
  tasks:
        - name: all
          debug: var=ansible_local
        - name: title
          debug: msg="the title of book is {{ansible_local.example.book.title}}"
```

输出

```shell
PLAY [local fact] ************************************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************************
ok: [ali]

TASK [all] *******************************************************************************************************************************************************************
ok: [ali] => {
    "ansible_local": {
        "example": {
            "book": {
                "author": "SATH", 
                "publisher": "beijing", 
                "title": "ansible: up and running"
            }
        }
    }
}

TASK [title] *****************************************************************************************************************************************************************
ok: [ali] => {
    "msg": "the title of book is ansible: up and running"
}

PLAY RECAP *******************************************************************************************************************************************************************
ali                        : ok=3    changed=0    unreachable=0    failed=0  
```

**取值的方式就是字典的取值方式**

### 使用set_fact定义新变量

ansible还允许使用set_fact模块在task中设置fast（实际上与定义一个新变量一样），我们还是喜欢在register关键字后立即使用set_fact，这可让变量引用变得简单，下面的例子演示了如何利用set_fact使变量以snap引用，而不是更繁琐的snap_result.stdout

```yaml
- name: set_fact
  hosts: all
  tasks:
        - name: print
          command: whoami
          register: login
        - set_fact: sath={{login.start}}
        - debug: var=sath
```

### 内置变量

ansible定义了一些在playbook中永远有效的变量，下面是常用的一部分



### 在命令行设置变量





### 变量的优先级





# role

在ansible中, role是将playbook分割到多个文件的主要机制, 他大大简化了复杂playbook的编写, 同时, 他还使复用变得轻而易举, role可以看成你分配给一台或多台主机的配置与操作的集合

## role的文件构成

`roles/database/tasks/mian.yml`	**task文件**

`roles/database/files/`	**保存着需要上传到主机的文件**

`roles/database/templates/`	**保存jinja2模板文件**

`roles/database/handlers/main.yml`	**handler**

`/roles/database/vars/main.yml`	**不应被覆盖的变量**

`/roles/database/defaults/main.yml`	**可以被覆盖的默认变量**

`roles/database/meta/main.yml`	**role的从属信息**

每个文件都是可选的, 非强制, 如果你的role不包含handler, 并不需要准备空的`handlers/main.yml`文件



## ansible到哪里查找我的role

ansible将会到与你playbook并列的roles目录下找role, 他也会在`/etc/ansible/roles中查找系统级的role.

在ansible.cfg的defaults区段中,  通过roles_path的值来设置系统级role的位置

```ini
[defaults]
roles_path = ~/ansible_roles
```

也可以通过设置`ANSIBLE_REOLES_PATH`环境变量来覆盖这个设置

下面是一个示例

```yaml
- name: deploy
  host: web
  vars_file:
    - secrets.yml
  roles:
    - role: database
      database_name: "{{ mezzanine_proj_name}}"
      database_user: "{{ mezzanine_proj_user}}"
    - role: mezzanine
      live_hostname: 192.168.33.10.xip.io
      domains:
        - 192.168.33.10.xip.io
        - www.192.168.33.10.xip.io
```

`database_name`和`database_user`都是为database这个role定义的变量, 如果这些变量在role中被定义了, 那么不管是在`vars/main.yml`还是`vars/defaults/main.yml`已经声明了, 都会被覆盖

如果没有变量, 那么想下面这样直接声明role就行了

```yaml
- name: deploy
  host: web
  vars_file:
    - secrets.yml
  roles:
    - database
    - mezzanine
```



## 执行任务的前后

有时候你希望在调用你得role之前运行一些task, 比如在使用apt之前需要先更更新一些缓存, 并且在更新之后发送一个通知.

ansible把在role之前执行的一系列task定义为pre_task区段, 而在role之后执行的一系列task定义在post_task区段

下面是一个应用实例

```yaml
- name: deploy
  hosts: web
  vars_files:
    - secrets.yml
  pre_task:
    - name: update the apt cahce
      apt: update_cache=yes
  roles:
    - db
    - web
  post_task:
    - name: notify
      shell: echo "notify...."
```



## include语法

当task文件比较长时, 可以使用`include`语句把任务拆分都多个文件中

Main.yml

```yaml
- name: deploy
  hosts: web

- include: django.yml
- include: nginx.yml
```

Django.yml

```yaml
- name: create a logs directory
  file: path="{{ ansible_env.HOME }}/logs" state=directory
- name: check out the repository on the host
  git: repo={{ mezzanine_repo_url }} dest={{ mezzanine_proj_path }} accept_hostkey=yes
- name: install Python requirements globally via pip
  pip: name={{ item }} state=latest
  with_items:
    - pip
    - virtualenv
    - virtualenvwrapper
  become: True
```

Nginx.yml

```yaml
- name: set the nginx config file
  template: src=nginx.conf.j2 dest=/etc/nginx/sites-available/mezzanine.conf
  notify: restart nginx
  become: True
- name: enable the nginx config file
  file:
    src: /etc/nginx/sites-available/mezzanine.conf
    dest: /etc/nginx/sites-enabled/mezzanine.conf
    state: link
  notify: restart nginx
  become: True
```



## ansible-galaxy脚手架

```shell
ansible-galaxy init web
ansible-galaxy init roles/web
```

# 过滤器

过滤器是jinja2模板引擎的一个功能, 由于ansible除了使用jinja2作为模板引擎外, 还使用jinja2进行变量引擎, 所以除了模板之外, 你也可以在playbook中的`{{}}`内使用过滤器, 过滤器的用法有点像Unix的管道, 可以想象为变量像通过管道一样通过过滤器, jinja2还附带了一系列的内置过滤器, 初次之外ansible还附带了自己的过滤器来扩展jinja2的过滤器

*写过django的同学会感觉很亲切*

## 默认过滤器

default过滤器非常有用, 以下是一个简单的例子

```yml
- name: 过滤器
  hosts: web-1
  gather_facts: False
  tasks:
    - name: 这是一个任务
      file:
        name: "{{ filename | default('默认文件名')}}"
        state: touch
```

当`filename`这个变量不存在是, 则使用`default`里的

```shell
SATH-MacBook-Pro:playbook mac$ ansible-playbook filter.yml
```

当`filename`这个变量存在时, 就直接使用

```shell
SATH-MacBook-Pro:playbook mac$ ansible-playbook filter.yml -e filename=指定好的
```

## 自定义过滤器

ansible会在存放playbook的同级的filter_plugins目录下查找自定义的过滤器

也可以将过滤器插件放置在`~/.ansible/plugins/filter`目录或`/usr/share/ansible/plugins/filter`目录下, 或者通过`ANSIBLE_FILTER_PLUGINS`环境变量设置为插件所在的目录来指定过滤器的目录

自定义的过滤器

```python
# -*- coding: utf-8 -*-
"""
@Time: 2020年04月27日 22时42分
@Desc:
"""


def name_upper(name: str):
    print(name)
    return name.upper()


class FilterModule:

    @staticmethod
    def filters():
        return {"name_upper": name_upper}

```

playbook

```yml
- name: 自定义filter
  hosts: web-1
  gather_facts: False
  tasks:
    - name: 使用自定义的filter
      file:
        name: "{{ name | default('toy') | name_upper() }}"
        state: touch
```



# lookup





# 在控制主机上执行任务





# 在涉及到的主机以外的机器上执行task

delegate_to



# 逐台执行

```yml
serial: 1
```

# 一次运行一批

```yml
serial: 50%
```

# 只执行一次

```yml
- name: run
  command: /opt/migrate
  run_once: True
```

# 运行策略

