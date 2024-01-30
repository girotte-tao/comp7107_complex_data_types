from fileReader import read_data_to_2d_list


def sort_by_column_index(data_list_2d, column_index):
    data_list_2d_sorted = sorted(data_list_2d, key=lambda x: x[column_index])
    return data_list_2d_sorted


def get_pair_num_by_k(data_list_2d_sorted, k, column_index):
    cnt = 0

    def explore(index, k):
        base = data_list_2d_sorted[index][column_index]
        cnt = 0
        for i in range(index,len(data_list_2d_sorted)):
            if data_list_2d_sorted[i][column_index] - base <= k:
                cnt += 1
                i += 1
            else: break
        return cnt - 1

    for record_index in range(len(data_list_2d_sorted)):
        cnt += explore(record_index, k)

    return cnt



if __name__ == "__main__":
    dataset_file_path = '../dataset/covtype.data'

    print('Reading dataset...')
    data_list_2d = read_data_to_2d_list(dataset_file_path)
    print('Reading dataset is DONE.')

    print('Sorting dataset...')
    data_list_2d_sorted = sort_by_column_index(data_list_2d, 0)
    print('Sorting dataset is DONE.')

    while True:
        k = int(input('Please enter k (enter -1 to stop):'))
        if k == -1:
            print('END...')
            break
        print('In process, please wait...')
        print(get_pair_num_by_k(data_list_2d_sorted, k, 0))
        print()