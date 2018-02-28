import tkinter as tk

class Piece():
    def __init__(self, color, row, column):
        self.color = color
        self.row = row
        self.column = column
        self.isKing = False
    
    def promote(self):
        self.isKing |= True

class Tile():
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.piece = None
        self.color = color
        self.gui_tile = None
    
    def addPiece(self, piece):
        self.piece = piece
        
    def removePiece(self):
        toRemove = self.piece
        self.piece = None
        return toRemove
    
    def isOccupied(self):
        return self.piece != None
    
tile_colors = ['white', 'brown']        
        
class Game():
    def __init__(self):
        self.players = ['red','grey']
#         self.num_pieces = {color:12 for color in self.players}
        self.turn = 0
        self.selected = (None, None)
        self.Board = []
        for row_idx in range(8):
            row = []
            for col_idx in range(8):
                newTile = Tile(row_idx, col_idx, tile_colors[(row_idx + col_idx) % 2])
                if newTile.color == tile_colors[1]:
                    if row_idx in range(0,3):
                        newPiece = Piece("grey", row_idx, col_idx)
                        newTile.addPiece(newPiece)
                    if row_idx in range(5,8):
                        newPiece = Piece("red", row_idx, col_idx)
                        newTile.addPiece(newPiece)
                        
                row.append(newTile)
            self.Board.append(row)
    
    def nextTurn(self):
        self.turn = (self.turn + 1) % 2
        
    def isSelected(self):
        return self.selected != (None, None)
    
    def select(self, row, col):
        if self.Board[row][col].isOccupied():
            piece = self.Board[row][col].piece
            if piece.color == self.players[self.turn]:
                self.selected = (row, col)
                return True
            else:
                self.selected = (None, None)
        return False
    
    def move(self, row, col):
        assert self.isSelected()
        cur_row = self.selected[0]
        cur_col = self.selected[1]
        piece = self.Board[cur_row][cur_col].piece
        if piece.isKing:
            max_valid_moves = [(cur_row + i, cur_col + j) for i in [-1, 1] for j in [-1, 1]]
            max_valid_attacks = [(cur_row + i, cur_col + j) for i in [-2, 2] for j in [-2, 2]] 
        else:
            if self.turn == 0:
                max_valid_moves = [(cur_row + i, cur_col + j) for i in [-1] for j in [-1, 1]]
                max_valid_attacks = [(cur_row + i, cur_col + j) for i in [-2] for j in [-2, 2]]
            else:
                max_valid_moves = [(cur_row + i, cur_col + j) for i in [1] for j in [-1, 1]]
                max_valid_attacks = [(cur_row + i, cur_col + j) for i in [2] for j in [-2, 2]]
        
        
        max_valid_moves = [pos for pos in max_valid_moves if pos[0] in range(8) and pos[1]  in range(8)] 
        max_valid_attacks = [pos for pos in max_valid_attacks if pos[0] in range(8) and pos[1] in range(8)]
        
        max_valid_moves = [pos for pos in max_valid_moves if not self.Board[pos[0]][pos[1]].isOccupied()]
        max_valid_attacks = [pos for pos in max_valid_attacks if not self.Board[pos[0]][pos[1]].isOccupied()]

        new_valid = []
        for pos in max_valid_attacks:
            middle = self.Board[int((cur_row + pos[0])//2)][int((cur_col + pos[1])//2)]
            if middle.isOccupied() and middle.piece.color != piece.color:
                new_valid.append(pos)
        max_valid_attacks = new_valid

        if (row,col) in max_valid_moves:
            moved_piece = self.Board[cur_row][cur_col].removePiece()
            moved_piece.row = row
            moved_piece.col = col
            if moved_piece.color == self.players[0]:
                if moved_piece.row == 0:
                    moved_piece.isKing = True
            elif moved_piece.color == self.players[1]:
                if moved_piece.row == 7:
                    moved_piece.isKing = True
            self.Board[row][col].addPiece(moved_piece)
            self.nextTurn()
        elif (row,col) in max_valid_attacks:
            moved_piece = self.Board[cur_row][cur_col].removePiece()
            moved_piece.row = row
            moved_piece.col = col
            if moved_piece.color == self.players[0]:
                if moved_piece.row == 0:
                    moved_piece.isKing = True
            elif moved_piece.color == self.players[1]:
                if moved_piece.row == 7:
                    moved_piece.isKing = True
            self.Board[row][col].addPiece(moved_piece)
            killed_piece = self.Board[int((row + cur_row)//2)][int((col + cur_col)//2)].removePiece()
        
        self.selected = (None, None)        
        
        
        
                                        
        
# https://stackoverflow.com/questions/30657984/make-a-grid-with-tkinter-rectangle
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=640, height=640, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.Game = Game()
        self.rows = 8
        self.columns = 8
#         self.tiles = {}
        self.canvas.bind("<Configure>", self.redraw)
        self.status = tk.Label(self, anchor="w")
        self.status.pack(side="bottom", fill="x")
        self.tile_colors = ['white', 'brown']

    def redraw(self, event=None):
        self.canvas.delete("rect")
        cellwidth = int(self.canvas.winfo_width()/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.columns)
        for row, row_tiles in enumerate(self.Game.Board):
            for column, tile in enumerate(row_tiles):
                x1 = column*cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile.gui_tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill=tile.color, tags="rect")
                if tile.isOccupied():
                    if tile.piece.isKing:
                        oval = self.canvas.create_oval(x1,y1,x2,y2, fill=tile.piece.color, width = 10)
                        self.canvas.tag_bind(oval, "<1>", lambda event, row=row, column=column: self.clicked(row, column))
                    else:
                        oval = self.canvas.create_oval(x1,y1,x2,y2, fill=tile.piece.color)
                        self.canvas.tag_bind(oval, "<1>", lambda event, row=row, column=column: self.clicked(row, column))
                self.canvas.tag_bind(tile.gui_tile, "<1>", lambda event, row=row, column=column: self.clicked(row, column))

    def clicked(self, row, column):
        tile = self.Game.Board[row][column].gui_tile
        tile_color = self.canvas.itemcget(tile, "fill")
        if self.Game.isSelected():
            selected_tile = self.Game.Board[self.Game.selected[0]][self.Game.selected[1]]
            self.Game.move(row, column)
            self.canvas.itemconfigure(selected_tile.gui_tile, fill=selected_tile.color)
            self.redraw()
        else:
            new_color = "green" if self.Game.select(row, column) else self.Game.Board[row][column].color
            self.canvas.itemconfigure(tile, fill=new_color)
        self.status.configure(text="you clicked on %s/%s" % (row, column))

if __name__ == "__main__":
    app = App()
    app.resizable(0,0)
    app.mainloop()