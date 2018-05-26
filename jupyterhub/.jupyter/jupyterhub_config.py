import os

c.KubeSpawner.environment = dict(
    DASK_SCHEDULER_ADDRESS=os.envrion['DASK_SCHEDULER_ADDRESS']
)
