import dask.dataframe as dd

class Reader:

    @staticmethod
    def read_csv(filepath):
        df = dd.read_csv(filepath, dtype={
            'index_name': 'string'
        })
        summary = df.compute()
        return summary.reset_index(drop=True)