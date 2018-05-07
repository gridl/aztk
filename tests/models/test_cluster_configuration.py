import pytest

from aztk.error import InvalidModelError
from aztk.models import ClusterConfiguration, SchedulingTarget, Toolkit

def test_scheduling_target_dedicated_with_no_dedicated_nodes_raise_error():
    with pytest.raises(InvalidModelError, match="Scheduling target cannot be Dedicated if dedicated vm size is 0"):
        conf = ClusterConfiguration(
            cluster_id="abc",
            scheduling_target=SchedulingTarget.Dedicated,
            vm_size="standard_a2",
            vm_count=0,
            vm_low_pri_count=2,
            toolkit=Toolkit(software="spark", version="1.6.3"),
        )

        conf.validate()
