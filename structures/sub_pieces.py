from .piece import Piece
from .coordinate import Coordinate
from .rules import movement_rules



class Knight(Piece):
    def __init__(self, owner): 
        super().__init__(owner)
        self.piece_type = "Knight"
    
    def rules_abiding(self, start: Coordinate, end: Coordinate) -> bool:
        # Temporary
        return True


class Bishop(Piece):
    def __init__(self, owner):
        super().__init__(owner)    
        self.piece_type = "Bishop"

    def rules_abiding(self, start: Coordinate, end: Coordinate) -> bool:
        return movement_rules['Bishop'](start, end)
