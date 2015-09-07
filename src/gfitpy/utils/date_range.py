import datetime

class DateRange(object):
    near_time = datetime.timedelta(seconds=10*60)

    def __init__(self, start, end):
        assert start < end
        self._start, self._end = start, end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def duration(self):
        return self.end - self.start

    def near(self, other):
        '''
        Similar to contains, but returns if they are within ten minutes of each other
        '''
        # create a copy with 5 minutes on either side
        wider_reach_date = DateRange(self.start - self.near_time, self.end + self.near_time)
        return other in wider_reach_date


    def __contains__(self, other):
        '''
        `x in my_date_range` will return true if `x` intersects the date range. If x is a datetime
        object, then it simply checks if it is in the middle. If x is another DateRange it checks
        whether the two intersect. So say your ranges look like so:

        my_date_range:      |------------|
        x:          |-----------|
        y:              |-------------------|
        z:                       |----|

        All three x, y and z will return True.
        '''
        if isinstance(other, DateRange):
            return self.start <= other.end and other.start <= self.end
        elif isinstance(other, datetime.datetime):
            return self.start <= other <= self.end
        else:
            raise NotImplementedError('Cannot compare DateRange and {0}'.format(type(other)))

    def __lt__(self, other):
        '''
        this is smaller than the other if its start time is earlier. if they're identical
        then it looks at the end times
        '''
        if self.start == other.start:
            return self.end < other.end
        else:
            return self.start < other.start

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    # don't bother testing str and repr - they're boring functions
    def __str__(self): # pragma: no cover
        # trim the microseconds from timedelta - no-one cares about those anyway!
        trimmed_duration = datetime.timedelta(seconds=int(self.duration.total_seconds()))
        return 'DateRange s={0} d={1}'.format(self.start, trimmed_duration)

    def __repr__(self): # pragma: no cover
        return '{cls}(start={s!r}, end={e!r})'.format(
            cls=self.__class__.__name__,
            s=self.start,
            e=self.end
        )

    def combine(self, other):
        '''
        Return a new DateRange that encompasses both this DateRange and the Other
        '''
        return DateRange(
            start=min(self.start, other.start),
            end=max(self.end, other.end)
        )
