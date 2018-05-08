import io

import azure.batch.models as batch_models

class File:
    def __init__(self, name: str, payload: io.StringIO):
        self.name = name
        self.payload = payload


class RemoteLogin:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port



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
