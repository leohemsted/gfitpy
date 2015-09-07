from enum import Enum

class Activity(Enum):
    '''
    As defined here:
    https://developers.google.com/fit/rest/v1/reference/activity-types
    Only storing the ones I actually handle for now
    '''
    in_vehicle = 0
    biking = 1
    on_foot = 2
    still_not_moving = 3
    unknown_unable_to_detect_activity = 4
    tilting_sudden_device_gravity_change = 5
    walking = 7
    running = 8
    aerobics = 9
    zumba = 10
    badminton = 10
    baseball = 11
    basketball = 12
    biathlon = 13
    handbiking = 14
    mountain_biking = 15
    road_biking = 16
    spinning = 17
    stationary_biking = 18
    utility_biking = 19
    boxing = 20
    calisthenics = 21
    circuit_training = 22
    cricket = 23
    dancing = 24
    elliptical = 25
    fencing = 26
    football_american = 27
    football_australian = 28
    football_soccer = 29
    frisbee = 30
    gardening = 31
    golf = 32
    gymnastics = 33
    handball = 34
    hiking = 35
    hockey = 36
    horseback_riding = 37
    housework = 38
    jumping_rope = 39
    kayaking = 40
    kettlebell_training = 41
    kickboxing = 42
    kitesurfing = 43
    martial_arts = 44
    meditation = 45
    mixed_martial_arts = 46
    p90x_exercises = 47
    paragliding = 48
    pilates = 49
    polo = 50
    racquetball = 51
    rock_climbing = 52
    rowing = 53
    rowing_machine = 54
    rugby = 55
    jogging = 56
    running_on_sand = 57
    running_treadmill = 58
    sailing = 59
    scuba_diving = 60
    skateboarding = 61
    skating = 62
    cross_skating = 63
    inline_skating_rollerblading = 64
    skiing = 65
    back_country_skiing = 66
    cross_country_skiing = 67
    downhill_skiing = 68
    kite_skiing = 69
    roller_skiing = 70
    sledding = 71
    sleeping = 72
    snowboarding = 73
    snowmobile = 74
    snowshoeing = 75
    squash = 76
    stair_climbing = 77
    stair_climbing_machine = 78
    stand_up_paddleboarding = 79
    strength_training = 80
    surfing = 81
    swimming = 82
    swimming_swimming_pool = 83
    swimming_open_water = 84
    table_tennis_ping_pong = 85
    team_sports = 86
    tennis = 87
    treadmill_walking_or_running = 88
    volleyball = 89
    volleyball_beach = 90
    volleyball_indoor = 91
    wakeboarding = 92
    walking_fitness = 93
    nording_walking = 94
    walking_treadmill = 95
    waterpolo = 96
    weightlifting = 97
    wheelchair = 98
    windsurfing = 99
    yoga = 100
    diving = 102
    ergometer = 103
    ice_skating = 104
    indoor_skating = 105
    curling = 106
    other_unclassified_fitness_activity = 108
    light_sleep = 109
    deep_sleep = 110
    rem_sleep = 111
    awake_during_sleep_cycle = 112


    def valid(self):
        '''
        Returns true if the current value is in the following list of supported vals
        '''
        return self in (
            Activity.biking,
            Activity.walking,
            Activity.running,
        )

    @property
    def mfp_id(self):
        if self == Activity.biking:
            return 19
        elif self == Activity.walking:
            # Walking, 12.5 mins per km, mod. pace
            return 26688321
        elif self == Activity.running:
            # Running (jogging), 10.7 kph (5.6 min per km)
            return 127
        else:
            raise NotImplementedError('We do not know the myfitnesspal ID for {0}'.format(self))
