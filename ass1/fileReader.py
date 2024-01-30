def read_data_to_2d_list(file_path):
    with open(file_path, 'r') as file:
        data_2d_list = [list(map(int, line.strip().split(','))) for line in file]
    return data_2d_list

