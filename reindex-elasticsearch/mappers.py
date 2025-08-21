
class Mapper:

    @staticmethod
    def map_to_index(response_data, prefix_index):
        summary = {}

        for index_name, index_data in response_data.get("indices", {}).items():
            if index_name.startswith(prefix_index):
                shards = index_data.get("shards", {})
                docs_count = index_data.get("primaries", {}).get("docs", {}).get("count", 0)
                replicas = int(
                    index_data.get(index_name, {}).get("settings", {}).get("index", {}).get("number_of_replicas", 0))

                if index_name not in summary:
                    summary[index_name] = {
                        "shardCount": 0,
                        "memoryBytes": 0,
                        "docsCount": docs_count,
                        "replicas": replicas
                    }

                for shard_array in shards.values():
                    for shard in shard_array:
                        summary[index_name]["shardCount"] += 1
                        summary[index_name]["memoryBytes"] += shard.get("segments", {}).get("memory_in_bytes", 0)
        results = [
            {
                "name": name,
                "number_of_shards": stats["shardCount"],
                "number_of_replicas": stats["replicas"],
                "docsCount": stats["docsCount"],
                "memoryMB": round(stats["memoryBytes"] / 1048576, 2)
            }
            for name, stats in summary.items()
        ]
        results.sort(key=lambda x: x["memoryMB"], reverse=True)
        return results
