
import tools
import gameai as ai
from checkers import Piece
from checkers import Board

"""
    This program will play a game of checkers against the computer. The functions
    will work together to get the player to prompt a desired position
    and play the game.
"""

def indexify(position):
    """
    This function will have an input of a letter and a number, it will return a tuple of coordinates
    """
    #Create two values, one the letter, one the number
    x = position[0]
    y = int(position[1:])
    #Create two lists of all possible letters and numbers
    x_pos = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    y_pos = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    #Check the index of our position in our list
    x_cord = x_pos.index(x)
    y_cord = y_pos.index(y)
    #Put those indexs in a tuple
    tup = (x_cord,y_cord)
    #return the tuple
    return(tup)
    

def deindexify(row, col):
    """
    This function will have an input of a tuple with two positions, it will 
    return the position as a str of letter and numbers
    """
    #Create a list of all possible letters and numbers
    x_pos = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    y_pos = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    #Get the item at the index location of the list
    x_cord = x_pos[row]
    y_cord = str(y_pos[col])
    #Return the letter and number as a string
    pos = x_cord+y_cord
    return pos

def initialize(board):
    """
    This function puts white and black pieces according to the checkers
    game positions. The black pieces will be on the top three rows and
    the white pieces will be on the bottom three rows (for an 8x8 board).
    The first row for the black pieces will be placed as a2, a4, a6, ...
    etc. and the next rows will be b1, b3, b5, ... etc. For the white
    rows, the placement patterns will be opposite of those of blacks.
    This must work for any even length board size.
    """
    row = col = board.get_length()
    initrows = (row // 2) - 1
    for r in range(row - 1, row - (initrows + 1), -1):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece('white'))
    for r in range(0, initrows):
        for c in range(0 if r % 2 == 1 else 1, col, 2):
            board.place(r, c, Piece())

def count_pieces(board):
    """
    This function will be inputed our board and then it will return a tuple of 
    a count of black pieces and white pieces
    """
    #Initialize two values
    black = 0
    white = 0
    #Loop over every single square
    for r in range(board.get_length()):
            for c in range(board.get_length()):
                #If a square is free do next statements
                if not board.is_free(r, c):
                    #Grab the piece from the board
                    p = board.get(r,c)
                    #If the piece is black, we add one to the black counter
                    if p.is_black() == True:
                        black += 1
                    #If the piece is white, we add one to the white counter
                    if p.is_white() == True:
                        white += 1
    #We put both of these numbers in a tuple and return it
    tup = (black,white)
    return tup
                        
        
    

def get_all_moves(board, color, is_sorted = False):
    """
    Write something about this function here.
    """
    #Create an empty list
    end_list = []
    #loop over every single spot on the board
    for r in range(board.get_length()):
        for c in range(board.get_length()):
            #If that spot is not free, we execute the following statements
            if not board.is_free(r, c):
                #We get the position of the coordinates
                position = deindexify(r,c)
                #We grab the piece at the coordinates
                p = board.get(r,c)
                #We check that the color of the piece is the desired color
                if p.color() == color:
                    #We get moves from get_moves function
                    moves = tools.get_moves(board,r,c,is_sorted)
                    #Create a for every position in my list
                    for pos in moves:
                        #I append a tuple to my end list
                        end_list.append((position,pos))
    return (end_list)
                        

def sort_captures(all_captures,is_sorted=False):
    '''If is_sorted flag is True then the final list will be sorted by the length
    of each sub-list and the sub-lists with the same length will be sorted
    again with respect to the first item in corresponding the sub-list,
    alphabetically.'''
    
    return sorted(all_captures, key = lambda x: (-len(x), x[0])) if is_sorted \
            else all_captures

def get_all_captures(board, color, is_sorted = False):
    """
    This function returns a list of all possible captures for each piece of the 
    board (even if they were king)
    """
    #Create an empty list
    end_list = []
    for r in range(board.get_length()):
        for c in range(board.get_length()):
            if not board.is_free(r, c):
                p = board.get(r,c)
                if p.color() == color:
                    moves = tools.get_captures(board,r,c,is_sorted)
                    #If moves has something in it, extend it into the end list
                    if moves:
                        end_list.extend(moves)
    #Return the end list
    return (end_list)
            

def apply_move(board, move):
    """
    This function will try to apply the inputed move by checking if it is a 
    valid move, placing a piece at the new place and removing it from the old place.
    
    Raise this exception below:
        raise RuntimeError("Invalid move, please type" \
                         + " \'hints\' to get suggestions.") 
    If,
        a. there is no move from move[0], i.e. use tools.get_moves() function to
            get all the moves from move[0]
        b. the destination position move[1] is not in the moves list found
            from tools.get_moves() function.            
    """
    #Get the row and col of my first move
    row, col = indexify(move[0])
    #Get the possible moves from the get_moves function
    move_list = tools.get_moves(board, row, col)
    #Create an if statement to check that move_list is not empty and that move[1] is in my list
    if move_list and move[1] in move_list:
        #Grab the piece from the board
        piece = board.get(row,col)
        #Remove that piece
        board.remove(row,col)
        #Get the index of the location where we are putting the piece
        row1, col1 = indexify(move[1])
        #Place the piece we grabbed at the new location
        board.place(row1,col1,piece)
        #Create an if statement that if the piece has reached the last row to turn it into a king
        if (piece.color() == "black" and row1 == board.get_length() -1) or (piece.color() == "white" and row1 == 0):
            piece.turn_king()
    else:
        #If the move is not valid, we raise an error
        raise RuntimeError ("Invalid move, please type 'hints' to get suggestions.")
        

def apply_capture(board, capture_path):
    """
    This function will be inputed a capture_path as a list and apply the capture.
    
    Raise this exception below:
        raise RuntimeError("Invalid jump/capture, please type" \
                         + " \'hints\' to get suggestions.") 
    If,
        a. there is no jump found from any position in capture_path, i.e. use 
            tools.get_jumps() function to get all the jumps from a certain
            position in capture_path
        b. the destination position from a jump is not in the jumps list found
            from tools.get_jumps() function.            
    """
    #Loop over the number of the length of the list - 1
    for pos in range(len(capture_path)-1):
        #Get the coordinates of the position from
        row_from, col_from = indexify(capture_path[pos])
        #Get the possible jumps from the get_jumps function
        jumps = tools.get_jumps(board, row_from, col_from)
        #If statement if jumps isn't empty and my going to position is in jumps
        if jumps and (capture_path[pos + 1] in jumps):
            #Grabe the piece from the board
            piece = board.get(row_from, col_from)
            #Remove the piece from the board
            board.remove(row_from, col_from)
            #Get the coordinates of the position where the piece is going
            row_to, col_to = indexify(capture_path[pos+1])
            #These next if statements are to figure out the position of the captured piece
            if row_to >row_from:
                r = row_from +1
            else:
                r = row_from -1
            if col_to > col_from:
                c = col_from +1
            else:
                c = col_from -1
            #We remove the piece with the coordinates calculated above
            board.remove(r,c)
            #We place the old piece to the new location
            board.place(row_to, col_to, piece)
            #If the piece reachs the end row then we turn it into a king
            if (piece.color() == "black" and row_to == board.get_length() -1) or (piece.color() == "white" and row_to == 0):
                piece.turn_king()
        else:
            #If jumps is empty or our pos isnt in jumps than we raise an error
            raise RuntimeError ("Invalid jump/capture, please type 'hints' to get suggestions.")
        
        
            
def get_hints(board, color, is_sorted = False):
    """
    This function will return a list of two lists. The first list will be all possible moves and the second list will be all possible jumps. If a jump is possible, then the moves list will be empty
    """
    #Get a moves_list from our get_all_moves function
    moves_list = get_all_moves(board, color, is_sorted)
    #Get a jumps_list from our get_all_captures function
    jumps_list = get_all_captures(board, color, is_sorted)
    #If my jump list isn't empty
    if jumps_list:
        #Then we make the moves list empty
        moves_list = []
    #Create a hint_list and return it
    hint_list = (moves_list,jumps_list)
    return hint_list
        
def get_winner(board, is_sorted = False):
    """
    This function will test multiple possibilities of winners and return the winner or a draw
    """
    #black is the winner if it has more pieces on the board
    if count_pieces(board)[0] > count_pieces(board)[1]:
        return "black"
    #White is the winner if it has mroe pieces on the board
    if count_pieces(board)[1] > count_pieces(board)[0]:
        return "white"
    #If both colors ahve the same amount of pices than it's a draw
    if count_pieces(board)[0] == count_pieces(board)[1]:
        return "draw"
        
    
                        
def is_game_finished(board, is_sorted = False):
    """
    This function will return True if the game is finished, and false if the game is not
    """
    #Checks if there are no more possible moves by either colors
    if not get_hints(board,'black',is_sorted)[0] and not get_hints(board,'black',is_sorted)[1] or not get_hints(board,'white',is_sorted)[0] and not get_hints(board,'white',is_sorted)[1]:
        #If one is out of moves, then True, the game is over
        return True
    else:
        #Or else, the game is not over
        return False
    

# Some error messages to save lines.
move_error = "Invalid move, please type \'hints\' to get suggestions."
hasjump_error = "You have jumps, please type \'hints\' to get suggestions."
jump_error = "Invalid jump, please type \'hints\' to get suggestions."
hint_error = "Invalid hint number."
cmd_error = "Invalid command."

def game_play_human():
    """
    This is the main mechanism of the human vs. human game play.
    Use this function to write the game_play_ai() function.
    """    
    # UNCOMMENT THESE TWO LINES TO TEST ON MIMIR SUBMISSION
    #Piece.symbols = ['b', 'w']
    #Piece.symbols_king = ['B', 'W']
    
    prompt = "[{:s}'s turn] :> "
    print(tools.banner)
   
    # Choose the color here
    (my_color, opponent_color) = tools.choose_color()
    
    # Take a board of size 8x8
    board = Board(8)
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'black' else opponent_color
    print("Black always plays first.\n")
    
    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count)    
            
            # Get the command from user using input
            command = input(prompt.format(turn)).strip().lower()
            
            # Now decide on different commands
            if command == 'pass':
                break
            elif command == 'exit':
                break
            elif command == 'hints':
                (moves, captures) = get_hints(board, turn, True)
                if moves:
                    print("You have moves:")
                    for i, move in enumerate(moves):
                        print("\t{:d}: {:s} --> {:s}"\
                                  .format(i + 1, move[0], move[1]))
                if captures:
                    print("You have captures:")
                    for i, path in enumerate(captures):
                        print("\t{:d}: {:s}".format(i + 1, str(path)))
            else:
                command = [s.strip().lower() for s in command.split()]
                (moves, captures) = get_hints(board, turn, True)
                action = None
                if command and command[0] == 'move' and len(command) == 3:
                    if not captures:
                        action = (command[1], command[2])
                        if action in moves:
                            apply_move(board, action)
                        else:
                            raise RuntimeError(move_error)
                    else:
                        raise RuntimeError(hasjump_error)
                elif command and command[0] == 'jump' and len(command) >= 3:
                    action = command[1:]
                    if action in captures:
                        apply_capture(board, action)
                    else:
                        raise RuntimeError(jump_error)
                elif command and command[0] == 'apply' and len(command) == 2:
                    id_hint = int(command[1])
                    if moves and (1 <= id_hint <= len(moves)):
                        action = moves[id_hint - 1]
                        apply_move(board, action)
                    elif captures and (1 <= id_hint <= len(captures)):
                        action = captures[id_hint - 1]
                        apply_capture(board, action)
                    else:
                        raise ValueError(hint_error)
                else:
                    raise RuntimeError(cmd_error + tools.usage)
                print("\t{:s} played {:s}.".format(turn, str(action)))
                turn = my_color if turn == opponent_color else opponent_color
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)    
    if command != 'pass':
        winner = get_winner(board)
        if winner != 'draw':
            diff = abs(piece_count[0] - piece_count[1])
            print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
        else:
            print("This game ends in a draw.")
    else:
        winner = opponent_color if turn == my_color else my_color
        print("{:s} gave up! {:s} is the winner!! yay!!!".format(turn, winner))
    # --- end of game play human ---
    
def game_play_ai():
    """
    This is the main mechanism of the human vs. ai game play. You need to
    implement this function by taking helps from the game_play_human() 
    function.
    
    For a given board situation/state, you can call the ai function to get
    the next best move, like this:
        
        move = ai.get_next_move(board, turn)
        
    where the turn variable is a color 'black' or 'white', also you need to 
    import ai module as 'import gameai as ai' at the beginning of the file.
    This function will be very similar to game_play_human().
    """
    #Piece.symbols = ['b', 'w']
    #Piece.symbols_king = ['B', 'W']
    
    prompt = "[{:s}'s turn] :> "
    print(tools.banner)
   
    # Choose the color here
    (my_color, opponent_color) = tools.choose_color()
    
    # Take a board of size 8x8
    board = Board(8)
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'black' else opponent_color
    print("Black always plays first.\n")
    
    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count) 
            
            if turn == my_color:
                command = input(prompt.format(turn)).strip().lower()
            else:
                move = ai.get_next_move(board,turn)
                if type(move) == tuple:
                    command = 'move{:s}{:s}'.format(move[0],move[1])
                if type(move) is list:
                    for item in move:
                        jump = " ".join(str(item))
                        command = ('jump '+jump)
                '''if type(move) == list:
                    command = 'jump {:s}'.format(" ".join[v.strip().lower() for v in move])'''
            
            # Get the command from user using input
            command = input(prompt.format(turn)).strip().lower()
            
            # Now decide on different commands
            if command == 'pass':
                break
            elif command == 'exit':
                break
            elif command == 'hints':
                (moves, captures) = get_hints(board, turn, True)
                if moves:
                    print("You have moves:")
                    for i, move in enumerate(moves):
                        print("\t{:d}: {:s} --> {:s}"\
                                  .format(i + 1, move[0], move[1]))
                if captures:
                    print("You have captures:")
                    for i, path in enumerate(captures):
                        print("\t{:d}: {:s}".format(i + 1, str(path)))
            else:
                command = [s.strip().lower() for s in command.split()]
                (moves, captures) = get_hints(board, turn, True)
                action = None
                if command and command[0] == 'move' and len(command) == 3:
                    if not captures:
                        action = (command[1], command[2])
                        if action in moves:
                            apply_move(board, action)
                        else:
                            raise RuntimeError(move_error)
                    else:
                        raise RuntimeError(hasjump_error)
                elif command and command[0] == 'jump' and len(command) >= 3:
                    action = command[1:]
                    if action in captures:
                        apply_capture(board, action)
                    else:
                        raise RuntimeError(jump_error)
                elif command and command[0] == 'apply' and len(command) == 2:
                    id_hint = int(command[1])
                    if moves and (1 <= id_hint <= len(moves)):
                        action = moves[id_hint - 1]
                        apply_move(board, action)
                    elif captures and (1 <= id_hint <= len(captures)):
                        action = captures[id_hint - 1]
                        apply_capture(board, action)
                    else:
                        raise ValueError(hint_error)
                else:
                    raise RuntimeError(cmd_error + tools.usage)
                print("\t{:s} played {:s}.".format(turn, str(action)))
                turn = my_color if turn == opponent_color else opponent_color
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)    
    if command != 'pass':
        winner = get_winner(board)
        if winner != 'draw':
            diff = abs(piece_count[0] - piece_count[1])
            print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
        else:
            print("This game ends in a draw.")
    else:
        winner = opponent_color if turn == my_color else my_color
        print("{:s} gave up! {:s} is the winner!! yay!!!".format(turn, winner))
    
    
    
    
    '''#Piece.symbols = ['b', 'w']
    #Piece.symbols_king = ['B', 'W']
    
    prompt = "[{:s}'s turn] :> "
   
    # Choose the color here
    (my_color, opponent_color) = tools.choose_color()
    
    # Take a board of size 8x8
    board = Board(8)
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'black' else opponent_color
    print("Black always plays first.\n")
    
    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count)    
            if turn == opponent_color:
                move = ai.get_next_move(board,turn)
                if type(move) is list:
                    for item in move:
                        jump = " ".join(str(item))
                        command = ('jump '+jump)
                if type(move) is tuple:
                    command = ('move '+move[0]+move[1])
                command = [s.strip().lower() for s in command.split()]
                (moves, captures) = get_hints(board, turn, True)
                action = None
                if command and command[0] == 'move' and len(command) == 3:
                    if not captures:
                        action = (command[1], command[2])
                        if action in moves:
                            apply_move(board, action)
                        else:
                            raise RuntimeError(move_error)
                    else:
                        raise RuntimeError(hasjump_error)
                elif command and command[0] == 'jump' and len(command) >= 3:
                    action = command[1:]
                    if action in captures:
                        apply_capture(board, action)
                    else:
                        raise RuntimeError(jump_error)
                elif command and command[0] == 'apply' and len(command) == 2:
                    id_hint = int(command[1])
                    if moves and (1 <= id_hint <= len(moves)):
                        action = moves[id_hint - 1]
                        apply_move(board, action)
                    elif captures and (1 <= id_hint <= len(captures)):
                        action = captures[id_hint - 1]
                        apply_capture(board, action)
                    else:
                        raise ValueError(hint_error)
                else:
                    raise RuntimeError(cmd_error + tools.usage)
                print("\t{:s} played {:s}.".format(turn, str(action)))
                turn = my_color if turn == opponent_color else opponent_color
                piece_count = count_pieces(board)
                print("Current board:")
                board.display(piece_count)
            # Get the command from user using input
            command = input(prompt.format(turn)).strip().lower()
            
            # Now decide on different commands
            if command == 'pass':
                break
            elif command == 'exit':
                break
            elif command == 'hints':
                (moves, captures) = get_hints(board, turn, True)
                if moves:
                    print("You have moves:")
                    for i, move in enumerate(moves):
                        print("\t{:d}: {:s} --> {:s}"\
                                  .format(i + 1, move[0], move[1]))
                if captures:
                    print("You have captures:")
                    for i, path in enumerate(captures):
                        print("\t{:d}: {:s}".format(i + 1, str(path)))
            else:
                command = [s.strip().lower() for s in command.split()]
                (moves, captures) = get_hints(board, turn, True)
                action = None
                if command and command[0] == 'move' and len(command) == 3:
                    if not captures:
                        action = (command[1], command[2])
                        if action in moves:
                            apply_move(board, action)
                        else:
                            raise RuntimeError(move_error)
                    else:
                        raise RuntimeError(hasjump_error)
                elif command and command[0] == 'jump' and len(command) >= 3:
                    action = command[1:]
                    if action in captures:
                        apply_capture(board, action)
                    else:
                        raise RuntimeError(jump_error)
                elif command and command[0] == 'apply' and len(command) == 2:
                    id_hint = int(command[1])
                    if moves and (1 <= id_hint <= len(moves)):
                        action = moves[id_hint - 1]
                        apply_move(board, action)
                    elif captures and (1 <= id_hint <= len(captures)):
                        action = captures[id_hint - 1]
                        apply_capture(board, action)
                    else:
                        raise ValueError(hint_error)
                else:
                    raise RuntimeError(cmd_error + tools.usage)
                print("\t{:s} played {:s}.".format(turn, str(action)))
                turn = my_color if turn == opponent_color else opponent_color
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    board.display(piece_count)    
    if command != 'pass':
        winner = get_winner(board)
        if winner != 'draw':
            diff = abs(piece_count[0] - piece_count[1])
            print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
        else:
            print("This game ends in a draw.")
    else:
        winner = opponent_color if turn == my_color else my_color
        print("{:s} gave up! {:s} is the winner!! yay!!!".format(turn, winner))
    # --- end of game play ai ---'''

def main():
    game_play_human()
    game_play_ai()
    
# main function, the program's entry point
if __name__ == "__main__":
    main()