# Blog Demo

## Containerization

1. Build the container image

   ```shell
   docker build -t lingxiankong/blog-demo:1.0.0 .
   ```

1. Run a database container and initialize database

   ```shell
   docker volume create mysql
   docker volume create mysql_config
   docker network create mysqlnet
   docker run --rm -d \
     -v mysql:/var/lib/mysql \
     -v mysql_config:/etc/mysql \
     -v $(pwd)/schema.sql:/docker-entrypoint-initdb.d/schema.sql \
     --network mysqlnet \
     --name mysqldb \
     -e MYSQL_ROOT_PASSWORD=123456 \
     mysql:5.7
   ```

1. Run the blog demo as a container

   ```shell
   docker rm -f blog_demo; \
   docker run -p 5000:5000 -d --name blog_demo \
     --network mysqlnet \
     --env PORT=5000 \
     --env DB_CONNECTION=mysql+pymysql://root:123456@mysqldb/blog?charset=utf8 \
     --env FLASK_ENV=development \
     lingxiankong/blog-demo:1.0.0
   ```

1. Clean up

   ```shell
   docker rm -f mysqldb blog_demo
   docker volume rm mysql mysql_config
   docker network rm mysqlnet
   ```

## Docker compose

1. Start up

   ```shell
   docker-compose up -d
   ```

1. Clean up

   ```shell
   docker-compose down -v && docker-compose rm -f -s -v
   ```