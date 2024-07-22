from .functions import is_move_valid
from .params import board_height, board_width, total_knights, total_bishops
from .structures.sub_pieces import Knight, Bishop, Coordinate
from .structures.board import Board

class Game_state_machine:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        pieces = []
        for i in range(total_knights):
            owner = player1 if i % 2 == 0 else player2
            pieces.append(Knight(owner=owner))

        for i in range(total_bishops):
            owner = player1 if i % 2 == 0 else player2
            pieces.append(Bishop(owner=owner))
        
        self.board = Board(board_height, board_width, pieces)

    def move_piece(self, player, original_coordinate: Coordinate, destination_coordinate: Coordinate):
        error = is_move_valid(self.board, player, original_coordinate, destination_coordinate)
        if error:
            print(f"Error: {error}")
            return
        
        piece_to_move = self.board.get_piece_at_coordinate(original_coordinate)
        
        if not piece_to_move.rules_abiding(original_coordinate, destination_coordinate):
            print(f"{piece_to_move.piece_type}s cannot move this way.")
            return
        
        # Check if there is an enemy piece on the destination, if so remove it
        piece_at_destination = self.board.get_piece_at_coordinate(destination_coordinate)
        if piece_at_destination is not None and piece_at_destination.owner != player:
            self.board.handle_removal(piece_at_destination)

        original_coordinate = self.board.coordinate_map.get((original_coordinate.x, original_coordinate.y))
        destination_coordinate = self.board.coordinate_map.get((destination_coordinate.x, destination_coordinate.y))

        if original_coordinate and destination_coordinate:
            destination_coordinate.add_piece_to_coordinate(piece_to_move)
            
            original_coordinate.current_piece = None
            original_coordinate.occupied = False
            

