import pytest

from gfitpy.utils.activities import Activity


@pytest.mark.parametrize(
    'activity',
    [
        Activity.biking,
        Activity.walking,
        Activity.running,
    ]
)
def test_activity_valid(activity):
    assert activity.valid()


@pytest.mark.parametrize(
    'activity',
    [
        Activity.unknown,
        Activity.sleeping
    ]
)
def test_activity_invalid(activity):
    assert not activity.valid()


@pytest.mark.parametrize(
    'activity, mfp_id',
    [
        (Activity.biking, 19),
        (Activity.walking, 26688321),
        (Activity.running, 127),
    ]
)
def test_mfp_id(activity, mfp_id):
    assert activity.mfp_id == mfp_id


@pytest.mark.parametrize(
    'activity',
    [
        Activity.unknown,
        Activity.sleeping
    ]
)
def test_mfp_id_raises(activity):
    with pytest.raises(NotImplementedError):
        activity.mfp_id
