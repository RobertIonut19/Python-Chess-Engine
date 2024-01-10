from .game_state_class import GameState


class ChessModel:
    """
    Represents the model of the chess game, managing game state and player interactions.

    Attributes:
        - square_selected (tuple): Stores the coordinates of the selected piece.
        - player_clicks (list): Keeps track of player clicks as tuples (e.g., [(6, 1), (4, 1)]).
        - valid_moves (list): List of valid moves for the current game state.
        - game_situation (str): Represents the current situation of the game (e.g., "menu", "playing").
        - game_over (bool): True if the game is over, False otherwise.
        - animate (bool): True if animations are enabled, False otherwise.
        - move_made (bool): Flag variable indicating whether a move has been made.
        - running (bool): True if the game is running, False otherwise.
        - game_state (GameState): An instance of the GameState class representing the current state of the game.
        - white_player (bool): True if the white player is human, False if AI.
        - black_player (bool): True if the black player is human, False if AI.

    Methods:
        - update(move): Update the game state after a move is made.

    """

    def __init__(self):
        """
           Initializes the ChessModel with default attributes and an instance of the GameState class.
        """
        self.square_selected = ()  # a tuple to store the coordinates of pieces selected
        self.player_clicks = []  # keeps track of player_clicks  (example [(6,1), (4, 1)] )
        self.valid_moves = []  # list of valid moves

        self.game_situation = "menu"

        self.game_over = False
        self.animate = False
        self.move_made = False  # flag variable for when a move is made

        self.running = True

        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()

        self.white_player = True
        self.black_player = True

    def update(self, move):
        """
            Update the game state after a move is made.
            Args:
                move (Move): The move to be made.
        """
        self.game_state.make_move(move)
        self.move_made = True
        self.animate = True
