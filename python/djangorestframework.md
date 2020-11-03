## 有用的配置
### 全局时间格式
```python
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%d %X',
}
```
官方提供了以下几种关于时间格式的配置
```python
# Input and output formats
REST_FRAMEWORK = {
'DATE_FORMAT': "ISO_8601",
'DATE_INPUT_FORMATS': ["ISO_8601"],

'DATETIME_FORMAT': "ISO_8601",
'DATETIME_INPUT_FORMATS': ["ISO_8601"],

'TIME_FORMAT': "ISO_8601",
'TIME_INPUT_FORMATS': ["ISO_8601"],
}
```

