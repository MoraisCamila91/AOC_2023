import re

star_numbers = {}

def add_star_location(lst_stars_loc: list[tuple[int, int]],
                      number: int) -> None:
    for star_loc in lst_stars_loc:
        if star_loc not in star_numbers:
            star_numbers[star_loc] = [number]
        else:
            star_numbers[star_loc].append(number)
    

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

def str_to_matrix(str_input: str) -> list[list[str]]:
    rows = str_input.split('\n')    
    return [[*r]for r in rows]

def get_dimension_2D(input_matrix: list[list[str]]) -> tuple[int, int]:
    return len(input_matrix) - 1, len(input_matrix[0]) - 1

def get_symbol(input_matrix: list[list[str]], location: tuple[int, int]) -> str or None:
    matrix_dimension = get_dimension_2D(input_matrix)
    
    if is_location_valid(location, matrix_dimension):
        return input_matrix[location[0]][location[1]]
    
    return None

def is_location_valid(location: tuple[int, int], matrix_dimension: tuple[int, int]) -> bool:
    if location[0] < 0 or location[1] < 0:
        return False
    if location[0] > matrix_dimension[0]:
        return False
    if location[1] > matrix_dimension[1]:
        return False    
    return True

def is_there_vertical_symbol(input_matrix: list[list[str]], 
                             number_locations: list[tuple[int, int]], 
                             invalid_symbols: list[str],
                             number: int) -> bool:
    matrix_dimension = get_dimension_2D(input_matrix)
    symbols = []

    for location in number_locations:
        # vertical up
        loc_vert_up = (location[0]-1, location[1])
        s = get_symbol(input_matrix, loc_vert_up)
        if s is not None: symbols.append((s, loc_vert_up))

        # vertical down
        loc_vert_down = (location[0]+1, location[1])
        s = get_symbol(input_matrix, loc_vert_down)
        if s is not None: symbols.append((s, loc_vert_down))

    true_symbols = [symbol for symbol in symbols if symbol[0] not in invalid_symbols]

    if '*' in [s[0] for s in symbols]: add_star_location([s[1] for s in symbols if s[0] == '*'], number)
    
    if len(true_symbols) > 0:
        return True
    return False

def is_there_horizontal_symbol(input_matrix: list[list[str]], 
                               number_locations: list[tuple[int, int]], 
                               invalid_symbols: list[str],
                               number: int) -> bool:
    matrix_dimension = get_dimension_2D(input_matrix)
    symbols = []

    hor_left = (number_locations[0][0], min([x[1] for x in number_locations]) - 1)
    hor_right = (number_locations[0][0], max([x[1] for x in number_locations]) + 1)
    
    # horizontal left
    s = get_symbol(input_matrix, hor_left)
    if s is not None: symbols.append((s, hor_left))

    # horizontal right
    s = get_symbol(input_matrix, hor_right)
    if s is not None: symbols.append((s, hor_right))

    true_symbols = [symbol for symbol in symbols if symbol[0] not in invalid_symbols]
    
    if '*' in [s[0] for s in symbols]: add_star_location([s[1] for s in symbols if s[0] == '*'], number)

    if len(true_symbols) > 0:
        return True
    return False

def is_there_diagonal_symbol(input_matrix: list[list[str]], 
                             number_locations: list[tuple[int, int]], 
                             invalid_symbols: list[str],
                             number: int) -> bool:
    matrix_dimension = get_dimension_2D(input_matrix)
    symbols = []

    top_left = (number_locations[0][0] - 1, min([x[1] for x in number_locations]) - 1)
    top_right = (number_locations[0][0] - 1, max([x[1] for x in number_locations]) + 1)
    down_left = (number_locations[0][0] + 1, min([x[1] for x in number_locations]) - 1)
    down_right = (number_locations[0][0] + 1, max([x[1] for x in number_locations]) + 1)
    
    # top left
    s = get_symbol(input_matrix, top_left)
    if s is not None: symbols.append((s, top_left))
    
    # top right
    s = get_symbol(input_matrix, top_right)
    if s is not None: symbols.append((s, top_right))
    
    # down left
    s = get_symbol(input_matrix, down_left)
    if s is not None: symbols.append((s, down_left))
    
    # down right
    s = get_symbol(input_matrix, down_right)
    if s is not None: symbols.append((s, down_right))

    true_symbols = [symbol for symbol in symbols if symbol[0] not in invalid_symbols]
    
    if '*' in [s[0] for s in symbols]: add_star_location([s[1] for s in symbols if s[0] == '*'], number)

    if len(true_symbols) > 0:
        return True
    return False

def is_there_adjacent_symbol(input_matrix: list[list[str]], 
                             number_locations: list[tuple[int, int]], 
                             invalid_symbols: list[str],
                             number: int) -> bool:
    
    adj_vert = is_there_vertical_symbol(input_matrix, number_locations, invalid_symbols, number)
    adj_hor = is_there_horizontal_symbol(input_matrix, number_locations, invalid_symbols, number)
    adj_diag = is_there_diagonal_symbol(input_matrix, number_locations, invalid_symbols, number)

    if adj_vert or adj_hor or adj_diag: return True
    
    return False

def get_adjacent_numbers(matrix_input: list[list[str]], 
                         invalid_symbols: list[str]):
    adjacent_numbers = []
    not_adjacent_numbers = []

    i = 0
    for row in matrix_input:
        number_list = []
        number_list_location = []

        j = 0
        for value in row:
            is_eol = j == len(row) - 1
            if value.isdigit():
                number_list.append(value)
                number_list_location.append((i, j))
            if is_eol or not value.isdigit():
                if len(number_list) == 0:
                    next
                else:
                    number = int(''.join(number_list))
                    if is_there_adjacent_symbol(matrix_input, number_list_location, invalid_symbols, number):
                        adjacent_numbers.append(number)
                    else:
                        not_adjacent_numbers.append(number)
                
                number_list = []
                number_list_location = []

            j += 1            
        i += 1
    
    return (adjacent_numbers, not_adjacent_numbers)

file_path = '/home/mindera/Documents/2023AOC/AOC_03/input.txt'
input_string = read_file_and_produce_string(file_path)
input_matrix = str_to_matrix(input_string)

invalid_symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
adjacent_numbers, not_adjacent_numbers = get_adjacent_numbers(input_matrix, invalid_symbols)

# assert [114, 58] == not_adjacent_numbers
# assert 4361 == sum(adjacent_numbers)

# print(sum(adjacent_numbers))


### B
def mult(x: int, y: int) -> int:
    return x * y

gears = {k: mult(*v) 
         for k, v in star_numbers.items() 
         if len(v) == 2}

# assert 467835 == sum(gears.values())

print(sum(gears.values()))
