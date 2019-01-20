from unittest import TestCase
from player import Player
from carromBoard import CarromBoard
from config import settings

class TestCarromBoard(TestCase):

    def setUp(self):
        print("Initializing a Carrom Board.")
        # Initial coin details for a Carrom Board
        coins = {
            'black_coin': 9,
            'red_coin': 1
        }

        # Initializing players
        player_1 = Player(name='Player 1')
        player_2 = Player(name='Player 2')
        players = [player_1, player_2]

        self.carrom_board = CarromBoard(coins=coins, players=players)
        print("Carrom Board created!!")
    
    def test_creation(self):

        # invaid coins param testing
        with self.assertRaises(ValueError):
            CarromBoard('invalid_datatype', [Player('player 1')])
        with self.assertRaises(ValueError):
            CarromBoard({'invalid_coin': 3}, [Player('player 1')])
        
        # invalid players param testing
        with self.assertRaises(ValueError):
            CarromBoard({'black_coin':9}, Player('Invalid type'))
        with self.assertRaises(ValueError):
            CarromBoard({'black_coin':3}, [Player('Player 1'), 'Not a player'])
        
        # Check the game state
        self.assertEqual(self.carrom_board.game_state, 'NotYetBegan')
    
    