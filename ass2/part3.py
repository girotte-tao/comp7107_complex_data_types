from searcher import GridNearestKSearcher
from dataIndex import GridDirIndex
from grid_dataset import GridDataset
from dataset_constructor import DataFrame

if __name__ == '__main__':
    grid_dir_path = "grid.dir"
    grid_grd_path = "grid.grd"
    index = GridDirIndex(grid_dir_path)
    dataset = GridDataset(grid_grd_path, index)
    searcher = GridNearestKSearcher(index, dataset)

    while True:
        x_coordinate = input('Please enter the coordinate of x axis or type "exit" to quit:')
        if x_coordinate.lower() == 'exit':
            break
        x_coordinate = float(x_coordinate)

        y_coordinate = input('Please enter the coordinate of y axis or type "exit" to quit:')
        if y_coordinate.lower() == 'exit':
            break
        y_coordinate = float(y_coordinate)

        k = input('Please enter k or type "exit" to quit:')
        if k.lower() == 'exit':
            break
        k = int(k)

        p = DataFrame(None, x_coordinate, y_coordinate, None)

        searcher.search(p, k)


