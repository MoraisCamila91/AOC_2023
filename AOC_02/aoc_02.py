import re
from functools import reduce

def read_file_and_produce_string(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the entire contents of the file into a string
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"

file_path = '/home/mindera/Documents/2023AOC/AOC_02/input.txt'
input_string = read_file_and_produce_string(file_path)

input_lst = input_string.split('\n')
input_dict = dict(map(lambda x: x.split(': '), input_lst))
input_dict = {int(k.replace('Game ', '')): v.split(';') for k, v in input_dict.items()}

def organize_rgb(game: list[str]) -> tuple[int, int, int]:
    game_tuples = []
    for draw in game:
        r = 0
        g = 0
        b = 0

        pattern = re.compile(r'(([0-9]*\ )(green|blue|red))')

        for match in pattern.finditer(draw):
            qtt = int(match.group(2))
            color = match.group(3)

            match color:
                case 'red': r = qtt
                case 'green': g = qtt
                case 'blue': b = qtt
                case other: raise Exception(other +" is not a valid color.")
        
        game_tuples.append((r, g, b))
    return game_tuples
            
input_dict = {k: organize_rgb(v) for k, v in input_dict.items()}

def test_viability(test: tuple[int, int, int], game: list[tuple[int, int, int]]) -> bool:
    game_viability = True

    for draw in game:
        if draw[0] > test[0] or draw[1] > test[1] or draw[2] > test[2]:
            game_viability = False
    
    return game_viability

input_value = (12, 13, 14)
result_dict = {k: test_viability(input_value, v) for k, v in input_dict.items()}

inviable_games = [k for k, v in result_dict.items() if v == False]
viable_games = [k for k, v in result_dict.items() if v == True]

# assert 8 == sum(viable_games)
# assert 7 == sum(inviable_games)

print(sum(viable_games))

#### B

def get_minimum_set(game: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    minimum_set = list(game[0])

    for draw in game[1:]:
        if draw[0] > minimum_set[0]:
            minimum_set[0] = draw[0]
        if draw[1] > minimum_set[1]:
            minimum_set[1] = draw[1]
        if draw[2] > minimum_set[2]:
            minimum_set[2] = draw[2]
    
    return minimum_set

dict_minimum_set = {k: get_minimum_set(v) for k, v in input_dict.items()}
dict_game_power = {k: reduce((lambda x, y: x * y), v) for k, v in dict_minimum_set.items()}

print(sum(list(dict_game_power.values())))

