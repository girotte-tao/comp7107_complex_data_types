from searcher import GridBoundQuerySearcher
from dataIndex import GridDirIndex
from grid_dataset import GridDataset

def get_float_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            return None
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number or type 'exit' to quit.")

if __name__ == '__main__':
    grid_dir_path = "grid.dir"
    grid_grd_path = "grid.grd"
    index = GridDirIndex(grid_dir_path)
    dataset = GridDataset(grid_grd_path, index)
    searcher = GridBoundQuerySearcher(index, dataset)

    while True:
        x_lower = get_float_input('Please enter the lower bound of x axis or type "exit" to quit:')
        if x_lower is None:
            break

        x_upper = get_float_input('Please enter the upper bound of x axis or type "exit" to quit:')
        if x_upper is None:
            break

        y_lower = get_float_input('Please enter the lower bound of y axis or type "exit" to quit:')
        if y_lower is None:
            break

        y_upper = get_float_input('Please enter the upper bound of y axis or type "exit" to quit:')
        if y_upper is None:
            break

        points = searcher.search_and_print_by_bound(x_lower, x_upper, y_lower, y_upper)
