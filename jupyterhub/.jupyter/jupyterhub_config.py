import os

c.KubeSpawner.environment = dict(
    DASK_SCHEDULER_ADDRESS=os.environ['DASK_SCHEDULER_ADDRESS']
)
