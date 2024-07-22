from .structures.coordinate import Coordinate
from .structures.board import Board

ERROR_COORDINATE_OUT_OF_BOUNDS = "Coordinate out of bounds"
ERROR_PIECE_NOT_FOUND = "Piece not found at the coordinate"
ERROR_INVALID_MOVE = "Invalid move"
ERROR_MOVE_BLOCKED = "Move blocked by another piece"
ERROR_NOT_RULE_ABIDING = "Piece not allowed to move like that"

def is_within_board(board: Board, coordinate: Coordinate) -> str:
    if not (0 <= coordinate.x < board.board_height) or not (0 <= coordinate.y < board.board_width):
        return ERROR_COORDINATE_OUT_OF_BOUNDS
    return None

def is_move_valid(board: Board, player, original_coordinate: Coordinate, destination_coordinate: Coordinate) -> str:
    # Check if the destination coordinate is within the board
    error = is_within_board(board, destination_coordinate)
    if error:
        return error
    

    # Check if the piece belongs to the current player
    piece_at_original = board.get_piece_at_coordinate(original_coordinate)
    if piece_at_original is None:
        return ERROR_PIECE_NOT_FOUND
    if piece_at_original.owner != player:
        return ERROR_INVALID_MOVE
    
    # Check if the destination coordinate is occupied by a piece of the same player
    piece_at_destination = board.get_piece_at_coordinate(destination_coordinate)
    if piece_at_destination is not None and piece_at_destination.owner == player:
        return ERROR_INVALID_MOVE

    # Check if the move follows the piece's rules
    if not piece_at_original.rules_abiding(original_coordinate, destination_coordinate):
        return ERROR_NOT_RULE_ABIDING
    
    # Check if the path is unobstructed
    error = is_path_unobstructed(original_coordinate, destination_coordinate, board)
    if error:
        return error

    return None

def is_diagonal_move(start: Coordinate, end: Coordinate) -> bool:
    dx = abs(end.x - start.x)
    dy = abs(end.y - start.y)
    return dx == dy

def is_path_unobstructed(start: Coordinate, end: Coordinate, board: Board) -> str:
    error = is_within_board(board, start)
    if error:
        return error
    
    error = is_within_board(board, end)
    if error:
        return error
    
    step_x = 1 if end.x > start.x else -1
    step_y = 1 if end.y > start.y else -1

    x, y = start.x, start.y
    while (x, y) != (end.x, end.y):
        x += step_x
        y += step_y
        
        if not (0 <= x < board.board_height and 0 <= y < board.board_width):
            return ERROR_MOVE_BLOCKED
        
        if board.get_piece_at_coordinate(Coordinate(x, y)) is not None:
            return ERROR_MOVE_BLOCKED
    
    return None
