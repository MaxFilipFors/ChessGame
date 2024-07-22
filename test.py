import pytest
from .structures.sub_pieces import Bishop, Knight
from .structures.board import Board
from .structures.coordinate import Coordinate
from .functions import is_move_valid, is_diagonal_move, is_path_unobstructed, is_within_board
from .game_state_machine import Game_state_machine

@pytest.fixture
def setup_game():
    # Setup a game with two players
    player1 = "Player1"
    player2 = "Player2"
    
    game = Game_state_machine(player1, player2)
    return game, player1, player2

def test_initialization(setup_game):
    # Setup
    game, player1, player2 = setup_game

    # Test board initialization
    assert len(game.board.coordinates) == 64
    assert len(game.board.current_pieces) == 4
    
    # Check that the coordinate map is correctly initialized
    for coordinate in game.board.coordinates:
        assert game.board.coordinate_map[(coordinate.x, coordinate.y)] == coordinate

    
    knights = [p for p in game.board.current_pieces if p.piece_type == "Knight"]
    bishops = [p for p in game.board.current_pieces if p.piece_type == "Bishop"]
    
    # Test that all pieces are initalized
    assert len(knights) == 2
    assert len(bishops) == 2
    
    # Test that they have owners
    for piece in knights + bishops:
        assert piece.owner in [player1, player2]

# This particular test may be superfluous
def test_piece_ownership():
    # Setup
    player1 = "Player1"
    player2 = "Player2"
    knight = Knight(owner=player1)
    bishop = Bishop(owner=player2)
    
    # Test correct owner
    assert knight.owner == player1
    assert bishop.owner == player2

def test_coordinate_equality():
    # Setup 
    coord1 = Coordinate(1, 2)
    coord2 = Coordinate(1, 2)
    coord3 = Coordinate(2, 3)
    
    # Test Comparison
    assert coord1 == coord2
    assert coord1 != coord3

def test_piece_id():
    # Setup
    piece1 = Knight(owner="Player1")
    piece2 = Bishop(owner="Player2")
    
    # Test Comparison
    assert piece1.unique_id != piece2.unique_id

def test_handle_removal():
    # Setup
    pieces = [Knight(owner="Player1"), Bishop(owner="Player2")]
    board = Board(8, 8, pieces)
    incorrect_piece = Knight(owner="Player1")
    piece_to_remove = pieces[0]

    # Test Correct Removal
    board.handle_removal(piece_to_remove)
    assert piece_to_remove not in board.current_pieces

    for coordinate in board.coordinates:
        if coordinate.current_piece == piece_to_remove:
            assert coordinate.current_piece is None
            assert not coordinate.occupied

    # Test Incorrect Removal
    try:
        board.handle_removal(incorrect_piece)
        assert False 
    except ValueError:
        assert True

def test_is_diagonal_move():
    # Setup
    start = Coordinate(0, 0)
    end = Coordinate(3, 3)
    
    # Check a diagonal move 
    assert is_diagonal_move(start, end)
    
    # Check a non-diagonal move
    end = Coordinate(3, 4)
    assert not is_diagonal_move(start, end)

def test_is_path_unobstructed():
    # Setup
    knight = Knight(owner="Player1")
    knight2 = Bishop(owner="Player1")
    bishop = Bishop(owner="Player2")
    pieces = [knight, knight2, bishop]
    board = Board(8, 8, pieces)
    start = Coordinate(0, 0)
    end = Coordinate(3, 3)
    
    if not start.occupied:
        start.add_piece_to_coordinate(knight)
    
    if not end.occupied:
        end.add_piece_to_coordinate(bishop)

    # Check without Pieces
    assert is_path_unobstructed(start, end, board) is None
    
    # Check Enemy Bishop
    board.coordinate_map[(2, 2)].add_piece_to_coordinate(bishop)
    assert is_path_unobstructed(start, end, board) == "Move blocked by another piece"

    # Check Friendly Knight, after removing the bishop
    board.handle_removal(bishop)
    board.coordinate_map[(1, 1)].add_piece_to_coordinate(knight2)
    assert is_path_unobstructed(start, end, board) == "Move blocked by another piece"




def test_is_within_board():
    # Setup
    board = Board(8, 8, [])
    inside_coordinate = Coordinate(4, 4)
    outside_coordinate = Coordinate(9, 9)
    
    # Check coordinates inside and outside the board
    assert is_within_board(board, inside_coordinate) is None
    assert is_within_board(board, outside_coordinate) == "Coordinate out of bounds"



def test_is_move_valid():
    # Setup
    knight = Knight(owner="Player1")
    pieces = [knight]
    board = Board(8, 8, pieces)
    start = Coordinate(0, 0)
    end = Coordinate(2, 2)

    '''
    coord_start = board.coordinate_map[(0, 0)]
    if not coord_start.occupied:
        coord_start.add_piece_to_coordinate(knight)
'''
    # Check a valid move
    assert is_move_valid(board, "Player1", start, end) is None
    
    # Check an invalid move (out of bounds)
    end = Coordinate(9, 9)
    assert is_move_valid(board, "Player1", start, end) == "Coordinate out of bounds"

def test_move_piece(setup_game):
    game, player1, player2 = setup_game

    # Initialize some pieces
    knight = Knight(owner=player1)
    start_coordinate = Coordinate(0, 0)
    end_coordinate = Coordinate(2, 2)
    
    # Ensure the knight is placed on the board
    coordinate_start = game.board.coordinate_map[(0, 0)]
    if not coordinate_start.occupied:
        coordinate_start.add_piece_to_coordinate(knight)
    
    # Move the piece
    game.move_piece(player1, start_coordinate, end_coordinate)
    
    # Get the piece at the end coordinate
    piece_at_end = game.board.get_piece_at_coordinate(end_coordinate)

    # Ensure the knight moved
    assert piece_at_end is not None 
    assert isinstance(piece_at_end, Knight) 
    assert piece_at_end.owner == knight.owner

    # Check if the starting coordinate is empty
    original_piece = game.board.get_piece_at_coordinate(start_coordinate)
    assert original_piece is None


def test_bishop_movement():
    # Setup
    board = Board(8, 8, [])
    player1 = "Player1"
    bishop = Bishop(owner=player1)
    start_coordinate = Coordinate(3, 3)
    valid_end_coordinates = [
        Coordinate(5, 5),
        Coordinate(1, 1), 
        Coordinate(0, 6)
    ]
    invalid_end_coords = [
        Coordinate(3, 4),
        Coordinate(4, 3),
        Coordinate(9, 9)
    ]

    # Place the Bishop on the starting coordinate
    board.coordinate_map[(3, 3)].add_piece_to_coordinate(bishop)

    # Test valid moves
    for end_coordinate in valid_end_coordinates:
        assert is_move_valid(board, player1, start_coordinate, end_coordinate) is None

    # Test invalid moves
    for end_coord in invalid_end_coords:
        if end_coord.x < 0 or end_coord.y < 0 or end_coord.x >= 8 or end_coord.y >= 8:
            assert is_move_valid(board, player1, start_coordinate, end_coord) == "Coordinate out of bounds"
        else:
            assert is_move_valid(board, player1, start_coordinate, end_coord) == "Piece not allowed to move like that"

def test_bishop_blocked_move():
    # Setup
    board = Board(8, 8, [])
    player1 = "Player1"
    player2 = "Player2"
    bishop = Bishop(owner=player1)
    blocking_piece = Knight(owner=player2)
    start_coord = Coordinate(3, 3)
    blocked_end_coord = Coordinate(5, 5)

    # Place the Bishop and blocking piece on the board
    board.coordinate_map[(3, 3)].add_piece_to_coordinate(bishop)
    board.coordinate_map[(4, 4)].add_piece_to_coordinate(blocking_piece)

    # Test blocked move
    assert is_move_valid(board, player1, start_coord, blocked_end_coord) == "Move blocked by another piece"
