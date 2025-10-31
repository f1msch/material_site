```
# 安装vue/cli
$ npm install -g @vue/cli
# 在项目目录下，运行以下命令来安装所有依赖（包括 vue-cli-service）
npm install
# 创建vue项目
$ vue create .
# 启动vue前端
npm run serve
```

**npm run serve (开发模式)**
* 用途: 启动开发服务器，用于开发阶段

* 特点:

* * 实时热重载（修改代码自动刷新）

* * 源代码映射（便于调试）

* * 不生成构建文件

* * 访问: http://localhost:8080/

* 使用场景: 开发时使用

**npm run build (生产构建)**
* 用途: 构建生产版本

* 特点:

* * 压缩和优化代码

* * 生成 dist/ 或配置的输出目录

* * 没有开发服务器

* * 需要配置Web服务器来提供静态文件

* 使用场景: 部署到生产环境时使用