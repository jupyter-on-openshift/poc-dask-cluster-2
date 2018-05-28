import os

c.JupyterHub.template_paths = [ '/opt/app-root/src/override-templates' ]

c.KubeSpawner.environment = dict(
    DASK_SCHEDULER_ADDRESS=os.environ['DASK_SCHEDULER_ADDRESS']
)

c.JupyterHub.services = [
    {
	'name': 'dask-monitor',
	'url': 'http://%s' % os.environ['DASK_MONITOR_ADDRESS']
    }
]

enable_persistent_volumes = False

if os.environ.get('OAUTH_SERVICE_TYPE') == 'GitHub':
    from oauthenticator.github import GitHubOAuthenticator
    c.JupyterHub.authenticator_class = GitHubOAuthenticator
    enable_persistent_volumes = True

c.MyOAuthenticator.oauth_callback_url = os.environ.get('OAUTH_CALLBACK_URL' )
c.MyOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.MyOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')

if enable_persistent_volumes:
    c.KubeSpawner.user_storage_pvc_ensure = True

    c.KubeSpawner.pvc_name_template = '%s-nb-{username}' % \
             c.KubeSpawner.hub_connect_ip

    c.KubeSpawner.user_storage_capacity = '1Gi'

    c.KubeSpawner.volumes = [
	{
	    'name': 'data',
	    'persistentVolumeClaim': {
		'claimName': c.KubeSpawner.pvc_name_template
	    }
	}
    ]

    c.KubeSpawner.volume_mounts = [
	{
	    'name': 'data',
	    'mountPath': '/opt/app-root',
	    'subPath': 'app-root'
	}
    ]

    c.KubeSpawner.singleuser_init_containers = [
	{
	    'name': 'setup-volume',
	    'image': os.environ['JUPYTERHUB_NOTEBOOK_IMAGE'],
	    'command': [
		'setup-volume.sh',
		'/opt/app-root',
		'/mnt/app-root'
	    ],
	    'resources': {
		'limits': {
		    'memory': '256Mi'
		}
	    },
	    'volumeMounts': [
		{
		    'name': 'data',
		    'mountPath': '/mnt'
		}
	    ]
	}
    ]
