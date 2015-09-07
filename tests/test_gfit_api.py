from unittest.mock import Mock, patch, call

import pytest

from gfitpy.gfit_api import GfitAPI


def test_get_time_range():
    start = Mock(timestamp=Mock(return_value=1))
    end = Mock(timestamp=Mock(return_value=2))
    expected = '1000000000-2000000000'
    assert GfitAPI.get_time_range_str(start, end) == expected


@patch('gfitpy.gfit_api.datetime')
@patch('gfitpy.gfit_api.DateRange')
@patch.object(GfitAPI, 'process_datapoint')
def test_preprocess_data_correct_daterange(proc_datapoint, daterange, datetime):
    data = {
        'minStartTimeNs': 1000000000,
        'maxEndTimeNs': 2000000000,
    }
    datetime.fromtimestamp=str

    GfitAPI({}).preprocess_data(data, Mock())

    assert daterange.call_args_list == [call('1.0', '2.0')]


@patch('gfitpy.gfit_api.datetime')
@patch('gfitpy.gfit_api.DateRange')
@patch.object(GfitAPI, 'process_datapoint')
def test_preprocess_data_calls_datapoint(proc_datapoint, daterange, datetime):
    data = {
        'minStartTimeNs': 1,
        'maxEndTimeNs': 1,
        'point': ['a', 'b']
    }
    d_t = Mock()

    GfitAPI({}).preprocess_data(data, d_t)

    assert proc_datapoint.call_args_list  == [call('a', d_t), call('b', d_t)]


@patch('gfitpy.gfit_api.datetime')
@patch('gfitpy.gfit_api.DateRange')
@patch.object(GfitAPI, 'process_datapoint')
def test_preprocess_data_no_points(proc_datapoint, daterange, datetime):
    data = {
        'minStartTimeNs': 1,
        'maxEndTimeNs': 1,
    }

    GfitAPI({}).preprocess_data(data, Mock())

    assert not proc_datapoint.called


@patch.object(GfitAPI, 'login')
def test_enter_returns_self(login_mock):
    api = GfitAPI({})
    ret = api.__enter__(Mock())

    assert login_mock.call_args_list == [call()]
    assert ret == api


def test_enter_sets_start():
    start = Mock()
    api = GfitAPI({})

    with patch.object(GfitAPI, 'login'):
        api.__enter__(start)
    assert api.start == start


@patch('gfitpy.gfit_api.httplib2')
@patch.object(GfitAPI, 'get_credentials')
@patch('gfitpy.gfit_api.build')
def test_login(build, get_creds, httplib):
    creds = get_creds.return_value
    api = GfitAPI({})

    api.login()

    assert creds.authorize.call_args_list == [call(httplib.Http.return_value)]
    assert build.call_args_list == [call('fitness', 'v1', http=creds.authorize.return_value)]
    assert api.api == build.return_value


@patch.object(GfitAPI, 'refresh_credentials')
@patch('gfitpy.gfit_api.Storage')
def test_credentials_retrieved(storage, refresh_creds):
    GfitAPI({}).get_credentials()

    assert storage.call_args_list == [call('user_credentials')]
    assert storage.return_value.get.call_args_list == [call()]


@pytest.mark.parametrize(
    'storage_get',
    [
        # get returns None
        Mock(return_value=None),
        # get returns an object... which has a truthy invalid
        Mock(return_value=Mock(invalid=True))
    ]
)
def test_credentials_are_refreshed_when_invalid(storage_get):
    with patch.object(GfitAPI, 'refresh_credentials') as refresh_creds,\
        patch('gfitpy.gfit_api.Storage') as storage:
        storage.return_value.get.return_value = storage_get

        api = GfitAPI({})

        ret = api.get_credentials()

    # refresh_credentials was not called
    assert refresh_creds.call_args_list == [call(storage.return_value)]
    assert ret == refresh_creds.return_value

@patch.object(GfitAPI, 'refresh_credentials')
@patch('gfitpy.gfit_api.Storage')
def test_credentials_are_not_touched_when_valid(storage, refresh_creds):
    storage = storage.return_value
    # storage returns something that is valid
    storage.get.return_value = Mock(invalid=False)

    api = GfitAPI({})

    ret = api.get_credentials()

    # refresh_credentials was not called
    assert refresh_creds.call_args_list == []
    assert ret == storage.get.return_value



@patch('gfitpy.gfit_api.argparse')
@patch('gfitpy.gfit_api.tools')
@patch('gfitpy.gfit_api.OAuth2WebServerFlow')
def test_refresh_credentials_creates_flow(oauth, tools, argparse):
    client_id = Mock()
    client_secret = Mock()
    oauth_scope = Mock()
    GfitAPI(
        {'client_id': client_id, 'client_secret': client_secret, 'api_scope': oauth_scope}
    ).refresh_credentials(Mock())

    assert oauth.call_args_list == [call(client_id, client_secret, oauth_scope)]

@patch('gfitpy.gfit_api.argparse')
@patch('gfitpy.gfit_api.tools')
@patch('gfitpy.gfit_api.OAuth2WebServerFlow')
@patch.object(GfitAPI, 'api_scope')
def test_refresh_credentials_runs_flow(api_scope, oauth, tools, argparse):
    storage = Mock()
    flags = argparse.ArgumentParser.return_value.parse_args.return_value

    GfitAPI({}).refresh_credentials(storage)

    assert tools.run_flow.call_args_list == [call(oauth.return_value, storage, flags)]
