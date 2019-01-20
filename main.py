from carromBoard import CarromBoard
from player import Player
from config.settings import TURNS
import sys, argparse, os

def load_turns(filename):
    """
    Loads truns stored in file with name <player.name>.txt
    """
    turns = list()
    try:
        with open(filename, 'r') as f_turns:
            for line in f_turns:
                if line.strip() in TURNS:
                    turns.append(line.strip())
                else:
                    raise ValueError(f"Invalid Turn '{line.strip()}' in file {filename}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        raise ValueError(f"{filename} No such file exits")
    
    return turns

def main(player_1_name, player_2_name, input_turns):
    """
    Main program where the Clear Strike Game starts
    """
    print("Starting Clear Strike Game!!")

    print("Initializing a Carrom Board.")
    # Initial coin details for a Carrom Board
    coins = {
        'black_coin': 9,
        'red_coin': 1
    }

    # Initializing players
    player_1 = Player(player_1_name)
    player_2 = Player(player_2_name)
    players = [player_1, player_2]

    carrom_board = CarromBoard(coins=coins, players=players)
    print("Carrom Board created!!")

    print("Start Playing")
    result = carrom_board.play(input_turns)
    print("Game Ended!!")

    print('--------- RESULTS ---------')
    result = carrom_board.results()
    if result.outcome == 'Won':
        print(f"{result.player.name} has won the game. Final Score: {result.statistics}")
    elif result.outcome == 'Draw':
        print(f"The Game is Draw with Final score: {result.statistics}")
    print('---------------------------')


if __name__ == '__main__':

    # initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_1", "-p1", help="File containing turns of player 1, One turn in each line. Filename will be player name")
    parser.add_argument("--player_2", "-p2", help="File containing turns of player 2, One turn in each line. Filename will be player name")
    # parser.add_argument("--output", "-o", help="File in which output should be stored")
    args = parser.parse_args()

    # Check arguments
    if args.player_1 or args.player_2:
        if not (args.player_1 and args.player_2):
            print("both optional arguments i,e -p1 -p2 should be present")
            sys.exit(1)

    # load inputs turns if exists
    input_turns = dict()
    p1_name = 'Player 1'
    p2_name = 'Player 2'
    if args.player_1 and args.player_2:
        head_1, tail_1 = os.path.split(args.player_1)
        head_2, tail_2 = os.path.split(args.player_2)
        p1_name = tail_1.split(".")[0]
        p2_name = tail_2.split(".")[0]
        if tail_1 == tail_2:
            print("Both file name are same. As filename will be the player's name, it has to be different")
            sys.exit(1)
        input_turns[p1_name] = load_turns(args.player_1)
        input_turns[p2_name] = load_turns(args.player_2) 

    # Start the Game
    main(p1_name, p2_name, input_turns)
    
     