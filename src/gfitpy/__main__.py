import sys
import logging
import datetime

from .gfit_api import GfitAPI

CLIENT_ID = 'abc'
CLIENT_SECRET = 'def'


def main(argv=()):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Some sample code for gfitpy - starts up, and executes.
    Gets calorie and activity data for the last ten days.
    """

    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    start_time = datetime.datetime.now() - datetime.timedelta(days=10)

    gfit = GfitAPI(
        settings={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    )

    with gfit(start_time):
        cal_data = gfit.get_cal_data()
        act_data = gfit.get_activity_data()

    import pdb
    pdb.set_trace()
    print(cal_data)
    print(act_data)
    print(argv)
    return 0

if __name__ == "__main__":
    sys.exit(main())
