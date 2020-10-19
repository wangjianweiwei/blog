# if判断
## if-then
其他编程语言中if后面应该是一个等式, 但是bash shell的if并不是。
bash shell的if语句会运行if后面的那个命令, 如果该命令的退出码是0, 位于then部分的代码就会被执行, 如果该命令的退出状态码是其他值, then部分的命令就不会被执行。
```bash
#!/bin/bash

# 写法一
if pwd
then
  echo "It worker"
fi

# 写法二
if pwd; then
  echo "It worker"
fi
```
在then中, 你可以使用不止一条命令, 可以像在脚本的其他位置一样在这里列出多条命令, bash shell会将这些命令当成一个块.
如果if语句行的命令的退出状态为0, 所有命令都会被执行, 如果if语句行的命令退出状态不为0, 则所有的命令都会被跳过
```bash
#!/bin/bash


user=mac

if grep $user /etc/passwd; then
  echo "this is my first command"
  echo "this is my sceond command"
  echo "I can even put in other command"
  ls -a /Users/$user/.bash*
fi
```

## if-then-else
```bash
#!/bin/bash


user=mac1

if grep $user /etc/passwd; then
  echo "This user exists"
else
  echo "This user does not exist"
fi
```
## if的其他用法
- 还支持if嵌套
```bash
#!/bin/bash

user=mac1

if grep $user /etc/passwd; then
  if pwd; then
    echo "OK"
  else
    echo "NO"
  fi
else
  echo "This user does not exist"
fi
```
- elif
```bash
#!/bin/bash

user=mac1

if grep $user /etc/passwd; then
  echo "This user exists"
elif grep $user /etc/haha; then
  echo "这个用户在这里"
else
  echo "This user does not exist"
fi
```
## test命令
到目前为止, 在if语句中看到的都是普通的shell命令, 可能会有疑惑, if-then语句能够测试命令退出码之外的条件吗?
答案是: **NO, 不可以**
但是在bash中有一个工具可以帮助我们通过if-then语句测试其他的条件
 test命令提供了在`if-then`语句中测试不同条件的途径, 如果`test`命令中列出的条件成立,`test`命令就会退出并返回退出状态码0, 如果条件不成立就返回非零的退出状态码, 这样`if-then`就和其他编程语言比较像了
**语法格式**
```bash
if test condition; then
  commands
fi
```
如果`test`后面没有表达式, 他会以非零的退出码退出, 并执行`else`语句块
```bash
if test; then
  echo "OK"
else
  echo "NO"
fi
```
用法如下
```bash
#!/bin/bash

my_var="Full"

if test $my_var
then
  echo "The $my_variable expression returns a True"
else
  echo "The $my_variable expression returns a False"
fi
```
如果把`my_var`改为`my_var=""`就意味着条件为`False`， 也就会执行`else`中的语句

bash还提供了另外一种(条件测试)test的写法，无需在if-then中声明test命令
```bash
#!/bin/bash

my_var="Full"

if [ $my_var ]; then
  echo "The $my_variable expression returns a True"
else
  echo "The $my_variable expression returns a False"
fi
```
**注意：在`[]`的前后都要有一个空格**

test命令可以判断三种条件
- 数字比较
- 字符串比较
- 文件比较
### 数值比较
```bash
#!/bin/bash

var1=10

if [ $var1 -gt 5 ]; then
  echo "大于 $var1 "
else
  echo "小于 $var1"
fi
```
常用的比较方法
- n1 -eq n2 相等
- n1 -ge n2 大于等于
- n1 -gt n2 大于
- n1 -le n2 小于等于
- n1 -lt n2 小于
- n1 -ne n2 不等于
**在测试条件中不能使用浮点数**

### 字符串比较
```bash
#!/bin/bash

user1=mac

if [ "$user1" == "$USER" ]; then
  echo "ok"
else
  echo "no"
fi
```
常用的字符串比较方法
- str1 = str2 # 是否相等
- str1 != str2  # 是否不同
- str1 < str2 # str1是否比str2小
- str1 > str2 # str1是否比str2大
- -n str1 # str1长度是否非0
- -z str1 # str1长度是否为0
