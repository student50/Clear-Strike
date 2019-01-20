from config.settings import TURNS, COIN_TYPES, Results
from player import Player

class CarromBoard():
    """
    Class to Create a carrom board.

    Each carrom board will have specific number of coins and players to start with.

    As the game progresses, turn by turn each players will either gain more points or
    looses their points.

    A player wins the game if his/her score is atlease 5 points and at least, 3 points more
    than the opponent.

    If coins get exhausted and above condition is not met then game is considered as draw

    For further details see the docstring of __init__
    """

    def __init__(self, coins, players):
        """
        Initializes Carrom Board with coins and players

        :param coins: Number and type of coins on the board. ex: {'black_coin':9}
        :type coins: dict

        :param players: List of players playing in game.
        :type players: list

        """
        # Check if coin type passed is valid
        if not type(coins) == dict:
            raise ValueError(f"Type of coins parameter should be a dict and not {type(coins)}")
        for coin in coins:
            if not coin in COIN_TYPES.keys():
                raise ValueError(f"{coin} is not a valid coin type.")

        # Check if type of players is a list and has only player class objects
        if not type(players) == list:
            raise ValueError(f"Type of players parameter should be a list and not {type(players)}")
        for player in players:
            if not type(player) == Player:
                print(f"One of the element in players list is not of type Player. Its of type {type(player)}")
                raise ValueError(f"All the element in list players should be an instance of Player class.")

        self.coins = coins
        self.players = players
        self.game_state = 'NotYetBegan'
        self.winner = None


    def play(self, input_turns=None):
        """
        This is recursive funtion which executes till game ends.

        There are 3 main task of this method,
        
        1. To get user input if input_turns is None
        2. Update player with the input turn
        3. Calculating result after each turn, and checking if game ended. if not repeat

        :param input_turns: dict of players containing list of turns played in order
        :type input_turns: dict

        :return: str Result of the play with statistics.
        """
        # Validate input_turns
        if not input_turns == None and not type(input_turns) == dict:
            raise ValueError(f"input_turns should of type dict and not {type(input_turns)}")

        # Update the game status
        self.game_state = 'InProgress'

        while(self.coin_exists()):
            for player in self.players:
                if not input_turns:
                    # get input from cmd line
                    outcome = self.get_input(player.name)
                else:
                    outcome = input_turns[player.name].pop(0)
                    if not self.is_turn_valid(outcome):
                        raise ValueError(f"Invalid Input turn in {player.name}.txt file")

                # pass input to player
                player.play(outcome)
                
                # update board's coins
                for k, v in TURNS[outcome]['coins_consumed'].items():
                    self.coins[k] -= v

                # Check if any player has won
                if self.has_winner():
                    self.game_state = 'Won'
                    return self.game_state
        
        self.game_state = 'Draw'
        return self.game_state


    def coin_exists(self):
        """
        Checks if any of the coin still exists on the board
        """
        for val in self.coins.values():
            if not val == 0:
                return True

        return False                


    def has_winner(self):
        """
        Checks if any player has won the game.

        For a player to win the game, we have 2 Criteria
        1. Player should have at least 5 points, in total
        2. Player should have at lease 3 points more than opponent

        :return: bool, True if there is a winner. False if not
        """
        points = list(self.get_current_points().values())

        # debug
        print(points)

        # Get max point and remove it from points list
        winner_index = points.index(max(points))
        max_points = points.pop(winner_index)

        # Condition 1 : should have at least 5 points
        if not max_points >= 5:
            return False
        
        # Condition 2 : should have at lease 3 points more than opponent
        for point in points:
            if not max_points - 3 >= point:
                return False

        self.winner = self.players[winner_index]
        return True
    
    def get_current_points(self):
        """
        Retuns current points of all the players in the Board as dict of player name and score

        :return: dict ex: {'Player name': 13, 'player name 2': 10}
        """
        ret = dict()
        for player in self.players:
            ret[player.name] = player.total_points
        
        return ret
    

    def is_turn_valid(self, turn_val):
        """
        Check if the turn value passed is valid w.r.t number of coins present
        """
        for coin, val in TURNS[turn_val]['coins_consumed'].items():
            if self.coins[coin] < val:
                print(f"Chosen turn {turn_val} is not valid as {coin} coin is not enough on the board.")
                print(f"{coin} left on board is : {self.coins[coin]}")
                return False

        return True 


    def get_input(self, player_name):
        """
        Prompt's user to choose various turn options as a turn's outcome.

        Various turn options are:
        1. Strike
        2. MultiStrike
        3. Red strike
        4. Striker strike
        5. Defunct coin
        6. None

        User should input the number corresponding to turn which they want to choose

        Error handing for wrong input is also taken case in this function itself

        :param player_name: name of player to choose the input
        :type player_name: str

        :return: str, Turn Choosed by the player
        """
        turn_output = None
        # Prompt user's Input choices
        print(f"{player_name}: Choose an outcome from the list below")
        for i, turn in enumerate(TURNS.keys()):
            print(f"\t {i+1}. {turn}")

        # Get the input
        while True:
            outcome = input(">")
            # Prompt again if valid input is not given
            if not outcome.isdigit() or not int(outcome) in range(1, len(TURNS.keys())+1):
                print(f"Invalid Input!! Please choose any number from 1 to {len(TURNS.keys())}")
                continue

            # Compute turn output
            outcome = int(outcome)
            turn_output = list(TURNS.keys())[outcome-1]

            if not self.is_turn_valid(turn_output):
                print("Please choose another input")
                continue
            
            break

        return turn_output


    def results(self):
        """
        Returns results based on the game state.
        Returns a object of Results (a namedtuple in settings file)

        Game States are:
        1. 'NotYetBegan' - If play is not yet started
        2. 'InProgress' - If play has started but still in progress
        3. 'Draw' - If game is ended but match is draw
        4. 'Won' - If game is ended and we have a winner

        :return: Results('outcome', 'player', 'statistics') 
        """

        # Populating statistics
        statistics = "-".join(str(i) for i in self.get_current_points().values())

        if self.game_state in ['InProgress', 'Draw', 'NotYetBegan', 'Won']:
            return Results(self.game_state, self.winner, statistics)
        else:
            raise ValueError(f"game_state value is {self.game_state}, Which is not valid state!!")
        