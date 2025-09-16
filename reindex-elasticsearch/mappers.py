
class Mapper:

    @staticmethod
    def map_to_index(data_stats, data_settings, mappings, prefix_index):
        summary = {}

        for index_name, index_data in data_stats.get("indices", {}).items():
            if index_name.startswith(prefix_index):
                docs_count = index_data.get("primaries", {}).get("docs", {}).get("count", 0)
                number_of_shards = int(data_settings.get(index_name, {}).get("settings", {}).get("index", {}).get("number_of_shards", 0))
                number_of_replicas = int(data_settings.get(index_name, {}).get("settings", {}).get("index", {}).get("number_of_replicas", 0))

                if index_name not in summary:
                    summary[index_name] = {
                        "shardCount": number_of_shards,
                        "memoryBytes": 0,
                        "docsCount": docs_count,
                        "replicas": number_of_replicas
                    }

                shards = index_data.get("shards", {})
                for shard_array in shards.values():
                    for shard in shard_array:
                        summary[index_name]["memoryBytes"] += shard.get("segments", {}).get("memory_in_bytes", 0)
        results = [
            {
                "name": name,
                "number_of_shards": stats["shardCount"],
                "number_of_replicas": stats["replicas"],
                "docsCount": stats["docsCount"],
                "memoryMB": round(stats["memoryBytes"] / 1048576, 2),
                "analysis": data_settings.get(name, {}).get("settings", {}).get("index", {}).get("analysis", {}),
                "mappings": mappings.get(name, {}).get('mappings', {})
            }
            for name, stats in summary.items()
        ]
        results.sort(key=lambda x: x["memoryMB"], reverse=True)
        return results

    @staticmethod
    def map_to_settings(configs):
        settings = {
            "index_name": configs.get('index_name')
        }

        if configs['analysis']['file']:
            settings["analysis"] = configs["analysis"]["file"]
        elif configs['analysis']['index']:
            settings["analysis"] = configs["analysis"]["index"]

        if configs['mappings']['file']:
            settings["mappings"] = configs["mappings"]["file"]
        elif configs['mappings']['index']:
            settings["mappings"] = configs["mappings"]["index"]

        return settings

