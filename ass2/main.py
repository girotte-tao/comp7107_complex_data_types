from dataSet import SpatialDataset
from dataIndex import SpatialDataIndex

if __name__ == '__main__':
    dataset_path = "../dataset/Beijing_restaurants.txt"

    dataset = SpatialDataset(dataset_path)
    # dataset.print_restaurant_coordinates()
    index = SpatialDataIndex(dataset)
    # index.dataset.print_restaurant_coordinates()

#     part 1
    sorted_coordinates_path = "grid.grd"
    cell_index_path = "grid.dir"
    index.save_sorted_coordinates(sorted_coordinates_path)
    index.save_cell_index(cell_index_path)

