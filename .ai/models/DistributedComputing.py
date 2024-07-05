from dask.distributed import Client

class DistributedComputing:
    def __init__(self, client):
        self.client = client

    def compute(self, func, data):
        future = self.client.submit(func, data)
        result = future.result()
        return result

    def close(self):
        self.client.close()
