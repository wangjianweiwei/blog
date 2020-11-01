## os.dup2
os.dup2() 方法用于将一个文件描述符 fd 复制到另一个 fd2。
Unix, Windows 上可用。

### 语法
`os.dup2(fd, fd2)`
- fd 要被复制的文件描述符
- fd2 复制的文件描述符

### 示例
```python
import os

w = open("./123.log", mode="a")
fd = w.fileno()
fd2 = 1000

os.dup2(fd, fd2)
# 在fd2上写
os.write(fd2, b"123")
# 在df上就可以读出来
os.lseek(fd, 0, 0)
os.read(fd, 100)
```
