from tile import Tile

class Hotel:
    def __init__(self, label, tiles=[]):
        self.label = self.get_label_from_color(label)
        self.tiles = tiles

    def get_label_from_color(self, label):
        labels = {
            "red": "American",
            "blue": "Continental",
            "green": "Festival",
            "yellow": "Imperial",
            "purple": "Sackson",
            "brown": "Tower",
            "orange": "Worldwide"
        }
        return labels[label]
    
    def chain_size(self):
        return len(self.tiles)
    
