import io
from typing import List
import azure.batch.models as batch_models
from aztk import error
from aztk.utils import helpers, deprecate
from aztk.models.plugins import PluginConfiguration
from aztk.internal import ConfigurationBase
from .toolkit import Toolkit
from aztk.core.models import Model, fields

class File:
    def __init__(self, name: str, payload: io.StringIO):
        self.name = name
        self.payload = payload


class RemoteLogin:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port


class ServicePrincipalConfiguration(ConfigurationBase):
    """
    Container class for AAD authentication
    """

    def __init__(self,
                 tenant_id: str = None,
                 client_id: str = None,
                 credential: str = None,
                 batch_account_resource_id: str = None,
                 storage_account_resource_id: str = None):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.credential = credential
        self.batch_account_resource_id = batch_account_resource_id
        self.storage_account_resource_id = storage_account_resource_id

    def validate(self) -> bool:
        """
        Validate the config at its current state.
        Raises: Error if invalid
        """
        self._validate_required([
            "tenant_id",
            "client_id",
            "credential",
            "batch_account_resource_id",
            "storage_account_resource_id",
        ])


class SharedKeyConfiguration(ConfigurationBase):
    """
    Container class for shared key authentication
    """

    def __init__(self,
                 batch_account_name: str = None,
                 batch_account_key: str = None,
                 batch_service_url: str = None,
                 storage_account_name: str = None,
                 storage_account_key: str = None,
                 storage_account_suffix: str = None):

        self.batch_account_name = batch_account_name
        self.batch_account_key = batch_account_key
        self.batch_service_url = batch_service_url
        self.storage_account_name = storage_account_name
        self.storage_account_key = storage_account_key
        self.storage_account_suffix = storage_account_suffix

    def validate(self) -> bool:
        """
        Validate the config at its current state.
        Raises: Error if invalid
        """
        self._validate_required([
            "batch_account_name",
            "batch_account_key",
            "batch_service_url",
            "storage_account_name",
            "storage_account_key",
            "storage_account_suffix",
        ])


class DockerConfiguration(ConfigurationBase):
    def __init__(self, endpoint=None, username=None, password=None):

        self.endpoint = endpoint
        self.username = username
        self.password = password

    def validate(self):
        pass


class SecretsConfiguration(ConfigurationBase):
    def __init__(self,
                 service_principal=None,
                 shared_key=None,
                 docker=None,
                 ssh_pub_key=None,
                 ssh_priv_key=None):
        self.service_principal = service_principal
        self.shared_key = shared_key
        self.docker = docker

        self.ssh_pub_key = ssh_pub_key
        self.ssh_priv_key = ssh_priv_key

    def validate(self):
        if self.service_principal and self.shared_key:
            raise error.AztkError(
                "Both service_principal and shared_key auth are configured, must use only one"
            )
        elif self.service_principal:
            self.service_principal.validate()
        elif self.shared_key:
            self.shared_key.validate()
        else:
            raise error.AztkError(
                "Neither service_principal and shared_key auth are configured, must use only one"
            )

    def is_aad(self):
        return self.service_principal is not None


class VmImage:
    def __init__(self, publisher, offer, sku):
        self.publisher = publisher
        self.offer = offer
        self.sku = sku


class Cluster:
    def __init__(self,
                 pool: batch_models.CloudPool,
                 nodes: batch_models.ComputeNodePaged = None):
        self.id = pool.id
        self.pool = pool
        self.nodes = nodes
        self.vm_size = pool.vm_size
        if pool.state.value is batch_models.PoolState.active:
            self.visible_state = pool.allocation_state.value
        else:
            self.visible_state = pool.state.value
        self.total_current_nodes = pool.current_dedicated_nodes + \
            pool.current_low_priority_nodes
        self.total_target_nodes = pool.target_dedicated_nodes + \
            pool.target_low_priority_nodes
        self.current_dedicated_nodes = pool.current_dedicated_nodes
        self.current_low_pri_nodes = pool.current_low_priority_nodes
        self.target_dedicated_nodes = pool.target_dedicated_nodes
        self.target_low_pri_nodes = pool.target_low_priority_nodes


class SSHLog():
    def __init__(self, output, node_id):
        self.output = output
        self.node_id = node_id


class Software:
    """
        Enum with list of available softwares
    """
    spark = "spark"
