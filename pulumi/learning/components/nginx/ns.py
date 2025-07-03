# components/namespace.py

from pulumi_kubernetes.core.v1 import Namespace

def create_namespace(namespace_name):
    return Namespace("pulumi-ns", metadata={ "name": namespace_name })

