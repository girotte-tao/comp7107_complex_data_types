from fileReader import read_data_to_2d_list
import random
random.seed(42)

def normalization_by_line(data_list, column_index):
    column = [i[column_index] for i in data_list]
    maxcol = max(column)
    mincol = min(column)
    for line in range(len(data_list)):
        data_list[line][column_index]= (data_list[line][column_index] - mincol)/(maxcol-mincol)
    return data_list

def normalization(data_list, column_indices):
    for i in column_indices:
        data_list = normalization_by_line(data_list, i)

    return data_list

def get_indicator(a, b):
    if a == b == 0 or not a or not b:
        return 0
    else:
        return 1

def interval_similarity(a, b):
    # Using Euclidean distance, similarity is inversely related to distance
    distance_square = abs(a - b)
    # We will invert the distance to get a similarity measure. The closer the distance to 0, the higher the similarity.
    similarity = 1 / (1 + distance_square)
    return similarity

def asymmetric_similarity(a,b):
    return 1 if a == 1 and b == 1 else 0

def get_similarity_between_lines(r1, r2, interval_column_num, last_attr):
    assert len(r1) == len(r2)
    flag = 0 if last_attr else 1
    similarity_interval = [interval_similarity(r1[i], r2[i]) for i in range(interval_column_num)]
    similarity_asymmetric = [asymmetric_similarity(r1[i], r2[i]) for i in range(interval_column_num, len(r1)-flag)]
    return similarity_interval + similarity_asymmetric

def get_indicator_between_lines(r1, r2, last_attr):
    assert len(r1) == len(r2)
    flag = 0 if last_attr else 1
    indicator = [get_indicator(r1[i], r2[i]) for i in range(len(r1)-flag)]
    return indicator

def get_overall_similarity(r1, r2, interval_column_num, last_attr=False):
    similarities = get_similarity_between_lines(r1, r2, interval_column_num, last_attr)
    deltas = get_indicator_between_lines(r1, r2, last_attr)
    return sum(d * s for d, s in zip(deltas, similarities)) / sum(deltas)

def get_random_lines(data_list, line_num):
    l = len(data_list)
    number_range = [i for i in range(l)]
    random_numbers = random.sample(number_range, line_num)
    return [data_list[i] for i in random_numbers]

def get_similarity_between_data_list(data_list, interval_column_num, last_attr):
    l = len(data_list)
    s_list = []
    for i in range(l-1):
        for j in range(i+1, l):
            s_list.append(get_overall_similarity(data_list[i], data_list[j], interval_column_num, last_attr))
    return max(s_list), min(s_list), sum(s_list)/len(s_list)

def classify_by_datatypes(data_list_2d):
    res = {}
    for r in data_list_2d:
        datatype = r[-1]
        res[datatype] = res.get(datatype, [])
        res[datatype].append(r)
    return res

def get_random_lines_by_datatype(classified_data_dict, line_num):
    res = {}
    for datatype, data_list in classified_data_dict.items():
        res[datatype] = get_random_lines(data_list, line_num)
    return res

def print_similarities_by_types(classified_data_dict, interval_column_num):
    for datatype, data_list in classified_data_dict.items():
        ma, mi, av = get_similarity_between_data_list(data_list, interval_column_num, False)
        print(f'datatype:{datatype}, max:{ma}, min:{mi}, avg:{av}')


if __name__ == "__main__":
    dataset_file_path = '../dataset/covtype.data'
    line_num = 1000
    line_interval_num = 10

    print('Reading dataset...')
    data_list_2d = read_data_to_2d_list(dataset_file_path)
    print('Reading dataset is DONE.')

    print('Normalizing dataset...')
    data_list_2d_normalized = normalization(data_list_2d, [i for i in range(line_interval_num)])
    print('Normalizing dataset is DONE.')

    print('Getting 1000 random lines...')
    data_list_2d_normalized_1000_lines = get_random_lines(data_list_2d_normalized, line_num)
    print('Getting 1000 random lines is DONE.')

    print('Calculating similarities( last attribute not considered)...')
    ma, mi, av = get_similarity_between_data_list(data_list_2d_normalized_1000_lines, line_interval_num, False)
    print(f'max:{ma}, min:{mi}, avg:{av}')

    print('Calculating similarities( type considered)...')
    print_similarities_by_types(get_random_lines_by_datatype(classify_by_datatypes(data_list_2d_normalized), line_num), line_interval_num)
    # ma, mi, av = get_similarity_between_data_list(data_list_2d_normalized_1000_lines, True)
    # print(f'max:{ma}, min:{mi}, avg:{av}')




