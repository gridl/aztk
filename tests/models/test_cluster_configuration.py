import pytest

from aztk.models import ClusterConfiguration

def test_vm_count_deprecated():
    with pytest.warns(DeprecationWarning):
        config = ClusterConfiguration(vm_count=3)
        assert config.size == 3

    with pytest.warns(DeprecationWarning):
        config = ClusterConfiguration(vm_low_pri_count=10)
        assert config.size_low_pri == 10
