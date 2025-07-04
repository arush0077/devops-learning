import pulumi
import json
import logging
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.networking.v1 import Ingress, IngressClass
from typing import Optional, Dict, List, Any, Union, Callable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ingress_component')

class IngressComponent(pulumi.ComponentResource):
    def __init__(self, name: str, 
                 namespace: str, 
                 ingress_class_name: str, 
                 rules: List[Dict[str, Any]],
                 controller_values: Optional[Dict[str, Any]] = None,
                 ingress_annotations: Optional[Dict[str, Any]] = None,
                 create_namespace: bool = True,
                 retry_on_error: bool = True,
                 health_check_path: str = "/healthz",
                 opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__('custom:kubernetes:IngressComponent', name, {}, opts)
        
        if not name or len(name) > 20:
            raise ValueError(f"Name must be between 1-20 characters, got: '{name}'")
        
        if not namespace:
            raise ValueError("Namespace cannot be empty")
            
        if not ingress_class_name:
            raise ValueError("Ingress class name cannot be empty")
            
        if not rules or not isinstance(rules, list) or len(rules) == 0:
            raise ValueError("At least one ingress rule must be provided")
        
        logger.info(f"Initializing IngressComponent '{name}' in namespace '{namespace}'")
        
        self.namespace = namespace
        self.ingress_class_name = ingress_class_name
        self.retry_on_error = retry_on_error
        self.health_check_path = health_check_path
        
        self.controller_values = controller_values or {}
        self.ingress_annotations = ingress_annotations or {}
        
        logger.info(f"Using ingress class: {ingress_class_name}")
        logger.info(f"Controller values: {json.dumps(self.controller_values, indent=2)}")
        
        ns = None
        resource_deps = []
        if create_namespace:
            try:
                logger.info(f"Creating namespace: {namespace}")
                ns = Namespace(
                    f"{name}-ns",
                    metadata={
                        "name": namespace,
                        "labels": {
                            "name": namespace,
                            "managed-by": "pulumi",
                            "component": "ingress"
                        }
                    },
                    opts=pulumi.ResourceOptions(
                        parent=self,
                        protect=False
                    )
                )
                resource_deps.append(ns)
                logger.info(f"Successfully created namespace: {namespace}")
            except Exception as e:
                logger.error(f"Failed to create namespace {namespace}: {str(e)}")
                if not self.retry_on_error:
                    raise
                logger.info(f"Continuing without creating namespace {namespace}")
                
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
        
        def deep_merge(source: Dict[str, Any], destination: Dict[str, Any]) -> Dict[str, Any]:
            try:
                if not isinstance(source, dict) or not isinstance(destination, dict):
                    logger.warning(f"Invalid merge: source or destination is not a dictionary")
                    return destination
                    
                for key, value in source.items():
                    if isinstance(value, dict):
                        node = destination.setdefault(key, {})
                        if isinstance(node, dict):
                            deep_merge(value, node)
                        else:
                            logger.warning(f"Cannot merge dict into non-dict at key '{key}', overwriting")
                            destination[key] = value
                    elif isinstance(value, list) and key in destination and isinstance(destination[key], list):
                        destination[key].extend(value)
                    else:
                        destination[key] = value
                return destination
            except Exception as e:
                logger.error(f"Error during deep merge: {str(e)}")
                return destination
        
        if self.controller_values:
            logger.info("Merging user-provided controller values")
            try:
                helm_values = deep_merge(self.controller_values, helm_values)
                logger.info("Successfully merged controller values")
            except Exception as e:
                logger.error(f"Failed to merge controller values: {str(e)}")
        
        controller_deps = resource_deps.copy()
        
        self.ingress_controller = Release(
            f"{name}-controller",
            ReleaseArgs(
                chart="ingress-nginx",
                repository_opts=RepositoryOptsArgs(
                    repo="https://kubernetes.github.io/ingress-nginx"
                ),
                namespace=namespace,
                values=helm_values,
                timeout=600,
                cleanup_on_fail=True,
                atomic=True
            ),
            opts=pulumi.ResourceOptions(
                parent=self, 
                depends_on=controller_deps,
                ignore_changes=["status"],
                custom_timeouts=pulumi.CustomTimeouts(create="15m", update="10m", delete="10m")
            )
        )
        
        ingress_annotations = {
            "kubernetes.io/ingress.class": ingress_class_name,
            "nginx.ingress.kubernetes.io/ssl-redirect": "false",
            "nginx.ingress.kubernetes.io/force-ssl-redirect": "false",
            "nginx.ingress.kubernetes.io/proxy-connect-timeout": "300",
            "nginx.ingress.kubernetes.io/proxy-send-timeout": "300",
            "nginx.ingress.kubernetes.io/proxy-read-timeout": "300",
        }
        
        if self.health_check_path:
            ingress_annotations.update({
                "nginx.ingress.kubernetes.io/healthcheck-path": self.health_check_path,
                "nginx.ingress.kubernetes.io/healthcheck-interval": "10s",
                "nginx.ingress.kubernetes.io/healthcheck-timeout": "5s",
                "nginx.ingress.kubernetes.io/healthcheck-port": "80",
            })
        
        if self.ingress_annotations:
            logger.info("Merging user-provided ingress annotations")
            try:
                ingress_annotations.update(self.ingress_annotations)
            except Exception as e:
                logger.error(f"Failed to merge ingress annotations: {str(e)}")
        
        try:
            logger.info(f"Creating ingress resource in namespace {namespace}")
            self.ingress = Ingress(
                f"{name}-ingress",
                metadata={
                    "namespace": namespace,
                    "annotations": ingress_annotations
                },
                spec={
                    "ingressClassName": ingress_class_name,
                    "rules": rules
                },
                opts=pulumi.ResourceOptions(
                    parent=self, 
                    depends_on=[self.ingress_controller],
                    custom_timeouts=pulumi.CustomTimeouts(create="5m", update="5m", delete="5m")
                )
            )
            logger.info(f"Successfully created ingress resource")
        except Exception as e:
            logger.error(f"Failed to create ingress resource: {str(e)}")
            raise
        
        try:
            logger.info("Registering component outputs")
            self.register_outputs({
                "namespace": namespace,
                "ingress_class_name": ingress_class_name,
                "ingress_controller": self.ingress_controller,
                "ingress": self.ingress,
                "controller_service_type": self.controller_values.get("controller", {}).get("service", {}).get("type", "LoadBalancer"),
                "health_check_path": self.health_check_path,
                "creation_timestamp": pulumi.Output.from_input(self.ingress.metadata).apply(
                    lambda meta: meta.get("creationTimestamp", "")
                )
            })
            logger.info("Successfully registered component outputs")
        except Exception as e:
            logger.error(f"Error registering outputs: {str(e)}")
            
        
    def get_ingress(self):
        return self.ingress
    
    def get_controller(self):
        return self.ingress_controller
        
    def get_controller_service_url(self) -> pulumi.Output[str]:
        return self.ingress_controller.status.apply(
            lambda status: self._extract_service_url(status)
        )
    
    def _extract_service_url(self, status: Dict[str, Any]) -> str:
        try:
            if not status or 'resources' not in status:
                return "Service URL not available yet"
                
            for resource in status.get('resources', []):
                if resource.get('kind') == 'Service' and 'status' in resource:
                    service_status = resource.get('status', {})
                    ingress = service_status.get('loadBalancer', {}).get('ingress', [])
                    
                    if ingress and len(ingress) > 0:
                        if 'ip' in ingress[0]:
                            return f"http://{ingress[0]['ip']}"
                        elif 'hostname' in ingress[0]:
                            return f"http://{ingress[0]['hostname']}"
            
            return "LoadBalancer pending"
        except Exception as e:
            logger.error(f"Error extracting service URL: {str(e)}")
            return "Error extracting service URL"