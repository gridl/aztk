from azure import batch
from aztk.models import ClusterConfiguration, SchedulingTarget
from core import config, log

def disable_scheduling(batch_client: batch.BatchServiceClient):
    """
    Disable scheduling for the current node
    """
    pool_id = config.pool_id
    node_id = config.node_id

    node = batch_client.compute_node.get(pool_id, node_id)
    if node.scheduling_state == batch.models.SchedulingState.enabled:
        log.info("Disabling task scheduling for this node")
        batch_client.compute_node.disable_scheduling(pool_id, node_id)
    else:
        log.info("Task scheduling is already disabled for this node")

def enable_scheduling(batch_client: batch.BatchServiceClient):
    """
    Disable scheduling for the current node
    """
    pool_id = config.pool_id
    node_id = config.node_id

    node = batch_client.compute_node.get(pool_id, node_id)
    if node.scheduling_state == batch.models.SchedulingState.disabled:
        log.info("Enabling task scheduling for this node")
        batch_client.compute_node.disable_scheduling(pool_id, node_id)
    else:
        log.info("Task scheduling is already enabled for this node")


def setup_node_scheduling(batch_client: batch.BatchServiceClient, cluster_config: ClusterConfiguration, is_master: bool):
    is_dedicated = config.is_dedicated
    enable = False
    if cluster_config.scheduling_target == SchedulingTarget.Any:
        log.info("Scheduling target is any, will enable scheduling on this node")
        enable = True
    elif cluster_config.scheduling_target == SchedulingTarget.Dedicated and is_dedicated:
        log.info("Scheduling target is dedicated and this node is dedicated, will enable scheduling on this node")
        enable = True
    elif cluster_config.scheduling_target == SchedulingTarget.Master and is_master:
        log.info("Scheduling target is master and this node is the master, will enable scheduling on this node")
        enable = True
    elif cluster_config.scheduling_target == SchedulingTarget.NonMasterDedicated and not is_master and is_dedicated:
        log.info("Scheduling target is NonMasterDedicated and this node is dedicated but not the master, will enable scheduling on this node")
        enable = True

    if enable:
        enable_scheduling(batch_client)
    else:
        disable_scheduling(batch_client)
