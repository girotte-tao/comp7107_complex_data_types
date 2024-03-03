from searcher import GridSearcher
from dataIndex import GridDirIndex
from grid_dataset import GridDataset


if __name__ == '__main__':
    grid_dir_path = "grid.dir"
    grid_grd_path = "grid.grd"
    index = GridDirIndex(grid_dir_path)
    dataset = GridDataset(grid_grd_path, index)
    searcher = GridSearcher(index, dataset)

    while True:
        x_lower_input = input('Please enter the lower bound of x axis or type "exit" to quit:')
        if x_lower_input.lower() == 'exit':
            break
        x_lower = float(x_lower_input)

        x_upper_input = input('Please enter the upper bound of x axis or type "exit" to quit:')
        if x_upper_input.lower() == 'exit':
            break
        x_upper = float(x_upper_input)

        y_lower_input = input('Please enter the lower bound of y axis or type "exit" to quit:')
        if y_lower_input.lower() == 'exit':
            break
        y_lower = float(y_lower_input)

        y_upper_input = input('Please enter the upper bound of y axis or type "exit" to quit:')
        if y_upper_input.lower() == 'exit':
            break
        y_upper = float(y_upper_input)

        points = searcher.search_and_print(x_lower, x_upper, y_lower, y_upper)

