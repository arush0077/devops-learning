import pulumi

def get_config():
    config = pulumi.Config()
    
    return {
        'namespace': config.get('namespace') or 'notes-app',
        'notes_app_image': config.get('notesAppImage') or 'trainwithshubham/notes-app-k8s',
        'nginx_image': config.get('nginxImage') or 'nginx',
        'notes_app_replicas': config.get_int('notesAppReplicas') or 2,
        'nginx_replicas': config.get_int('nginxReplicas') or 2,
        'notes_app_port': config.get_int('notesAppPort') or 8000,
        'nginx_port': config.get_int('nginxPort') or 80,
    }