from pynamodb.models import Model

from alfred.feature_flag.models import FeatureFlag
from alfred.settings import DYNAMODB_PREFIX


def test_feature_flag_isinstance():
    assert issubclass(FeatureFlag, Model)


def test_feature_flag_tablename():
    assert FeatureFlag.Meta.table_name == f"{DYNAMODB_PREFIX}_feature_flag"


def test_feature_flag_get_date_with_sucess():
    FeatureFlag(
        id=1,
        data={"foo": "bar"},
    ).save()

    flag = FeatureFlag.get_data(id=1)

    assert flag == {"foo": "bar"}


def test_feature_flag_get_date_with_none():
    FeatureFlag(
        id=1,
        data={"foo": "bar"},
    ).save()
    flag = FeatureFlag.get_data(id=None)

    assert flag is None


def test_feature_flag_get_date_with_wrong_id():
    FeatureFlag(
        id=1,
        data={"foo": "bar"},
    ).save()
    flag = FeatureFlag.get_data(id=6)

    assert flag is None


def test_feature_flag_get_batch():

    with FeatureFlag.batch_write() as batch:
        for i in range(5):
            batch.save(FeatureFlag(id=i, data={"foo": f"bar{i}"}))
    flag = FeatureFlag.get_batch_feature_flag([1, 2, 3, 4, 5])
    assert flag == {"foo": "bar1"}
