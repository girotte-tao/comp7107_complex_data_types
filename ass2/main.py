from dataSet import SpatialDataset
from dataIndex import SpatialDataIndex

if __name__ == '__main__':
    file_path = "../dataset/Beijing_restaurants.txt"
    dataset = SpatialDataset(file_path)
    dataset.print_restaurant_coordinates()

    index = SpatialDataIndex(dataset)
    index.dataset.print_restaurant_coordinates()
