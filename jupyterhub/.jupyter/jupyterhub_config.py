import os

c.KubeSpawner.environment = dict(
    DASK_SCHEDULER_ADDRESS=os.environ['DASK_SCHEDULER_ADDRESS']
)

c.JupyterHub.services = [
    {
	'name': 'dask-monitor',
	'url': 'http://%s' % os.environ['DASK_MONITOR_ADDRESS']
    }
]
