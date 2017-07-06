from django.db import models

class ChessBoard:
    def __init__(self):
        # the ChessBoard model won't persist in the database
        managed = False
        self.fen = ''
        self.moved = ''
    
    # return a text representation of the chess board
    def text(self):
        board_text = ""
        # convert fen to rows and columns
        rows = self.__fen_to_rows();
        row_divider = "  ---------------------------------"
        for row_index, row in rows.items():
            # print row divider
            board_text += row_divider + "\n"
            # print row label
            board_text += str(row_index) + " "
            # print columns in this row
            for col_index, col in row.items():
                board_text += "| " + col + " "
            board_text += "|\n"
        # print last row divider
        board_text += row_divider + "\n"
        # print column labels
        board_text += "    a   b   c   d   e   f   g   h  \n"
        return board_text

    # move a chess piece
    def move(self, start_end):
        # get column and row indexes for start and end positions
        start_col = start_end[0:1]
        start_row = start_end[1:2]
        end_col = start_end[2:3]
        end_row = start_end[3:4]
        # convert fen to rows and columns
        rows = self.__fen_to_rows()
        # get the chess piece at start position
        piece = rows[int(start_row)][start_col]
        # replace it with a space
        rows[int(start_row)][start_col] = " "
        # put the piece in the end position, replacing whatever is there
        rows[int(end_row)][end_col] = piece
        # update 'moved'
        self.moved = start_end
        # update this ChessBoard's fen
        self.__rows_to_fen(rows)

    # convert FEN notation into rows and columns (dictionary)
    # rows are indexed from 8 to 1, columns within rows are indexed a-h
    def __fen_to_rows(self):
        # ignore everything after the first space
        rows = self.fen.split(" ", 1)[0]
        # split into rows divided by /
        rows = rows.split("/")
        # for each row create column indexes a-h
        rows = [self.__create_col_indexes(row) for row in rows]
        # create row indexes, counting down from 8 to 1
        rows = {8-k: v for k, v in enumerate(rows)}
        return rows
            
    # convert a given row (list) into a dictionary with a-h indexes
    # private function used by fen_to_rows()
    def __create_col_indexes(self, row):
        new_row = ""
        # add n spaces when there is a number
        for char in row:
            if(char.isdigit()):
                new_row += " " * int(char)
            else:
                new_row += char
        # create a-h indexes using chr(n+97)
        new_row = {chr(n+97): v for n, v in enumerate(new_row)}
        return new_row
        
    # convert rows and columns (dictionary) into fen notation
    def __rows_to_fen(self, rows):
        fen = ""
        row_num = 0
        for row_index, row in rows.items():
            row_num += 1
            if(row_num > 1):
                fen += "/"
            spaces = 0
            for col_index, col in row.items():
                # convert spaces to an integer (# of consecutive spaces)
                if(col == " "):
                    spaces += 1
                if(col != " " and spaces > 0):
                    fen += str(spaces)
                    fen += col
                    spaces = 0
                elif(col != " "):
                    fen += col
                elif(col_index == "h"):
                    fen += str(spaces)
                    spaces = 0
        # add end of FEN string back to the end
        end_of_fen = self.fen.split(" ", 1)[1]
        self.fen = fen + ' ' + end_of_fen

