from Chess_Project.Chess.model.game_state_class import GameState
import copy as c

class ChessModel():

    def __init__(self):
        self.square_selected = ()  # a tuple to store the coordinates of pieces selected
        self.player_clicks = []  # keeps track of player_clicks  (example [(6,1), (4, 1)] )
        self.valid_moves = []  # list of valid moves

        self.game_over = False
        self.animate = False
        self.move_made = False  # flag variable for when a move is made

        self.running = True

        self.game_state = GameState()
        self.valid_moves = self.game_state.get_valid_moves()

        self.white_player = True
        self.black_player = True

    def update(self, move):
        pass
