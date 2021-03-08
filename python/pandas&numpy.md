## 调整Dataframe的列顺序

```python
import pandas as pd

data = [{"name": "zhangsan", "age": 18, "address": "北京"},
        {"name": "李四", "age": 20, "address": "上海"},
        {"name": "toy", "age": 24, "address": "太阳宫"}
        ]

df = pd.DataFrame(data)
print(df.columns)
df = df[["age", "address", "name"]]
print(df.columns)
```

## 将多个Dataframe输出到同一个excel的不同sheet中

```python
import pandas as pd

writer = pd.ExcelWriter('result.xlsx', engine='openpyxl')
for i, path in enumerate(["1.json", "2.json"], 1):
    df = pd.read_json(path)
    df.to_excel(excel_writer=writer, sheet_name=str(i), encoding="utf-8", index=False)

writer.save()
```
