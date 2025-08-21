import argparse

from logger import log
from reader import Reader
from elasticsearch import ElasticsearchClient
from file import FileValidator

class Processor:

    def __init__(self, configs):
        self.client = ElasticsearchClient(configs)
        self.mode = configs.mode
        self.prefix = configs.prefix
        self.number_of_shards = configs.shards
        self.number_of_replicas = configs.replicas
        self.file_path = configs.file
        self.host = configs.host

    def execute(self):
        try:
            log.info("Start the Elasticsearch cluster maintenance process...")
            log.info("Parameters:")
            log.info(f"   Cluster host: {self.host}")
            log.info(f"   Operation mode: {self.mode}")
            log.info(f"   Number of shards: {self.number_of_shards}")
            log.info(f"   Number of replicas: {self.number_of_replicas}")
            log.info(f"   Prefix of the analyzed indices: {self.prefix}")
            if self.file_path:
                log.info(f"   Data file path: {self.file_path}")

            if self.mode == 'DELETE':
                indexes = self.client.find_index_by_name(self.prefix)
                self.delete(indexes)
            if self.mode == 'REINDEX':
                indexes = self.client.find_index_by_name(self.prefix)
                self.reindex(indexes)
            if self.mode == 'ALL':
                indexes = self.client.find_index_by_name(self.prefix)
                self.delete(indexes)
                self.reindex(indexes)
            if self.mode == 'ONLY':
                self.process_only_indexes()
            if self.mode == 'SEARCH':
                self.report()
        except Exception as e:
            log.error(f"An error occurred while executing the cluster maintenance routine : {e}")
            return None

    def delete(self, indexes):
        try:
            log.info(f'Starting the deletion process for unregistered indices')
            indexes_without_documents = [index for index in indexes if index["docsCount"] == 0]
            if len(indexes_without_documents) == 0:
                log.warn('There are no indices without documents to be deleted.')
                return

            log.info(f'Found {len(indexes_without_documents)} indices with no documents')
            for index in indexes_without_documents:
                log.info(f"Starting deletion for index: '{index['name']}'")
                response = self.client.delete_index(index['name'])
                log.info(f'Has the index deletion process been completed? {response}')
            log.info('Finishing the deletion process for indices without documents.')
        except Exception as e:
            log.error(f"An error occurred while executing the index deletion : {e}")
            return None

    def reindex(self, indexes):
        try:
            log.info('Starting the reindexing process for indices with documents.')
            indexes_with_documents = [index for index in indexes if index["docsCount"] > 0]
            if len(indexes_with_documents) == 0:
                log.warn('There are no indices with documents to be reindexed.')
                return

            log.info(f'Found {len(indexes_with_documents)} indices with documents')
            for index in indexes_with_documents:
                index_name = index['name']
                log.info(f"Starting the reindexing process for the index: '{index_name}'")
                if (self.number_of_shards == int(index.get('number_of_shards', 0))
                    and self.number_of_replicas == int(index.get('number_of_replicas', 0))
                ):
                    log.warn(
                        f"Index '{index_name}' reindexing is unnecessary because "
                        f"the settings (Shards: {self.number_of_shards} and "
                        f"Replicas: {self.number_of_replicas}) are already applied."
                    )
                    continue
                backup_index_name = f'backup-{index_name}'
                log.info(f"Creating index '{backup_index_name}' for document backup")
                response = self.client.create_index(backup_index_name)
                log.info(f"Has the index '{backup_index_name}' been created? {response}")
                log.info(f"Replicating documents from index '{index_name}' to index '{backup_index_name}'")
                status = self.client.replicate_data_from_index(index_name, backup_index_name)
                log.info(f"Reindexed {status['reindex']['documents']} documents")
                log.info(f"Deleted index '{index_name}'")
                response = self.client.delete_index(index_name)
                log.info(f"Has the index '{index_name}' deletion process been completed? {response}")
                log.info(f"Rebuilding index '{index_name}' with parameters: [Number of shards: {self.number_of_shards}, Number of replicas:{self.number_of_replicas}]")
                response = self.client.create_index(index_name)
                log.info(f"Has the index '{index_name}' been created? {response}")
                log.info(f"Replicating documents from index '{backup_index_name}' to index '{index_name}'")
                status = self.client.replicate_data_from_index(backup_index_name, index_name)
                log.info(f"Reindexed {status['reindex']['documents']} documents")
                log.info(f"Deleted index '{backup_index_name}'")
                response = self.client.delete_index(backup_index_name)
                log.info(f"Has the index '{backup_index_name}' deletion process been completed? {response}")
                log.info(f"Reindexing of index '{index_name}' completed...")
            log.info('Finishing the reindex process for indices with documents.')
        except Exception as e:
            log.error(f"An error occurred while executing the reindexing routine for the index : {e}")
            return None

    def process_only_indexes(self):
        try:
            log.info('Starting cluster maintenance process for specific indices')
            data_set = Reader.read_csv(self.file_path)
            log.info(f'Amount of objects read from CSV file: {data_set.shape[0]}')
            for _, row in data_set.iterrows():
                log.info(f'Starting process for index: {row['index_name']}')
                indexes = self.client.find_index_by_name(row['index_name'])
                self.delete(indexes)
                self.reindex(indexes)
            log.info('Finishing cluster maintenance process for specific indices...')
        except Exception as e:
            log.error(f"An error occurred while performing maintenance for specific indices : {e}")
            return None

    def report(self):
        total_memory = 0
        total_docs = 0
        total_shards = 0
        total_replicas = 0
        indexes_with_data = 0
        indexes_without_data = 0

        indexes = self.client.find_index_by_name(self.prefix)

        log.info_with_print("-" * 100)
        log.info_with_print(f"{'Index':50} {'Shards':>6} {'Replicas':>9} {'Documents':>10} {'Memory (MB)':>14}")
        log.info_with_print("-" * 100)

        for entry in indexes:
            log.info_with_print(
                f"{entry['name']:50} {entry['number_of_shards']:>6} {entry['number_of_replicas']:>9} {entry['docsCount']:>10} {entry['memoryMB']:>14}")

            total_memory += entry['memoryMB']
            total_docs += entry['docsCount']
            total_shards += entry['number_of_shards']
            total_replicas += entry['number_of_replicas']
            if entry['docsCount'] > 0:
                indexes_with_data += 1
            else:
                indexes_without_data += 1

        log.info_with_print("-" * 100)
        log.info_with_print(f"{'TOTAL':50} {total_shards:>6} {total_replicas:>9} {total_docs:>10} {round(total_memory, 2):>14}")
        log.info_with_print("-" * 100)
        log.info_with_print(f"{'Index with documents:':50} {indexes_with_data:>6}")
        log.info_with_print(f"{'Index without documents:':50} {indexes_without_data:>6}")
        log.info_with_print("-" * 100)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument(
        "-H", "--host",
        type=str,
        required=True,
        help="Enter the Elasticsearch cluster address"
    )
    parser.add_argument(
         "-m", "--mode",
        choices=["ALL", "DELETE", "REINDEX", "ONLY", "SEARCH"],
        default='ALL',
        help="Choose the operation mode (default: ALL)"
    )
    parser.add_argument(
        "-s", "--shards",
        type=int,
        default=1,
        help="Enter the number of shards. (default: 1)"
    )
    parser.add_argument(
        "-r", "--replicas",
        type=int,
        default=1,
        help="Enter the number of replicas. (default: 1)"
    )
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        default='hcm-rs-*',
        help="Enter the index name prefix. (default: hcm-rs-*)"
    )
    parser.add_argument(
        "-f", "--file",
        type= lambda f: FileValidator.allow_extension(f, extensions=[".csv"]),
        required=False,
        help="CSV file containing the indices to process (required if operation mode is ONLY)"
    )

    args = parser.parse_args()
    if args.mode == "ONLY" and not args.file:
        parser.error("--file is required when mode is ONLY")
    if args.mode != "ONLY":
        args.file = None
    processor = Processor(args)
    processor.execute()