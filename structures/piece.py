class Piece:
    unique_id_counter = 0
    def __init__(self, owner):
        self.unique_id = Piece.get_next_unique_id()
        self.owner = owner

    @classmethod
    def get_next_unique_id(cls):
        cls.unique_id_counter += 1
        return cls.unique_id_counter
    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.unique_id == other.unique_id