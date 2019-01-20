from unittest import TestCase
from player import Player
from config import settings

class TestPlayer(TestCase):

    def setUp(self):
        # Create a player
        self.player = Player('Test Player')

    def test_update_fouls(self):
        print("In update_fouls() method testing")
        for turn in settings.FOUL_TURNS:
            print(f"Testing for {turn}")
            # fouls count before
            b_count = self.player.fouls_count

            # calling function
            ret = self.player.update_fouls(turn)

            # test return value is True
            self.assertTrue(ret)

            # Test if incremented in mod 3
            self.assertEqual(self.player.fouls_count, (b_count+1) % settings.MAX_FOUL_COUNT)

    
    def test_update_misses(self):
        print("In update_misses() method testing")
        for turn in settings.MISSED_TURNS:
            print(f"Testing for {turn}")
            # fouls count before
            b_count = self.player.missed_count

            # calling function
            ret = self.player.update_misses(turn)

            # test return value is True
            self.assertTrue(ret)

            # Test if incremented in mod 3
            self.assertEqual(self.player.missed_count, (b_count+1) % settings.MAX_MISSED_COUNT)

    def test_play(self):
        print("In play() method testing")
        for turn in settings.TURNS:
            print(f"testing for {turn}")
            # before 
            b_points = self.player.total_points
            b_fouls = self.player.fouls_count
            b_misses = self.player.missed_count

            # calling function
            self.player.play(turn)

            # test parameter
            a_points = b_points + settings.TURNS[turn]['points']
            if turn in settings.FOUL_TURNS:
                if self.player.fouls_count == 0: a_points += settings.FOUL_PENALTY_POINTS
                self.assertEqual(self.player.fouls_count, (b_fouls+1) % settings.MAX_FOUL_COUNT)
            if turn in settings.MISSED_TURNS:
                if self.player.missed_count == 0: a_points += settings.MISSED_PENALTY_POINTS
                self.assertEqual(self.player.missed_count, (b_misses+1) % settings.MAX_MISSED_COUNT)
            self.assertEqual(self.player.total_points, a_points)
        