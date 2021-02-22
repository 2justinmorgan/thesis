
import pytest
import importlib
import clustering_evaluation


@pytest.fixture(autouse=True)
def before_each():
    x = importlib


@pytest.mark.parametrize(
    "user_freqs,expect",
    [
        ({
            "userA": 2,
            "userB": 88,
            "userC": 24,
            "userD": 9,
            "userE": 0,
            "userF": 30
        },
         0.133987),
        ({
            "userA": 20,
            "userB": 6,
            "userC": 3,
            "userD": 9,
            "userE": 6,
            "userF": 18
        },
         0.006298),
        ({
             "userA": 311,
             "userB": 323,
             "userC": 325,
             "userD": 112,
             "userE": 374,
             "userF": 408
         },
         9.570579),
        ({
             "userA": 23,
             "userB": 44,
             "userC": 78,
             "userD": 12,
             "userE": 38,
             "userF": 21
         },
         0.017574)
    ]
)
def test_get_user_freq_bias_metric(user_freqs, expect):
    cluster = clustering_evaluation.defines.Cluster(
        cluster_id="sample_cluster",
        user_names=list(user_freqs.keys())
    )
    cluster.user_freqs = user_freqs
    cluster.population_count = sum(list(user_freqs.values()))
    actual = clustering_evaluation.get_user_freq_bias_metric(cluster, 1676, 10)
    assert actual == pytest.approx(expect, 1)
