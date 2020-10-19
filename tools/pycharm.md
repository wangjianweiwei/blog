![image](https://user-images.githubusercontent.com/41533289/95804494-668ee280-0d35-11eb-8fa1-2acfba1f2beb.png)
父类中`run_simple`
```python
@classmethod
@orm_context
def run_simple(cls, UVID, **kwargs):
    version = Abc.get(UVID=UVID)  # type: Abc
    task = Def.get(resource_id=version.id)
    with cls(task_id=task.id) as obj:
        return obj
```

现在子类中想要覆盖`run_simple`这个方法， 并且会在原来的基础上增加一个或多个参数，
```python
@classmethod
def run_simple(cls, UVID, episode, **kwargs):
    version = Abc.get(UVID=UVID)  # type: Abc
    task = Def.get(resource_id=version.id)
    with cls(task_id=task.id, episode=episode) as obj:
        return obj
```

通过上面的图片看出，pycharm给出了警告， 原因是违反了**LSP原则（在使用父类的场景下，替换为子类也要可行）**， 也就是说在有些场景下使用了父类的`run_simple`但是并不知道有`episode`这个参数， 加入有一天换成子类中的`run_simple`，此时不传递`episode`参数就不能够能正常运行。

解决这个问题的本质就是保证父类和子类之间可能完美的切换。**具体的代码改动就只需要在子类的`run_simple`中给`episode`添加默认参数即可。**
