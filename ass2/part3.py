from searcher import GridNearestKSearcher
from dataIndex import GridDirIndex
from grid_dataset import GridDataset
from dataset_constructor import DataFrame

def get_input(prompt, expected_type):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            return None
        try:
            if expected_type == float:
                return float(user_input)
            elif expected_type == int:
                return int(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {expected_type.__name__} or type 'exit' to quit.")

if __name__ == '__main__':
    grid_dir_path = "grid.dir"
    grid_grd_path = "grid.grd"
    index = GridDirIndex(grid_dir_path)
    dataset = GridDataset(grid_grd_path, index)
    searcher = GridNearestKSearcher(index, dataset)

    while True:
        x_coordinate = get_input('Please enter the coordinate of x axis or type "exit" to quit:', float)
        if x_coordinate is None:
            break

        y_coordinate = get_input('Please enter the coordinate of y axis or type "exit" to quit:', float)
        if y_coordinate is None:
            break

        k = get_input('Please enter k or type "exit" to quit:', int)
        if k is None:
            break

        p = DataFrame(None, x_coordinate, y_coordinate, None)
        searcher.search(p, k)
