class Tile:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        
    def __gt__(self,other):
        if ord(self.row) < ord(other.row) or (ord(self.row) == ord(other.row) and int(self.column) < int(self.column)):
            return False
        return True
    def __str__(self):
        return "<"+self.row+","+self.column+">"
