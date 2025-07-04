import pulumi
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi_kubernetes.networking.v1 import Ingress, IngressSpecArgs
from pulumi_kubernetes.core.v1 import Namespace
from typing import Dict, List, Any, Optional
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('k8s_ingress')


class DelayProvider(pulumi.dynamic.ResourceProvider):
    def create(self, props):
        delay_seconds = props.get('delay_seconds', 30)
        logger.info(f"Waiting for {delay_seconds} seconds...")
        time.sleep(delay_seconds)
        logger.info("Delay completed")
        return pulumi.dynamic.CreateResult(id_=f"delay-{int(time.time())}")

class DelayResource(pulumi.dynamic.Resource):
    def __init__(self, name, delay_seconds=30, opts=None):
        props = {
            'delay_seconds': delay_seconds
        }
        super().__init__(DelayProvider(), name, props, opts)

class K8sIngress(pulumi.ComponentResource):
    
    
    def __init__(self,
                 name: str,
                 namespace: str = "ingress-nginx",
                 ingress_class_name: str = "nginx",
                 rules: List[Dict[str, Any]] = None,
                 controller_values: Optional[Dict[str, Any]] = None,
                 ingress_annotations: Optional[Dict[str, Any]] = None,
                 create_namespace: bool = False,
                 health_check_path: Optional[str] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        
        super().__init__('custom:kubernetes:K8sIngress', name, None, opts)
        
        self.namespace = namespace
        self.namespace_name = namespace
        self.ingress_class_name = ingress_class_name
        logger.info(f"Using namespace: {namespace}")
        
        from pulumi_kubernetes.apiextensions import CustomResource
        import pulumi_kubernetes.core.v1 as corev1
        
        resource_deps = []
        if create_namespace:
            try:
                existing_namespaces = corev1.NamespaceList.get(
                    "existing-namespaces",
                    opts=pulumi.ResourceOptions(parent=self)
                )
                
                namespace_exists = False
                for ns in existing_namespaces.items:
                    if ns.metadata.name == namespace:
                        namespace_exists = True
                        logger.info(f"Namespace {namespace} already exists, skipping creation")
                        break
                
                if not namespace_exists:
                    ns = Namespace(namespace,
                                  metadata={
                                       "name": namespace,
                                       "labels": {
                                           "name": namespace,
                                           "managed-by": "pulumi"
                                       }
                                   },
                                   opts=pulumi.ResourceOptions(
                                       parent=self, 
                                       protect=False
                                   ))
                    resource_deps.append(ns)
                    logger.info(f"Created namespace: {namespace}")
            except Exception as e:
                logger.warning(f"Error handling namespace: {str(e)}")
                
        
        helm_values = {
            "controller": {
                "ingressClassResource": {
                    "name": ingress_class_name,
                    "controllerValue": "k8s.io/ingress-nginx",
                    "enabled": True,
                },
                "watchIngressWithoutClass": False,
                "service": {
                    "annotations": {}
                },
                "resources": {
                    "requests": {
                        "cpu": "100m",
                        "memory": "90Mi"
                    }
                }
            }
        }
        
        if controller_values:
            helm_values = self._merge_dicts(controller_values, helm_values)
        
        
        self.controller = Chart(
            f"{name}-controller",
            ChartOpts(
                chart="ingress-nginx",
                version="4.7.1",
                fetch_opts=FetchOpts(
                    repo="https://kubernetes.github.io/ingress-nginx"
                ),
                namespace=namespace,
                values=helm_values,
                skip_await=True
            ),
            opts=pulumi.ResourceOptions(
                parent=self,
                depends_on=resource_deps,
                ignore_changes=["status"],
                custom_timeouts=pulumi.CustomTimeouts(create="5m", update="3m", delete="5m")
            )
        )
        
        default_annotations = {
            "kubernetes.io/ingress.class": ingress_class_name,
            "nginx.ingress.kubernetes.io/ssl-redirect": "false",
        }
        
        if health_check_path:
            default_annotations.update({
                "nginx.ingress.kubernetes.io/healthcheck-path": health_check_path,
            })
        
        if ingress_annotations:
            default_annotations.update(ingress_annotations)
        
        delay_name = f"{name}-delay"
        delay_resource = DelayResource(
            delay_name,
            delay_seconds=30,
            opts=pulumi.ResourceOptions(
                parent=self,
                depends_on=[self.controller]
            )
        )
        
        logger.info(f"Skipping ingress resource creation in namespace {namespace}")
        self.ingress = None
        
        logger.info("To create an ingress resource manually, use kubectl apply -f ingress.yaml")
        
        outputs = {
            "namespace": namespace,
            "ingress_class_name": ingress_class_name,
            "controller": self.controller,
        }
        
        if self.ingress is not None:
            outputs["ingress"] = self.ingress
            
        self.register_outputs(outputs)
    
    def _merge_dicts(self, source: Dict[str, Any], destination: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in source.items():
            if isinstance(value, dict) and key in destination and isinstance(destination[key], dict):
                destination[key] = self._merge_dicts(value, destination[key])
            else:
                destination[key] = value
        return destination
    
    def get_controller_url(self):
        service_name = "ingress-nginx-controller"
        
        try:
            import subprocess
            import json
            
            return pulumi.Output.from_input(f"http://<LoadBalancer-IP-for-{service_name}>")
        except Exception as e:
            logger.error(f"Error getting controller service: {str(e)}")
            return pulumi.Output.from_input("Service URL not available")

    
    def _extract_service_url(self, service):
        try:
            if service and service.status and service.status.load_balancer and service.status.load_balancer.ingress:
                ingress_list = service.status.load_balancer.ingress
                if len(ingress_list) > 0:
                    ingress = ingress_list[0]
                    if hasattr(ingress, 'hostname') and ingress.hostname:
                        return f"http://{ingress.hostname}"
                    elif hasattr(ingress, 'ip') and ingress.ip:
                        return f"http://{ingress.ip}"
            if service and service.spec and service.spec.type == "NodePort" and service.spec.ports:
                node_port = None
                for port in service.spec.ports:
                    if port.port == 80:
                        node_port = port.node_port
                        break
                if node_port:
                    return f"http://localhost:{node_port}"
            return "LoadBalancer pending"
        except Exception as e:
            logger.error(f"Error extracting service URL: {str(e)}")
            return "Error extracting service URL"