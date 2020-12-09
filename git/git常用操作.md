# 配置操作
## 查看当前仓库的配置
```shell script
git config  -l
```

## 设置邮箱姓名
```shell script
git config user.name "wangjianwei"
git config user.email "594504110@qq.com"
```

# 基本操作
## 初始化工作目录

```shell
git init
```

## 查看工作目录中的文件状态

```shell
git status
```

## 对文件进行追踪

```shell
git add .	# 追踪所有的文件
git add README.md	# 追踪指定的文件
```

## 提交暂存区的文件提交到本地仓库

```shell
git commit -m "对本次操作的描述"
```

## 指定忽略的文件

```shell
初始化版本库

git init

创建版本库过滤文件
touch .gitignore

向.gitignore文件中写入以下内容，过滤env目录，python的编译文件:

cat .gitignore
env/
*.pyc
```

## 指定远程仓库

```shell
git remote add origin https://github.com/594504110/hello.git
```

## 将本地仓库推送到远程仓库

```shell
git push -u origin master
```

## 查看更新记录

```shell
git log
git log --oneline    一行显示git记录
git log --oneline  --all  一行显示所有分支git记录
git log --oneline --all -4 --graph 显示所有分支的版本演进的最近4条
git log -4  显示最近4条记录
git log --all     显示所有分支的commit信息
```

## 版本回退到过去

```shell
git log可以查看历史版本记录
git reset --hard命令可以回退版本
git reset --hard HEAD^ 回退到上个版本
HEAD表示当前版版本
HEAD^表示上个版本
HEAD^^上上个版本

也可以直接git reset --hard 版本id号
```

## 版本回退到未来

```shell
git reflog	# 可以查看所有版本id
git reset --hard id	# 即可回退
```

## 撤销还未提交到暂存区中的修改

```shell
# 当对某个文件进行了修改, 并且保存了, 此时查看git status的状态为modified
git checkout -- README.md	# 撤销暂存区中的修改
```

## 撤销已经提交到暂存区中的修改

```shell
# 对应经执行了git add的修改进行撤回
# 先撤销暂存区中的修改
git reset HEAD README.md
# 在撤销修改记录
git checkout -- README.md
```

## 删除文件与恢复文件

```shell
# 如果直接在工作区删除文件, 这个动作会被git记录
rm -rf README.md	# 虽然删除了工作区的文件, 但是git仓库中还有记录
# 如果删除的文件确定是无用的, 那么既可以commit到本地仓库中
git commit -m "rm README.md"

# 如果想恢复文件, 可以使用本地仓库中的文件替换工作区的文件
git checkout -- README.md
```

## 对文件进行重命名

```shell
git mv README.md test.md
git commit -m 'mv README.md'
```

## 分支操作

```shell
git branch 分支名	# 创建分支
git checkout 分支名	# 切换分支
git branch	# 查看所有的分支, 当前所在的分支会使用*标记
git check --filename	# 一键还原文件, 用本地仓库中文件覆盖工作区的文件
git checkout -b 分支名	# 创建分支并切换到该分支
```

## 多分支开发冲突

```shell
# 创建分支, 提交代码
git checkout master
echo "master" >> README.md
git commit -a -m "#echo master"

git checkout python
echo "python" >> README.md
git commit -a -m "#echo python"

# 此时在切到master上发现python echo的内容并没有出现在master分支的文件中, 此时就需要git marge
git marge pyhton	# 和python分支进行合并
# 此时会报一个错误
Automatic merge failed; fix conflicts and then commit the result.	# 自动合并失败；修复冲突，然后提交结果。
# 这时就需要我们手动解决冲突, 在README.md文件中手动删除冲突的部分, 保留需要的部分, 然后在进行commit
```

## 查看分支合并图

```
git log --graph
```

# 分支

## 列出本地分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git branch --list
  develop
* feature/login-api
  master
```

## 列出所有分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git branch --all
  develop
* feature/login-api
  master
  remotes/origin/develop
  remotes/origin/feature/login
  remotes/origin/feature/login-api
  remotes/origin/master

```

## 列出远程分支

这个命令将会给你一个仅包含远程分支的列表(使用这些分支的真实名称)，如下所示。

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git branch --remote
  origin/develop
  origin/feature/login
  origin/feature/login-api
  origin/master

```

## 更新远程分支列表

远程分支列表不会自动更新, 因此这个列表将会随着时间而落后, 使用fetch命令更新这个列表

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git fetch
remote: Counting objects: 1, done.
remote: Total 1 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (1/1), done.
From 39.106.15.4:wangjianwei/git_home
   0c249d7..9ebd1ea  develop    -> origin/develop
```

# 使用不同的分支

## 切换分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout --track origin/develop
Branch 'develop' set up to track remote branch 'develop' from 'origin'.
Switched to a new branch 'develop'
```

或者使用下面的方式

```shell
git checkout --track -b video-lessons origin/video-lessons
```

这个命令(checkout -b)启用了跟踪(--track)，从远程仓库origin中存储的video- lessons 分支上，创建了一个名为 video-lessons 的新分支。这个远程分支的本地副本可以 通过 origin/video-lessons 访问到，而你自己的分支副本可以通过 video-lessons 访问到。

*你现在应该已经有了远程分支 video-lesson 的一份本地副本*

## 创建新分支

首先签出你希望作为起点使用的分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout master
Switched to branch 'master'
Your branch is up to date with 'origin/master'.
```

然后创建一个新的分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git branch 1-process_notes
```

接着签出刚刚创建的新分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout 1-process_notes
Switched to branch '1-process_notes'
```

## 在仓库中添加更改

![image-20191121225303509](/Users/mac/wangjianwei/document/Summary/git常用操作.assets/image-20191121225303509.png)

*git中的更改必须先进行暂存, 然后再保存到仓库中*

## 将修改保存到暂存区

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git add --all
```

*将该仓库下所有的改动都添加到暂存区, 包括新加的或更新的*

当你同时进行一些不相关的编辑, 并且想将这些修改放置在不通过的提交中, 这是一个很好的想法, 这时就不能使用`--all`参数, 你需要价将`--all`替换成你想要暂存的文件名, 你可以同时添加一个或多个文件名, 

**文件名支持模糊匹配和递归添加**

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git add *.txt
```

还可以只add那些已经在git暂存区或仓库中存在的文件, 通过`--update`参数来控制

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git add --update
```

## 从暂存区中移除文件

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git reset HEAD b.txt 
```

# commit管理

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git commit

(venv) SATH-MacBook-Pro:git_home mac$ git commit -m "fix"
[1-process_notes 3f33973] fix
 1 file changed, 3 insertions(+)
 create mode 100644 c.json

(venv) SATH-MacBook-Pro:git_home mac$ git commit --amend
```

# 忽略文件

1. 在项目根目录创建一个名为 .gitignore 的文件。
2. 每行一个文件名，写上所有你一定不希望 Git 添加到仓库中的文件。你可以使用确切的文件名或通配符(如 *.swp)。
3. 使用 add 和 commit 命令将 .gitignore 文件添加到你的仓库。

*包含以上扩展名的文件将永远不会被添加至你的仓库，即使你使用了 --all 参数。*

# 标签

标签只能添加到指定的提交.

**查看提交的记录**

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git log --oneline
4f17c20 (HEAD -> 1-process_notes) fix: 修复了一个重大的bug
d3b179f feat: 暂存区测试
570adbd (origin/master, master) Initial commit
```

查看某个节点以及之前的提交

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git log --oneline
4f17c20 (HEAD -> 1-process_notes) fix: 修复了一个重大的bug
d3b179f feat: 暂存区测试
570adbd (origin/master, master) Initial commit

(venv) SATH-MacBook-Pro:git_home mac$ git log d3b179f
commit d3b179f1f8c87d9c3d0d5c2a0c3671d88bf47f94
Author: wangjianwei <wangjianwei@haimaqingfan.com>
Date:   Thu Nov 21 23:09:39 2019 +0800

    feat: 暂存区测试

commit 570adbd6c35d85f71ac3d7d0c51eed5f844b1f12 (origin/master, master)
Author: wangjianwei <wangjianwei@haimaqingfan.com>
Date:   Wed Nov 20 23:40:11 2019 +0800

    Initial commit

```

查看某次提交的详细信息

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git show 4f17c20
commit 4f17c20c8dcc97cc06f46a0cec93c2af92c0397d (HEAD -> 1-process_notes)
Author: wangjianwei <wangjianwei@haimaqingfan.com>
Date:   Sat Nov 23 16:16:20 2019 +0800

    fix: 修复了一个重大的bug

diff --git a/c.json b/c.json
new file mode 100644
index 0000000..a41fbfc
--- /dev/null
+++ b/c.json
@@ -0,0 +1,3 @@
+{
+  "name": "叶子"
+}
\ No newline at end of file
```

*正如你之前所见，show 命令将会显示该提交的日志消息和文本 diff。*

# 标签操作

## 添加新标签

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git log --oneline
4f17c20 (HEAD -> 1-process_notes) fix: 修复了一个重大的bug
d3b179f feat: 暂存区测试
570adbd (origin/master, master) Initial commit

(venv) SATH-MacBook-Pro:git_home mac$ git tag v0.0.1 4f17c20
```

## 查看所有的标签

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git tag
v0.0.1
```

## 查看标签的详细信息

和`git show 4f17c20`的输出一样

正如你之前所见，show 命令将会显示该提交的日志消息和文本 diff。

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git show v0.0.1
commit 4f17c20c8dcc97cc06f46a0cec93c2af92c0397d (HEAD -> 1-process_notes, tag: v0.0.1)
Author: wangjianwei <wangjianwei@haimaqingfan.com>
Date:   Sat Nov 23 16:16:20 2019 +0800

    fix: 修复了一个重大的bug

diff --git a/c.json b/c.json
new file mode 100644
index 0000000..a41fbfc
--- /dev/null
+++ b/c.json
@@ -0,0 +1,3 @@
+{
+  "name": "叶子"
+}
\ No newline at end of file
```

# 远程仓库操作

## 添加远程仓库链接

```shell
git remote add origin git@39.106.15.4:wangjianwei/git_home.git
```

*origin只是一个别名而已, 你可以用任何你喜欢的东西命名*

## 推送更改

为了上传你得更改, 你可能需要下面几个东西

1. 远程仓库的链接
2. 可以发布到仓库的权限
3. 要想上传修改的分支名

你会想到用下面的命令将本地分更改推送到远端

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git push
```

但是你可能会得到下面的提示

```shell
fatal: The current branch 1-process_notes has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin 1-process_notes
```

这条错误消息为我们提供了非常有用的信息，但可能并不完全正确。与其说是将你的分支 上传到远程仓库 *origin*，不如说我们事实上想要使用新的远程仓库 git_home*。

### 在上传本地分支时设置上游分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git push --set-upstream origin 1-process_notes
Total 0 (delta 0), reused 0 (delta 0)
To 39.106.15.4:wangjianwei/git_home.git
 * [new branch]      1-process_notes -> 1-process_notes
Branch '1-process_notes' set up to track remote branch '1-process_notes' from 'origin'.

```

# 分支维护

一旦代码经过了测试, 你就希望将这个工单分支并入master分支, 并删除本地分支和这个工单分支的远程副本, 在单人团队中, 你不太可能需要处理合并冲突.

## 将工单分支并入你的主分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout master
Switched to branch 'master'
Your branch is up to date with 'origin/master'.

(venv) SATH-MacBook-Pro:git_home mac$ git merge 1-process_notes
Updating 570adbd..68a10ce
Fast-forward
 .gitignore | 127 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 a.txt      |   0
 b.txt      |   0
 c.json     |   3 +++
 d.c        |   1 +
 5 files changed, 131 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 a.txt
 create mode 100644 b.txt
 create mode 100644 c.json
 create mode 100644 d.c
```

## 将master推送到远程仓库

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git push

Total 0 (delta 0), reused 0 (delta 0)
To 39.106.15.4:wangjianwei/git_home.git
   570adbd..68a10ce  master -> master
```

## 删除本地分支

现在修改已经并入远程仓库, 本地仓库的分支就可以删除了. 这样可以保证本地仓库的整洁.

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git branch -d  1-process_notes
Deleted branch 1-process_notes (was 68a10ce).
```

## 删除远程分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git push --delete origin 1-process_notes
To 39.106.15.4:wangjianwei/git_home.git
 - [deleted]         1-process_notes
```

# 变基

[推荐文章](https://blog.csdn.net/fly_zxy/article/details/82586861)

## 什么是变基

使用rebase命令将提交到某一分支上的所有修改都移至另一分支上，就好像“重新播放”一样(**将一个分支的修改操作在另一个分支最新的提交基础上在依次应用**)。

## 变基的目的

一般我们这样做的目的是为了确保在向远程分支推送时能保持提交历史的整洁——例如向某个其他人维护的项目贡献代码时。 在这种情况下，你首先在自己的分支里进行开发，当开发完成时你需要先将你的代码变基到 origin/master 上，然后再向主项目提交修改。 这样的话，该项目的维护者就不再需要进行整合工作，只需要快进合并便可


切到要进行rebase的分支

```shell
git checkout wang
```

将wang分支变基到master分支上

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git rebase master
First, rewinding head to replay your work on top of it...
Applying: feat: commit 10
Applying: feat: commit 11

```

*注意: 保持master分支是最新的代码, 在master和wang两个分支没有冲突的情况下, 会很顺利.* 

## 当在变基时遇到冲突

当进行变基时, 输出下面的内容, 就以为了, 遇到了冲突

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git rebase master
First, rewinding head to replay your work on top of it...
Applying: feat/wang: commit 13
Using index info to reconstruct a base tree...
M       a.txt
Falling back to patching base and 3-way merge...
Auto-merging a.txt
CONFLICT (content): Merge conflict in a.txt
error: Failed to merge in the changes.
Patch failed at 0001 feat/wang: commit 13
hint: Use 'git am --show-current-patch' to see the failed patch
Resolve all conflicts manually, mark them as resolved with
"git add/rm <conflicted_files>", then run "git rebase --continue".
You can instead skip this commit: run "git rebase --skip".
To abort and get back to the state before "git rebase", run "git rebase --abort".
```

从上面的提示中可以看出:

1. 在进行`feat/wang: commit 13`时合并失败, 出现冲突
2. 如果解决了冲突, 使用`git add`然后使用`git rebase --continue`继续下一个commit节点的变基
3. 使用`git rebase --skip`跳过这个commit节点的冲突
4. 当遇到解决不了, 或者搞乱的情况下可以使用`git rebase --abort`, 使代码回到`git rebase`之前的样子

切回master, 将wang分支合并到master分支

合并前的log

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git log --oneline
7b07c5c (HEAD -> master) feat: 叶子家在广平县刘董村
2f48f4c feat: 叶子体重110
3b3a117 (origin/master) feat: commit 9
03b768a feat: commit 8
0a2a557 feat: 叶子身高160
fa25f41 feat: 叶子今年22了
ac77cce feat: commit 7
2360ab5 feat: commit 6
2ad22d4 feat: commit 5
3943d1a feat:commit 4
ca558ce 冲突合并
86bf35d feat:commit 3
985be69 feat:commit 2
1f017bf feat:commit 1
8a1c222 feat:wang在a.txt中写了一句话
701c890 feat:master在a.txt中写了一句话
68a10ce feat:写了一段c
4f17c20 (tag: v0.0.1, origin/wang) fix: 修复了一个重大的bug
d3b179f feat: 暂存区测试
570adbd Initial commit
```



```shell
(venv) SATH-MacBook-Pro:git_home mac$ git merge wang
Updating 7b07c5c..4a134aa
Fast-forward
 a.txt | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)
```

合并后的log

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git log --oneline
4a134aa (HEAD -> master, wang) feat: commit 11
6084cd5 feat: commit 10
7b07c5c feat: 叶子家在广平县刘董村
2f48f4c feat: 叶子体重110
3b3a117 (origin/master) feat: commit 9
03b768a feat: commit 8
0a2a557 feat: 叶子身高160
fa25f41 feat: 叶子今年22了
ac77cce feat: commit 7
2360ab5 feat: commit 6
2ad22d4 feat: commit 5
3943d1a feat:commit 4
ca558ce 冲突合并
86bf35d feat:commit 3
985be69 feat:commit 2
1f017bf feat:commit 1
8a1c222 feat:wang在a.txt中写了一句话
701c890 feat:master在a.txt中写了一句话
68a10ce feat:写了一段c
4f17c20 (tag: v0.0.1, origin/wang) fix: 修复了一个重大的bug
d3b179f feat: 暂存区测试
570adbd Initial commit
```

可以看到刚刚在wang分支提交的节点, 通过变基的方式, 都放到了master的最顶端

# 回滚



# 撤销

## 未暂存

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout -- a.txt
```

## 已经暂存

操作步骤

1. 取消暂存
2. 恢复被删除的文件

先使用 reset 命令在恢复文件之前将它取消暂存

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git status
On branch master
Your branch is ahead of 'origin/master' by 10 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        deleted:    a.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        a/
        e.pdf
```

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git reset HEAD a.txt
Unstaged changes after reset:
D       a.txt
```

一旦文件被取消暂存后，你可以像之前使用 checkout 命令那样恢复被删除的文件

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout -- a.txt
```



# 重置



# log

## log和reflog

log

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git log
commit 3d274127a5a0e80ee502ee334ab9cd9f28495962 (HEAD -> master, wang)
Author: wangjianwei <wangjianwei@haimaqingfan.com>
Date:   Sun Nov 24 13:34:58 2019 +0800

    feat/wang: commit 14

commit 507a3f72fc03e66ff6ca70a7a5f2c1e42105954a
Author: wangjianwei <wangjianwei@haimaqingfan.com>
Date:   Sun Nov 24 13:34:46 2019 +0800

    feat/wang: commit 13
```

reflog

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git reflog
3d27412 (HEAD -> master, wang) HEAD@{0}: checkout: moving from 570adbd6c35d85f71ac3d7d0c51eed5f844b1f12 to master
570adbd HEAD@{1}: checkout: moving from master to 570adbd
3d27412 (HEAD -> master, wang) HEAD@{2}: merge wang: Fast-forward
7877f97 HEAD@{3}: checkout: moving from wang to master
3d27412 (HEAD -> master, wang) HEAD@{4}: rebase finished: returning to refs/heads/wang
3d27412 (HEAD -> master, wang) HEAD@{5}: rebase: feat/wang: commit 14
507a3f7 HEAD@{6}: rebase: feat/wang: commit 13
7877f97 HEAD@{7}: rebase: checkout master
ebf9e50 HEAD@{8}: commit: feat/wang: commit 14
d7277d7 HEAD@{9}: commit: feat/wang: commit 13
4a134aa HEAD@{10}: checkout: moving from master to wang
7877f97 HEAD@{11}: commit: feat/master: commit 12
09c9da7 HEAD@{12}: commit: feat/master: commit 11
4a134aa HEAD@{13}: merge wang: Fast-forward
7b07c5c HEAD@{14}: checkout: moving from wang to master
4a134aa HEAD@{15}: rebase finished: returning to refs/heads/wang
4a134aa HEAD@{16}: rebase: feat: commit 11
6084cd5 HEAD@{17}: rebase: feat: commit 10
7b07c5c HEAD@{18}: rebase: checkout master
f41b766 HEAD@{19}: checkout: moving from master to wang
7b07c5c HEAD@{20}: commit: feat: 叶子家在广平县刘董村
2f48f4c HEAD@{21}: commit: feat: 叶子体重110
3b3a117 (origin/master) HEAD@{22}: checkout: moving from wang to master
f41b766 HEAD@{23}: commit: feat: commit 11
a20bacd HEAD@{24}: commit: feat: commit 10
3b3a117 (origin/master) HEAD@{25}: checkout: moving from logout to wang
454911f HEAD@{26}: commit: feat: 增加注销接口
9ebd1ea (develop) HEAD@{27}: checkout: moving from develop to logout
9ebd1ea (develop) HEAD@{28}: checkout: moving from master to develop
3b3a117 (origin/master) HEAD@{29}: merge wang: Fast-forward
0a2a557 HEAD@{30}: checkout: moving from wang to master
3b3a117 (origin/master) HEAD@{31}: rebase finished: returning to refs/heads/wang
3b3a117 (origin/master) HEAD@{32}: rebase: feat: commit 9
03b768a HEAD@{33}: rebase: feat: commit 8
0a2a557 HEAD@{34}: rebase: checkout master
f14d231 HEAD@{35}: checkout: moving from master to wang
```

这个历史记录是私有的。只有你可以看到它!它包含你所做的所有事，包括那 些并不影响代码的事情，比如签出一个分支。都会被记录下来.

**log 和 reflog 这两个命令都会显示仓库中某个状态的提交 ID。只要你找到了提交 ID，你 就可以签出这个提交，及时将代码库的版本临时恢复到那个节点。**

随便选择一个commit ID进行签出

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout 03b768a
Note: checking out '03b768a'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 03b768a feat: commit 8
```

签出后查看当前所在的分支

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git branch
* (HEAD detached at 03b768a)
  develop
  feature/login-api
  master
  wang
```

当前的这个分支, 就是头指针处于分离的状态, 只是将HEAD指向了你签出的那个commit节点, 如果你希望保存当前的状态, 是可以使用下面的方式签出一个真实的分支.

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git checkout -b 签出的commit8分支
Switched to a new branch '签出的commit8分支'
```

# 修补提交

如果你在add或commit之后又对文件进行了修改, 那么你可能需要先进行add, 然后再cmmit, 但是,如果你只是想修改commit为, 那么你可能跳过add和commit, 直接使用下面的命令.

```shell
(venv) SATH-MacBook-Pro:git_home mac$ git commit --amend
```

*你的新变更将会被添加到之前的提交，并且 Git 会为这个修改过的提交对象分配一个新的 ID。*

# 使用reset合并提交

**对 reset 作用最基本的解释是，它其实只是修改了头指针的指向。 不管你用手指着哪个提交，Git 都会把它当作你的分支当前的 HEAD(或顶端)**

**reset 会改变你已记录的历史记录**

reset 将会改变你的历史记录，因为它移除了指向提交的引用。如果有人试 图合并他们旧版本的分支，他们将会重新引入你尝试移除的提交。因此，最好只在尚未与他人共享的分支上使用 reset 来改变分支历史记录(也就是说 你本地创建的分支，且你尚未将它推送到服务器)。

# 使用rebse合并commit

使用`git rebase HEAD~3`合并最新的3个commit

或者指定commit ID

`git rebase -i 3b4246`合并`3b4246`之后的commit 你可进行从后面的commitID中选择性合并

然后修改多个commit的msg

如果只是本地的commit合并, 到这里就已经结束了

但是如果你要合并的已经推送到远端仓库时, 就不能直接push了, 需要加`-f`参数, 强制覆盖
