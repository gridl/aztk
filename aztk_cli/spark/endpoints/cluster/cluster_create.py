import argparse
import typing

import aztk.spark
from aztk.spark.models import ClusterConfiguration, UserConfiguration
from aztk_cli import config, log, utils
from aztk_cli.config import load_aztk_spark_config


def setup_parser(parser: argparse.ArgumentParser):
    parser.add_argument('--id', dest='cluster_id',
                        help='The unique id of your spark cluster')
    parser.add_argument('--size', type=int,
                        help='Number of vms in your cluster')
    parser.add_argument('--size-low-pri', type=int,
                        help='Number of low priority vms in your cluster')
    parser.add_argument('--vm-size',
                        help='VM size for nodes in your cluster')
    parser.add_argument('--username',
                        help='Username to access your cluster (required: --wait flag)')
    parser.add_argument('--password',
                        help="The password to access your spark cluster's head \
                             node. If not provided will use ssh public key.")
    parser.add_argument('--docker-repo',
                        help='The location of the public docker image you want to use \
                             (<my-username>/<my-repo>:<tag>)')
    parser.add_argument('--subnet-id',
                        help='The subnet in which to create the cluster.')

    parser.add_argument('--no-wait', dest='wait', action='store_false')
    parser.add_argument('--wait', dest='wait', action='store_true')
    parser.set_defaults(wait=None, size=None, size_low_pri=None)


def execute(args: typing.NamedTuple):
    spark_client = aztk.spark.Client(config.load_aztk_secrets())
    cluster_conf = ClusterConfiguration()
    cluster_conf.spark_configuration = load_aztk_spark_config()

    # read cluster.yaml configuartion file, overwrite values with args
    file_config, wait = config.read_cluster_config()
    cluster_conf.merge(file_config)
    cluster_conf.merge(ClusterConfiguration(
        cluster_id=args.cluster_id,
        vm_count=args.size,
        vm_low_pri_count=args.size_low_pri,
        vm_size=args.vm_size,
        subnet_id=args.subnet_id,
        user_configuration=UserConfiguration(
            username=args.username,
            password=args.password,
        )))

    if args.docker_repo and cluster_conf.toolkit:
        cluster_conf.toolkit.docker_repo = args.docker_repo

    wait = wait if args.wait is None else args.wait

    user_configuration = cluster_conf.user_configuration

    if user_configuration and user_configuration.username:
        ssh_key, password = utils.get_ssh_key_or_prompt(spark_client.secrets_config.ssh_pub_key,
                                                        user_configuration.username,
                                                        user_configuration.password,
                                                        spark_client.secrets_config)
        cluster_conf.user_configuration = aztk.spark.models.UserConfiguration(
            username=user_configuration.username,
            password=password,
            ssh_key=ssh_key
        )
    else:
        cluster_conf.user_configuration = None

    utils.print_cluster_conf(cluster_conf, wait)
    with utils.Spinner():
        # create spark cluster
        cluster = spark_client.create_cluster(
            cluster_conf,
            wait=wait
        )

    if wait:
        log.info("Cluster %s created successfully.", cluster.id)
    else:
        log.info("Cluster %s is being provisioned.", cluster.id)
