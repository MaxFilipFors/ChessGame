from .coordinate import Coordinate
from .piece import Piece
from typing import Optional, List, Dict



class Board:
    def __init__(self, board_height, board_width, pieces: List[Piece]):
        self.board_height = board_height
        self.board_width = board_width
        self.coordinates = []
        self.coordinates : List[Coordinate] = [Coordinate(x, y) for y in range(board_width) for x in range(board_height)]
        self.current_pieces: List[Piece] = pieces
        self.coordinate_map: Dict[tuple, Coordinate] = {(coordinate.x, coordinate.y): coordinate for coordinate in self.coordinates}
        for piece in pieces:
            for coordinate in self.coordinates:
                if not coordinate.occupied:
                    coordinate.add_piece_to_coordinate(piece)
                    break
    '''
    # Remove a piece from the board
    def handle_removal(self, piece: Piece):
        for coordinate in self.coordinates:
            if coordinate.current_piece == piece:
                coordinate.remove_piece_from_coordinate()
                self.current_pieces.remove(piece)
                break
    '''
    def handle_removal(self, piece: Piece):
        found = False
        for coordinate in self.coordinates:
            if coordinate.current_piece == piece:
                print(f"Removing piece: {piece}")
                coordinate.remove_piece_from_coordinate()
                found = True
                break
        
        if found:
            if piece in self.current_pieces:
                print(f"Removing from current_pieces: {piece}")
                self.current_pieces.remove(piece)
            else:
                print(f"Piece not in current_pieces: {piece}")
        else:
            print(f"Piece not found on board: {piece}")
            raise ValueError("Piece not found on the board")
        

    # Standard getter
    def get_piece_at_coordinate(self, coordinate: Coordinate) -> Optional[Piece]:
        coordinate = self.coordinate_map.get((coordinate.x, coordinate.y))
        return coordinate.current_piece if coordinate else None