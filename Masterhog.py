"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sum = 0
    num1s = 0
    current_roll = 0
    while(num_rolls>0):
        current_roll = dice()
        if(current_roll == 1):
            num1s+=1
        sum+=current_roll
        num_rolls-=1
    if(num1s>0):
        return num1s
    return sum

    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    #returnns 1 plus the larger digit of the two numbers
    return 1 + max(opponent_score % 10, opponent_score // 10)
    # END PROBLEM 2
def is_prime(score):
    """Return True or False based on whether a number is prime
        >>> is_prime(11)
        True
        >>> is_prime(13)
        True
        >>> is_prime(132)
        False
    """
    if(score == 0 or score == 1):
        return False
    i = 2
    while(i<= score // 2): #divides a number successfully to test if it is prime
        if(score % i == 0):
            return False
        i+=1
    return True
def next_prime(prime):
    """Return the next prime number after a prime
    """
    i = 1
    while(True):
        if(is_prime(prime + i)):
            return prime + i
        i+=1
def hogtimus_prime(score):
    if(is_prime(score)):
        return next_prime(score)
    return score
    
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.
    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if(num_rolls == 0):
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)
    score = hogtimus_prime(score)
    return min(score, 25- num_rolls)
    
def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 3
        roll = dice()
        if(roll % 2 == 0):
            return roll
        else:
            return dice()
        # END PROBLEM 3
    return rerolled

def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).
    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    "*** REPLACE THIS LINE ***"
    if dice_swapped==True:
        dice=four_sided
    else:
        dice=six_sided

    # END PROBLEM 4
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.
    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.
    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.
    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 5
    while (score0<goal) and (score1<goal):
        dice=select_dice(score0, score1, dice_swapped)
        if player==0:
            num_roll=strategy0(score0,score1)
            if num_roll==-1:
                score0+=1
                dice_swapped=not(dice_swapped)
            else:
                round_points=take_turn(num_roll, score1,dice)
                score0+=round_points
                
        elif player==1:
            num_roll=strategy1(score1,score0)
            if num_roll==-1:
                score1+=1
                dice_swapped=not(dice_swapped)
            else:
                round_points=take_turn(num_roll, score0,dice)
                score1+=round_points
                
        #swine swap
        if (score0==score1*2) or (score1==score0*2):
            score0,score1=score1,score0
        player=other(player)
        
    return score0, score1

    # END PROBLEM 5
    

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.
    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.
    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.
    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)
    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)
    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.
    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    score = 0
    while(score<=goal):
        opponent_score = 0
        while(opponent_score<=goal):
            num_rolls=strategy(score, opponent_score)
            check_strategy_roll(score,opponent_score, num_rolls)
            opponent_score += 1
        score+=1
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.
    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.
    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def average_fn(*args):
        i = 0
        sum = 0
        while(i < num_samples):
            sum += fn(*args)
            i+=1
        return sum/num_samples
    return average_fn
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.
    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    max_value=0
    i=10
    while(i>0):
        avg_turn_score=make_averaged(roll_dice,1000)(i,dice)
        if avg_turn_score>=max_value:
            max_value=avg_turn_score
            max_rolls=i
        i-=1
    return max_rolls
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
   
    bacon_score=hogtimus_prime(free_bacon(opponent_score))
    if bacon_score>=margin:
        return 0
    else:
        return num_rolls

    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    bacon_score = hogtimus_prime(free_bacon(opponent_score))
    future_score=score+bacon_score
    if(future_score*2 == opponent_score or bacon_score>=margin):
        return 0
    return num_rolls
    # END PROBLEM 10
check_strategy(swap_strategy)

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    if score==0:
        return -1
        
    
    #setting margins
    if score>90:
        margin=5
    elif score>80:
        margin=7
    elif score>70:
        margin=8
    else:
        margin=10
    
    bacon_score = hogtimus_prime(free_bacon(opponent_score))
    future_score=score+bacon_score

    #forcing beneficial swaps
    if(future_score*2 == opponent_score):
        return 0
    #elif (score*2==opponent_score-1):
        #return -1
        

    #preventing opponent from getting re-rolling dice
    elif (future_score+opponent_score)%7==0:
        return 4

    #preventing opponent from getting a beneficial swap
    elif (opponent_score*2==future_score):
        return 4

    #getting free bacon
    elif bacon_score>=margin:
        return 0
    else:
        return 4

check_strategy(final_strategy)



##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.
    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
