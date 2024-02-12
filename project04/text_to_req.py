labels = {
            "red": "American",
            "blue": "Continental",
            "green": "Festival",
            "yellow": "Imperial",
            "purple": "Sackson",
            "brown": "Tower",
            "orange": "Worldwide"
        }

board_object = {
    "tiles": [],
    "hotels": []
}

hotel_object = {}


# Read the board from the file
with open("./board.txt", "r") as f:
    board = f.readlines()

# Remove newline characters
board = [row.strip().split(" ") for row in board]

# Create tiles and hotels
for row in board:
    for col in range(1,13):
        tile = {
            "row": row[0],
            "column": str(col)
        }
        if row[col] == "0":
            continue
        elif row[col] == "1":
            board_object["tiles"].append(tile)
        elif row[col] in labels.keys():
            board_object["tiles"].append(tile)
            label = labels[row[col]]
            if label not in hotel_object:
                hotel_object[label] = [tile]
            else:
                hotel_object[label].append(tile)
        else:
            raise ValueError("Invalid tile value at row {} and column {}".format(row[0], col))

board_object["hotels"].append(hotel_object)

# we need hotel_object in {"hotels": [{"hotel": "American", "tiles": [{"row": "A", "column": 1}, ...], ...}]}
# format, so we need to convert hotel_object to the required format
hotels = []
for hotel in hotel_object:
    hotels.append({"hotel": hotel, "tiles": hotel_object[hotel]})
board_object["hotels"] = hotels

print(board_object)

def matrix_to_object(board):
    board_object = {
        "tiles": [],
        "hotels": []
    }
    hotel_object = {}
    tiles = []
    hotels = []
    for i in range(9):
        for j in range(12):
            if board[i][j] == "0":
                continue
            elif board[i][j] == "1":
                tiles.append({"row": chr(i+65), "column": str(j+1)})
            elif board[i][j] in labels.keys():
                tiles.append({"row": chr(i+65), "column": str(j+1)})
                label = labels[board[i][j]]
                if label not in hotel_object:
                    hotel_object[label] = [{"row": chr(i+65), "column": str(j+1)}]
                else:
                    hotel_object[label].append({"row": chr(i+65), "column": str(j+1)})
    board_object["tiles"] = tiles
    for hotel in hotel_object:
        hotels.append({"hotel": hotel, "tiles": hotel_object[hotel]})
    board_object["hotels"] = hotels

    return board_object

test_board = [['yellow', '1', 'blue', 'blue', '0', '0', '0', '0', '0', '0', '0', '0'],
['yellow', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', 'green', 'green', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
matrix_to_object(test_board)