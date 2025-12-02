## redis
**TODO: how to use Celery??**

docker run --name my_redis redis:7-alpine
```bash
docker exec -it my-redis redis-cli ping
同样，返回 PONG 即为成功。
```
## postgres
默认user postgres
docker run -d --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres:latest
### pgAdmin
#### 第一步：拉取镜像
docker pull dpage/pgadmin4:latest
#### 第二步：运行容器
docker run -d --name my_pgadmin -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4:latest

http://localhost:5050

## elasticsearch

docker pull docker.elastic.co/elasticsearch/elasticsearch:8.9.0
docker run -d --name my-es -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0
https://chat.deepseek.com/share/84167pajtj8vbkzaha

* -d: 在后台运行容器。
* --name my-es: 为容器指定一个名字。
* -p 9200:9200: 将容器的 9200 端口（Elasticsearch 的 HTTP API 端口）映射到宿主机的相同端口。
* -e "discovery.type=single-node": 设置为单节点模式，适用于开发。
* -e "xpack.security.enabled=false": （开发环境适用） 禁用安全功能，方便本地连接。生产环境中务必开启。

http://localhost:9200


## MinIO
https://chat.deepseek.com/share/rlqdu2o2eq7uylvubd

# 拉取镜像
docker pull minio/minio
# 运行容器 (将 `/your/local/data` 和 `/your/local/config` 替换为本地路径)
docker run -d \
   -p 9000:9000 -p 9001:9001 \
   --name minio \
   -e "MINIO_ROOT_USER=你的管理账号" \
   -e "MINIO_ROOT_PASSWORD=你的强密码" \
   -v /your/local/data:/data \
   -v /your/local/config:/root/.minio \
   minio/minio server /data --console-address ":9001"