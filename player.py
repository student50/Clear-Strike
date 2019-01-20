import os
from config.settings import *

class Player():
    """
    Class to create a player to play game.

    For more details see docstring of __init__
    """

    def __init__(self, name):
        """
        Initializes Player with name and default points and foul values

        :param name: name, to identify players.
        :type name: str

        """
        self.name = name
        self.total_points = 0
        self.fouls_count = 0
        self.missed_count = 0
    

    def play(self, turn_val):
        """
        This method is called for each turn of player

        Does 3 jobs:
        1. Updates player's points
        2. If its a foul, updates foul_count
        3. If its a miss, updates missed_count

        :return: turn output i,e one of TURNS dict element in config/settings
        """

        # update player's points
        self.total_points += TURNS[turn_val]['points']

        # Update foul count
        self.update_fouls(turn_val)        
        
        # update misses counts
        self.update_misses(turn_val)

        return turn_val


    def update_fouls(self, turn_val):
        """
        Checks if given turn is a foul or not. If it is then updates points and foul count
        A foul is a turn where a player loses, at least, 1 point

        :param turn_val: one of turn in TURNS dict in config
        :type turn_val: str

        :return: bool, True if it is a foul and false otherwise
        """

        if turn_val in FOUL_TURNS:
            # Increment fouls_count
            self.fouls_count += 1

            # If foul count reached max foul count
            if self.fouls_count == MAX_FOUL_COUNT:
                # Update total_count
                self.total_points += FOUL_PENALTY_POINTS 
                # reset the foul count
                self.fouls_count = 0
            
            return True
        else:
            # reset the foul count as current turn is not a foul
            self.fouls_count = 0
        
        return False
    

    def update_misses(self, turn_val):
        """
        Checks if given turn is a miss or not. If its miss then updates foul count and points accordingly.
        A miss is a turn where a player doesn't pockets a coin

        :param turn_val: one of turn in TURNS dict in config
        :type turn_val: str

        :return: bool, True if it is a miss and false otherwise
        """
        if turn_val in MISSED_TURNS:
            # Increment fouls_count
            self.missed_count += 1

            # If foul count reached max foul count
            if self.missed_count == MAX_MISSED_COUNT:
                # Update total_count
                self.total_points += MISSED_PENALTY_POINTS 
                # reset the missed count
                self.missed_count = 0
            
            return True
        else:
            # reset the missed count as current turn is not a missed turn
            self.missed_count = 0
        
        return False
    
    def __repr__(self):
        """
        Overwriting buildin function __repr__

        :return: Player(name='Player_name', score:14)
        """

        return f"Player(name={self.name}, score={self.total_points})"
