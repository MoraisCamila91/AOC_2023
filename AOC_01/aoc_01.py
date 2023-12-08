import re

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

file_path = '/home/mindera/Downloads/input.txt'
result_string = read_file_and_produce_string(file_path)

lst_values = result_string.split('\n')

def to_digit(string_value):
     match string_value:
        case 'one': return '1'
        case 'two': return '2'
        case 'three': return '3'
        case 'four': return '4'
        case 'five': return '5'
        case 'six': return '6'
        case 'seven': return '7'
        case 'eight': return '8'
        case 'nine': return '9'
        case _: return string_value

def get_first_and_last_digit(string_value) -> int:
        first_find = re.findall(r'(\d|one|two|three|four|five|six|seven|eight|nine).*', string_value) or ['0']
        second_find = re.findall(r'.*(\d|one|two|three|four|five|six|seven|eight|nine)', string_value) or first_find
        # print(first_find)
        
        return int(to_digit(first_find[0]) + to_digit(second_find[0]))

assert 97 == get_first_and_last_digit('9six27sdgmz')
assert 82 == get_first_and_last_digit('aeight2')
assert 23 == get_first_and_last_digit('2eighthree')
assert 22 == get_first_and_last_digit('two')

lst_digits = list(map(get_first_and_last_digit, lst_values))
# print(list(zip(lst_digits, lst_values))[100])
# print(list(zip(lst_digits, lst_values)))
print(sum(lst_digits))
