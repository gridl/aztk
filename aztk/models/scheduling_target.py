from enum import Enum

class SchedulingTarget(Enum):
    """
    Target where task will get scheduled.
    For spark this is where the driver will live.
    """

    Master = "master"
    """
    Only master is allowed to run task
    """

    Dedicated = "dedicated"
    """
    Any dedicated node is allowed to run task(Default)
    """

    NonMasterDedicated = "non_master_dedicated"
    """
    Any dedicated node that is not the master
    """

    Any  = "any"
    """
    Any node(Not reconmmended if using low pri)
    """

