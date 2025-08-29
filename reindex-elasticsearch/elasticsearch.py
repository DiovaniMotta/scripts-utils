import requests
import time

from mappers import Mapper
from logger import log

class ElasticsearchClient:

    def __init__(self, configs):
        self.url = configs.host
        self.number_of_shards = configs.shards
        self.number_of_replicas = configs.replicas

    def find_index_by_name(self, index_name='hcm-rs-*'):
        complete_url = f"{self.url}/{index_name}/_stats?level=shards"
        log.info(f"Executing [GET] request to API: {complete_url}")
        try:
            response = requests.get(complete_url, auth=None, verify=False)
            response.raise_for_status()
            response_data = response.json()
            prefix_index = index_name[:-1] if index_name.endswith("*") else index_name
            return Mapper.map_to_index(response_data, prefix_index)

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                log.warn(f"Index {index_name} not found. Returning empty list.")
                return []
            else:
                log.error(f"HTTP error while accessing {complete_url}: {e}")
                raise
        except requests.exceptions.RequestException as e:
            log.error(f"Request error while accessing {complete_url}: {e}")
            raise

    def create_index(self, index_name):
        complete_url = f"{self.url}/{index_name}"
        payload = {
            'settings':{
                'number_of_shards': self.number_of_shards,
                'number_of_replicas': self.number_of_replicas
            }
        }
        log.info(f"Executing [PUT] request to API: {complete_url} with the parameters: {payload}")
        response = requests.put(complete_url, json=payload, auth=None, verify=False)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get('acknowledged', False)


    def replicate_data_from_index(self, index_name_origin, index_name_destination):
        complete_url = f"{self.url}/_reindex?wait_for_completion=false"
        payload = {
            'source': {
                'index': index_name_origin
            },
            'dest': {
                'index': index_name_destination
            }
        }
        log.info(f"Executing [POST] request to API: {complete_url} with the parameters: {payload}")
        response = requests.post(complete_url, json=payload, auth=None, verify=False)
        response.raise_for_status()
        response_data = response.json()
        task = response_data.get("task")
        log.info(f"Asynchronous reindexing request was successfully accepted. Task created: '{task}'")
        return self.__search_task_status(task)

    def delete_index(self, index_name):
        complete_url = f"{self.url}/{index_name}"
        log.info(f"Executing [DELETE] request to API: {complete_url}")
        response = requests.delete(complete_url, auth=None, verify=False)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get("acknowledged", False)

    def __search_task_status(self, task):
        complete_url = f"{self.url}/_tasks/{task}"
        payload = {
            'task': task
        }
        log.info(f"Executing [GET] request to API: {complete_url} with the parameters: {payload}")
        while True:
            response = requests.get(complete_url, json=payload,auth=None, verify=False)
            response.raise_for_status()
            response_data = response.json()

            status = response_data.get("task", {}).get("status", {})
            created = status.get("created", 0)
            total = status.get("total", 1)

            log.info(f"Progress: {created}/{total} documents reindexed...")
            if response_data.get("completed", False):
                log.info(f"Task '{task}' has been completed")
                return  {
                    'reindex': {
                        'documents': total
                    }
                }
            else:
                time.sleep(5)
