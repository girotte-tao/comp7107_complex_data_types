from typing import List
from dataIndex import GridBound, GridDirIndex
from dataset_constructor import DataFrame
from grid_dataset import GridDataset


class GridBoundQuerySearcher:
    def __init__(self, index: GridDirIndex, dataset: GridDataset):
        self.index = index
        self.dataset = dataset

    def get_bound_level_target_points(self, grid_bound: GridBound):
        target_points = []
        cells_bound = self.index.get_bound_cells(grid_bound)
        for cell in cells_bound:
            for point in self.dataset.cell_points_dict[cell]:
                if self.is_target(point, grid_bound):
                    target_points.append(point)

        return target_points

    def get_points_by_cells(self, cells):
        points = []
        for cell in cells:
            points.append(self.dataset.cell_points_dict[cell])
        return points

    def is_target(self, point: DataFrame, grid_bound: GridBound):
        return grid_bound.x_lower_bound < point.x_coordinate < grid_bound.x_upper_bound and grid_bound.y_lower_bound < point.y_coordinate < grid_bound.y_upper_bound

    def search_by_bound(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        grid_bound = GridBound(x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)
        cells_in_between = self.index.get_cells_in_between(grid_bound)
        points_in_between = self.get_points_by_cells(cells_in_between)
        points_bound = self.get_bound_level_target_points(grid_bound)
        return points_in_between + points_bound

    def print_by_point_list(self, points: List[DataFrame]):
        for point in points:
            print(f'{point.identifier} {point.x_coordinate} {point.y_coordinate}')
        print(len(points))
        return

    def search_and_print_by_bound(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        return self.print_by_point_list(
            self.search_by_bound(x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound))
