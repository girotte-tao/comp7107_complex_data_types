from dataset_constructor import SpatialDataset
from dataIndex import SpatialDataIndex


if __name__ == '__main__':
    dataset_path = "../dataset/Beijing_restaurants.txt"
    dataset = SpatialDataset(dataset_path)
    index = SpatialDataIndex(dataset)

    sorted_coordinates_path = "grid.grd"
    # sorted_coordinates_with_cell_path = "grid_with_cell.grd"

    cell_index_path = "grid.dir"
    index.save_sorted_coordinates(sorted_coordinates_path)
    # index.save_sorted_coordinates_with_cell(sorted_coordinates_with_cell_path)

    index.save_cell_index(cell_index_path)



