"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import logging

non_legal_moves = (-1, -1)

# Set up the logging
logging.basicConfig(filename='log_file.log', level=logging.DEBUG)


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def improved_weighted_score(game, player):
    """Implement weight on improved_score function

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    value = float(my_moves - 1.5 * opp_moves)
    return value
    #logging.debug("eval_fn value is {} for my_move :{} and opp_moves : {}".format(value, my_moves, opp_moves))


def ratio_weighted_score(game, player):
    """Implement weight on improved_score function

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    value = float('inf') if opp_moves == 0 else (my_moves / (1.5 * opp_moves))
    return value
    #logging.debug("eval_fn value is {} for my_move :{} and opp_moves : {}".format(value, my_moves, opp_moves))


def ratio_weighted(game, player):
    """Implement weight on improved_score function

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    blank_spaces = len(game.get_blank_spaces())
    value = float('inf') if opp_moves == 0 else float(my_moves / 1.5 * opp_moves)
    return value
    logging.debug("eval_fn value is {} for my_move :{} and opp_moves : {}".format(value, my_moves, opp_moves))


def ratio_plus_my_moves_weight_score(game, player):
    """Implement weight on improved_score function

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    blank_spaces = len(game.get_blank_spaces())
    value = float('inf') if opp_moves == 0 else float(my_moves / opp_moves + my_moves / blank_spaces)
    return value
    #logging.debug("eval_fn value is {} for my_move :{} and opp_moves : {}".format(value, my_moves, opp_moves))


def custom_score(game, player, eval_fn=ratio_plus_my_moves_weight_score):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return eval_fn(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        #logging.debug('Time left : {}'.format(self.time_left))

        # if no legal move return (-1,-1)
        if not legal_moves:
            return non_legal_moves

        # choose random move at start
        move = legal_moves[random.randint(0, len(legal_moves) - 1)]
        score = float("-inf")

        # Perform any required initializations, including selecting an initial
        # Returning immediately if there are no legal moves
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.method == "alphabeta":
                search_method = self.alphabeta
                logging.debug("Alphabeta was called.")
            else:
                search_method = self.minimax
                logging.debug("Minimax was called.")

            if self.iterative:
                self.search_depth = 1
                while score is not float("inf"):
                    score, move = max(search_method(game, self.search_depth), (score, move))
                    self.search_depth += 1

            else:
                score, move = max(search_method(game, self.search_depth), (score, move))


        except Timeout:
            # Handle any actions required at timeout, if necessary
            logging.debug("Time limit was reached so move : {} was passed. ".format(move))
            return move

        # Return the best move from the last completed search iteration
        logging.debug("Search Depth: {}, best move: {}, with score of {}".format(self.search_depth, move, score))
        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self), non_legal_moves

        if maximizing_player is True:
            minmax_eval_func = max
            score = float("-inf")
        else:
            minmax_eval_func = min
            score = float("inf")

        best_move = (-1, -1)

        for move in game.get_legal_moves():
            temp_score, _ = self.minimax(game.forecast_move(move), depth - 1, not maximizing_player)
            score, best_move = minmax_eval_func((score, best_move), (temp_score, move))
        return score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if maximizing_player:
            return self.max_value(game, depth, alpha, beta)
        else:
            return self.min_value(game, depth, alpha, beta)

    def max_value(self, game, depth, alpha, beta):
        """Implement max search for alpha-beta and min_max.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self), (-1, -1)
        best_score = float("-inf")
        best_move = (-1, -1)
        for move in game.get_legal_moves(self):
            temp_score, _ = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if temp_score > best_score:
                best_score, best_move = temp_score, move
                if alpha < best_score:
                    alpha = best_score
            if best_score >= beta:
                return best_score, best_move
        return best_score, best_move

    def min_value(self, game, depth, alpha, beta):
        """Implement min search of alpha-beta and minmax.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

       Returns
        -------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self), non_legal_moves
        best_score = float("inf")
        best_move = non_legal_moves
        for move in game.get_legal_moves(game.get_opponent(self)):
            temp_score, _ = self.max_value(game.forecast_move(move), depth - 1, alpha, beta)
            if temp_score < best_score:
                best_score, best_move = temp_score, move
                if beta > best_score:
                    beta = best_score
            best_score, best_move = min((best_score, best_move), (temp_score, move))
            if best_score <= alpha:
                return best_score, best_move
        return best_score, best_move
