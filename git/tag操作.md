## 创建tag

```shell
git tag {标签名称}
```

## 查看所有tag

```shell
git tag
```

默认标签是打在最新提交的commit上的。有时候，如果忘了打标签，比如，现在已经是周五了，但应该在周一打的标签没有打，怎么办？

方法是找到历史提交的commit id，然后打上就可以了：

```shell
git log --pretty=oneline --abbrev-commit

ab9141d (HEAD -> master, tag: V1.1, origin/master) add main.py
f04fd2f init

```

比方说要对`init`这次提交打标签，它对应的commit id是`f04fd2f`，敲入命令：

```shell
git tag V1.1 f04fd2f
```

查看tag

```shell
git tag
V1.1
```

查看标签是显示的顺序不是按照时间的顺序, 而是按照字母的顺序显示

**查看某个tag的详细信息**

```shell
$ git show V1.1
tag V1.1
Tagger: sath <59410@qq.com>
Date:   Tue Aug 20 21:55:53 2019 +0800

this is v1.1

commit ab9141df6056b70a6b839866ee2ebcea4c703deb (HEAD -> master, tag: V1.1, origin/master)
Author: sath <59410@qq.com>
Date:   Tue Aug 20 21:51:35 2019 +0800

    add main.py

diff --git a/main.py b/main.py
new file mode 100644
index 0000000..7f63695
--- /dev/null
+++ b/main.py
@@ -0,0 +1 @@
+print("Hello,World")
```

**创建基于某个tag的分支**

```shell
git  checkout -b tag_test week-two
```



**创建tag说明**

```shell
git tag -a V1.0 -m "version 1.0 released" f04fd2f
```

## 删除tag

如果tag打错了,也是可以删除的.

```shell
git tag -d V1.0
```

因为创建的tag都是存储在本地的, 不会自动推送到远端,所以, 打错的tag可以在本地安全的删除.

如果tag已经推送到了远端, 要想删除的话,也是可以的.

先删除本地的tag

```shell
git tag -d v1.0
```

再删除远端的

```shell
git push origin :refs/tags/{要删除的tag}
```

## 推送tag到远端仓库

如果要将某个tag推送到远端使用下面的命令

```shell
git push origin {本地存在的tag}
```

或者一次性将本地的所有tag都推送到远端.

```shell
git push origin --tags
```

