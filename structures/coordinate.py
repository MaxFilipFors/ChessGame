from .piece import Piece
from typing import Optional

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.current_piece: Optional[Piece] = None

    def add_piece_to_coordinate(self, piece: Piece):
        if self.occupied:
            raise ValueError("Coordinate is already occupied.")
        self.current_piece = piece
        self.occupied = True

    def remove_piece_from_coordinate(self):
        if not self.occupied:
            raise ValueError("Coordinate is unoccupied.")
        self.current_piece = None
        self.occupied = False

    # Need a comparison function on this one
    def __eq__(self, other) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return self.x == other.x and self.y == other.y
