def matrix_to_object(board):
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