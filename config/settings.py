# Foul details
MAX_FOUL_COUNT = 3
FOUL_PENALTY_POINTS = -1 
FOUL_TURNS = ['Striker strike', 'Defunct coin']

# Missed pocket details
MAX_MISSED_COUNT = 3
MISSED_PENALTY_POINTS = -1
MISSED_TURNS = ['Striker strike', 'Defunct coin', 'None']

# Types of coins
COIN_TYPES = {
    'black_coin': {
        'name': 'Black Coin',
    },
    'red_coin': {
        'name': 'Red Coin',
    }
}

# Types of turns
TURNS = {
    'Strike': {
        'points': 1,
        'coins_consumed': {
            'black_coin': 1
        }
    },
    'MultiStrike': {
        'points': 2,
        'coins_consumed': {
            'black_coin': 2
        }
    },
    'Red strike': {
        'points': 3,
        'coins_consumed': {
            'red_coin': 1
        }
    },
    'Striker strike': {
        'points': -1,
        'coins_consumed': {}
    },
    'Defunct coin': {
        'points': -2,
        'coins_consumed': {
            'black_coin': 1
        }
    },
    'None': {
        'points': 0,
        'coins_consumed': {}
    }
}

# Results
from collections import namedtuple
Results = namedtuple('Result', ['outcome', 'player', 'statistics'])
