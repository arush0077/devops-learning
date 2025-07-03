from pulumi_kubernetes.core.v1 import Service

def create_service(name_of_ns,port,targetPort):
    app_labels = { "app": name_of_ns }

    return Service(
        name_of_ns + "-svc",
        metadata={ "namespace": name_of_ns },
        spec={
            "selector": app_labels,
            "ports": [{
                "port": port,
                "targetPort": targetPort,
                "protocol": "TCP"
            }],
            "type": "NodePort"  
        }
    )
