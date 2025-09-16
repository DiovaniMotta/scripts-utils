import dask.dataframe as dd
import json
from logger import log

class Reader:

    @staticmethod
    def read_csv(filepath):
        df = dd.read_csv(filepath, dtype={
            'index_name': 'string'
        })
        summary = df.compute()
        return summary.reset_index(drop=True)

    @staticmethod
    def read_json(filepath, tag):
        try:
            with open(filepath, "r", encoding="utf-8") as json_file:
                content = json.load(json_file)
                return content[tag]
        except json.JSONDecodeError as e:
            log.error(f"Failed to extract information {tag} from JSON file {filepath}: Error: {e}")
            raise