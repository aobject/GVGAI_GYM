
# Python Modules
import argparse
import os
from os.path import dirname, abspath, join
from pathlib import Path
import random
import sys

# 3rd Party Modules
import gym

# Local Modules
# Must make sure the GVGAI_GYM is available
# sys.path.insert(0,os.path.dirname(__file__))
import gym_gvgai

def player(state,action_space=6):
    """
    player takes a current state and returns an action
    state (numpy array dtype uint8 shape (90, 130, 4)): the current state of the game as pixel values
    action_space (int): The number of discrete actions your player can take. 
    returns a randomly selected action. 
    """
    return random.randint(0, action_space-1)

def play(level, player, gvgai_path, max_len=1000):
    """
    play allows a player to play one episode of zelda with a custom level and player.
    level (string): Represents the level to be played. The level must be 
                    11 wide, by 7 tall with walls on all sides for a total dimension
                    of 13 wide by 9 tall. 
                    LevelMapping
                        g > floor goal
                        + > floor key        
                        A > floor nokey
                        1 > floor monsterQuick
                        2 > floor monsterNormal
                        3 > floor monsterSlow
                        w > wall
                        . > floor
    player (python function): A python function that takes a game state, takes an action_space,
                                and returns an action. 
                                state (numpy array dtype uint8 shape (90, 130, 4)): the current state of the game as pixel values.
                                action_space (int): The number of discrete actions your player can take. 
                                return: Your function must return an integer representing a discrete action from the action space. 
    gvgai_path (string): A string providing the absolute file path of the GVGAI_GYM repository
                        root folder. For example '/home/user_name/GVGAI_GYM/'
    max_len (integer): Sets the maximum number of steps the player is given. 
    return: if the player wins we return 1.0 otherwise -1.0 is returned. 
    """


    cur = 4
    board = 'gvgai-zelda-lvl{}-v0'.format(cur)

    f = open(Path(gvgai_path)/'gym_gvgai/envs/games/zelda_v0/zelda_lvl{}.txt'.format(cur), 'w')
    f.write(level)
    f.close()

    # print(board in [env.id for env in gym.envs.registry.all() if env.id.startswith('gvgai')])

    env = gym.make(board)

    state = env.reset()
    sum_score = 0
    win = False
    for i in range(max_len):
        # action_id = env.action_space.sample()
        action_id = player(state)
        state, reward, isOver, debug = env.step(action_id)
        sum_score += reward
        # print('Action: {} Reward: {} SumScore: {} Done: {}'.format(action_id, reward, sum_score, isOver))
        if isOver:
            # print('Game over at game tick {}'.format(i+1))
            # print(debug['winner'])
            # print(debug)
            if debug['winner'] == 'PLAYER_WINS':
                win = True
                break
    if win:
        return 1.0  # Return 1 if player wins
    else:
        return -1.0 # Return -1 if player does not win

# gvgai_path = '/Volumes/Data_01/home/g/hybrid/GVGAI_GYM/'

# result = play(level, player, gvgai_path, 1000)

# print(result)

# RESUME HERE # Call from command line with level string

def main():
    opts = argparse.ArgumentParser(
        description='Play level'
    )
    opts.add_argument(
        '-l',
        '--level',
        help='Level to play as a string.',
        default='wwwwwwwwwwwww\nwwA+g....w..w\nwwww........w\nw...w...w..ww\nwww.w2..wwwww\nw.......w...w\nw.2.........w\nw.....2.....w\nwwwwwwwwwwwww'
    )
    opts = opts.parse_args()
    level = opts.level

    gvgai_path = '/Volumes/Data_01/home/g/hybrid/GVGAI_GYM/'

    level = (
    """wwwwwwwwwwwww
    wwA+g....w..w
    wwww........w
    w...w...w..ww
    www.w2..wwwww
    w.......w...w
    w.2.........w
    w.....2.....w
    wwwwwwwwwwwww"""
    )

    result = play(level, player, gvgai_path, 1000)
    # print(result)
    
    return result

if __name__=="__main__":
    print(main())