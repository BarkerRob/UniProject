"""
Notes:
    Result criteria
    0 - 1.2 is a loss
    1.11 - 1.89 is a draw
    1.9 - 3.0 is a win

    I need to convert the win/draw/loss into a value between 0 and 1.
    Initial thoughts are below:
        A loss by 3+ goals
        A loss by 1-2 goals
        A draw is 0.5
        A win by 1-2 goals
        A win by 3+ goals

    Criteria to determine the result:
        Recent form, last 5 games
        Distance travelled, calculated by distance between stadiums
        Form against opponent, last 5 games, if possible
        Last years league position compared to opponents
        Current league position compared to opponents

        Possible inclusions:
            Goal difference of current season compared to opponent

Possible implementation:
    Function for each criteria, they can return a value between 0-1 each. The final value is determined from 3
    A main function which chooses, at random, 3 criteria - this is the random forest element to the code.
    The main function returns the result
    Example of this:
        Main:
            Recent form - returns 0.9
            Distance travelled - returns 0.1
            Form against opponent - returns 0.7
            Total is 1.7 which is a draw according to result criteria at the top.
"""
