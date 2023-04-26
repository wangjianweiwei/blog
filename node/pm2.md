### pm2 通过package.json中的script启动项目

启动命令
`pm2 start npm --watch --name cooperation_snapshot -- run start:prod`

package.json

```json
{
  "name": "cooperation_snapshot",
  "version": "1.0.0",
  "description": "",
  "main": "compose_snapshot_task.js",
  "scripts": {
    "start:dev": "cross-env APP_ENV=dev node compose_snapshot_task.js",
    "start:test": "cross-env APP_ENV=test node compose_snapshot_task.js",
    "start:prod": "cross-env APP_ENV=prod node compose_snapshot_task.js"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "amqplib": "^0.8.0",
    "mongodb": "^3.6.9",
    "quill-delta": "^4.2.2"
  },
  "devDependencies": {
    "cross-env": "^7.0.3"
  }
}
```

pm2管理的进程开机自启动
```shell
pm2 save
```

pm2服务开机自启动
```shell
pm2 startup
```
