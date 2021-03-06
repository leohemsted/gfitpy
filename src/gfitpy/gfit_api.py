import httplib2
import argparse
from datetime import datetime

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from .utils.date_range import DateRange


class GfitAPI(object):
    api_scope = None

    def __init__(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = {}
        settings = self.default_settings()
        settings.update(settings_dict)

        self.client_id = settings['client_id']
        self.client_secret = settings['client_secret']
        self.api_scope = settings['api_scope']

        self.start = settings['start_time']
        self.api = None
        self.credentials = None
        self.authed_http = None
        super().__init__()

    @staticmethod
    def default_settings():
        return {
            'client_id': 'MY_CLIENT_ID',
            'client_secret': 'MY_CLIENT_SECRET',
            'api_scope': 'https://www.googleapis.com/auth/fitness.activity.read',
            # if not specified, take the data from the earliest time known to man, the beginning of the modern epoch
            'start_time': datetime(1970, 1, 1)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass

    def get_credentials(self):
        storage = Storage('user_credentials')

        cred = storage.get()
        if cred is None or cred.invalid:
            cred = self.refresh_credentials(storage)
        return cred

    def refresh_credentials(self, storage):
        flow = OAuth2WebServerFlow(
            self.client_id,
            self.client_secret,
            self.api_scope
        )
        # google requires me to give an argparser for flags,
        # although I know i'll be passing none in
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()
        return tools.run_flow(flow, storage, flags)

    def login(self):
        # code liberated from:
        #  https://cloud.google.com/appengine/docs/python/endpoints/access_from_python
        self.credentials = self.get_credentials()

        self.authed_http = self.credentials.authorize(httplib2.Http())
        self.api = build('fitness', 'v1', http=self.authed_http)
        return self.__enter__()

    def _get_fit_data(self, data_source, data_type):
        response = self.api.users().dataSources().datasets().get(
            userId='me',
            dataSourceId=data_source,
            datasetId=self.get_time_range_str(self.start, datetime.now())
        ).execute()

        return self.preprocess_data(response, data_type)

    def get_cal_data(self):
        data = 'derived:com.google.calories.expended:com.google.android.gms:from_activities'
        return self._get_fit_data(data_source=data, data_type='fpVal')

    def get_activity_data(self):
        data = 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments'
        return self._get_fit_data(data_source=data, data_type='intVal')

    @staticmethod
    def process_datapoint(point, data_type):
        # no idea what might trip this one up
        if len(point['value']) != 1:
            raise ValueError(
                'can only handle one value in a point, instead found {0}'.format(
                    point
                )
            )

        start_ns = float(point['startTimeNanos'])
        end_ns = float(point['endTimeNanos'])

        start = datetime.fromtimestamp(start_ns / 1e9)
        end = datetime.fromtimestamp(end_ns / 1e9)

        # the calories burnt between start and end
        return {
            'times': DateRange(start, end),
            'value': point['value'][0][data_type]
        }

    def preprocess_data(self, data, data_type):
        global_start = datetime.fromtimestamp(float(data['minStartTimeNs']) / 1e9)
        global_end = datetime.fromtimestamp(float(data['maxEndTimeNs']) / 1e9)

        if 'point' in data:
            points = [self.process_datapoint(point, data_type) for point in data['point']]
        else:
            points = []

        return {
            'times': DateRange(global_start, global_end),
            'data': points
        }

    @staticmethod
    def get_time_range_str(start, end):
        # google accepts timestamps in nanoseconds
        start = int(start.timestamp() * 1e9)
        end = int(end.timestamp() * 1e9)
        return '{s}-{e}'.format(s=start, e=end)
