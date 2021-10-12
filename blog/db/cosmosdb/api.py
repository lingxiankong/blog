# Copyright 2021 Catalyst Cloud
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import uuid
import sys

from azure.cosmos import exceptions, CosmosClient, PartitionKey
from oslo_config import cfg

CONTAINER = None
CONF = cfg.CONF


def get_backend():
    return sys.modules[__name__]


def setup_db():
    global CONTAINER

    client = CosmosClient(CONF.cosmosdb.endpoint, CONF.cosmosdb.key)
    database = client.create_database_if_not_exists(id='Imooc')
    CONTAINER = database.create_container_if_not_exists(
        id='Blog',
        partition_key=PartitionKey(path="/title"),
        offer_throughput=400
    )


def get_post(id):
    # Otherwise, we need to provide the value of partition key.
    query = f'SELECT * FROM c WHERE c.id = "{id}"'
    items = list(CONTAINER.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    return items[0]


def get_posts():
    global CONTAINER

    return list(CONTAINER.read_all_items())


def create_post(title, content):
    id = str(uuid.uuid4())
    post = {
        'id': id,
        'title': title,
        'content': content,
    }
    CONTAINER.create_item(body=post)


def update_post(id, title, content):
    body = {
        'id': id,
        'title': title,
        'content': content
    }
    CONTAINER.upsert_item(body)


def delete_post(id):
    post = get_post(id)
    CONTAINER.delete_item(post, post['title'])