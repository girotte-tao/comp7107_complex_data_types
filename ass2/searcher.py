import math
from typing import List
from dataIndex import GridBound, GridDirIndex, GridDirIndexFrame
from dataset_constructor import DataFrame
from grid_dataset import GridDataset
import heapq


class GridBoundQuerySearcher:
    def __init__(self, index: GridDirIndex, dataset: GridDataset):
        self.index = index
        self.dataset = dataset

    def get_bound_level_target_points(self, grid_bound: GridBound, cells_in_between):
        target_points = []
        cells_bound = self.index.get_bound_cells(grid_bound, cells_in_between)
        for cell in cells_bound:
            points = self.dataset.cell_points_dict.get(cell, [])
            for point in points:
                if self.is_target(point, grid_bound):
                    target_points.append(point)

        return target_points

    def get_points_by_cells(self, cells):
        points = []
        for cell in cells:
            points = points + self.dataset.cell_points_dict[cell]
        return points

    def is_target(self, point: DataFrame, grid_bound: GridBound):
        return grid_bound.x_lower_bound < point.x_coordinate < grid_bound.x_upper_bound and grid_bound.y_lower_bound < point.y_coordinate < grid_bound.y_upper_bound

    def search_by_bound(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        grid_bound = GridBound(x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound)
        cells_in_between = self.index.get_cells_in_between(grid_bound)
        points_in_between = self.get_points_by_cells(cells_in_between)
        points_bound = self.get_bound_level_target_points(grid_bound, cells_in_between)
        return points_in_between + points_bound

    def print_by_point_list(self, points: List[DataFrame]):

        for point in points:
            try:
                print(f'{point.identifier} {point.x_coordinate} {point.y_coordinate}')
            except Exception as e:
                print(e, point)
        print(f'Total number of the query result is {len(points)}.')

        return

    def search_and_print_by_bound(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        return self.print_by_point_list(
            self.search_by_bound(x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound))


class GridNearestKSearcher:
    def __init__(self, index: GridDirIndex, dataset: GridDataset):
        self.index = index
        self.dataset = dataset
        self.visited_cells = set()
        self.priority_queue = []

    def search_neighbor_cells(self, cell):
        # Get neighboring cells of the current cell and points within the cell
        # Placeholder implementation
        # This should be replaced with actual logic to retrieve neighboring cells
        cell_x, cell_y = cell
        neighbors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx != 0 or dy != 0:
                    new_cell_x = cell_x + dx
                    new_cell_y = cell_y + dy
                    if 0 <= new_cell_x < 10 and 0 <= new_cell_y < 10:
                        neighbors.append((new_cell_x, new_cell_y))
        return neighbors

    def initialize_search(self, query_point: DataFrame):
        # Find the starting cell(s) based on the query point and add to the priority queue
        # Placeholder implementation
        # This should be replaced with actual logic to find starting cells
        starting_cell = self.index.get_cell_by_point(query_point)
        query_point.cell = starting_cell
        self.visited_cells.add(starting_cell)
        # push all points in the starting cell
        points_in_starting_cell = self.dataset.cell_points_dict[starting_cell]
        self.push_points(points_in_starting_cell, query_point)
        neighbour_cells = [self.index.grid_index_dict[c] for c in self.search_neighbor_cells(starting_cell)]
        self.push_cells(neighbour_cells, query_point)

    def push_points(self, points: List[DataFrame], query_point: DataFrame):
        for point in points:
            heapq.heappush(self.priority_queue,
                           (self.get_min_dist_between_points(point, query_point), point.identifier, point))
            # print(self.priority_queue)

    def push_cells(self, cells: List[GridDirIndexFrame], query_point: DataFrame):
        for cell in cells:
            heapq.heappush(self.priority_queue,
                           (self.get_min_dist_between_point_cell(cell, query_point), cell.cell, cell))
            # print(self.priority_queue)

    def get_min_dist_between_point_cell(self, cell: GridDirIndexFrame, point: DataFrame):

        # if x of cell equals, use projection of y
        # if y of cell equals, use projection of x
        # else calculate the sqrt

        point_cell_x, point_cell_y = point.cell
        cell_x, cell_y = cell.cell

        if point_cell_x == cell_x:
            return min(abs(point.y_coordinate - cell.grid_bound.y_lower_bound),
                       abs(point.y_coordinate - cell.grid_bound.y_upper_bound))
        elif point_cell_y == cell_y:
            return min(abs(point.x_coordinate - cell.grid_bound.x_lower_bound),
                       abs(point.x_coordinate - cell.grid_bound.x_upper_bound))
        else:
            pro_x = min(abs(cell.grid_bound.x_lower_bound - point.x_coordinate), abs(cell.grid_bound.x_upper_bound - point.x_coordinate))
            pro_y = min(abs(cell.grid_bound.y_lower_bound - point.y_coordinate), abs(cell.grid_bound.y_upper_bound - point.y_coordinate))
            return math.sqrt(pro_x**2+pro_y**2)

    def get_min_dist_between_points(self, p1: DataFrame, p2: DataFrame):
        dist = math.sqrt((p1.x_coordinate - p2.x_coordinate) ** 2 + (p1.y_coordinate - p2.y_coordinate) ** 2)
        assert isinstance(dist, float)
        return dist

    def nearest_k_generator(self, query_point):
        while True:
            try:
                yield self.get_next_neighbour(query_point)
            except IndexError:
                break
        # yield self.get_next_neighbour(query_point)

    def get_next_neighbour(self, query_point):
        t = heapq.heappop(self.priority_queue)
        candidate = t[2]
        if isinstance(candidate, DataFrame):
            return candidate
        elif isinstance(candidate, GridDirIndexFrame):
            if candidate.cell not in self.visited_cells:
                self.visited_cells.add(candidate.cell)
                points = self.dataset.cell_points_dict[candidate.cell]
                self.push_points(points, query_point)
                neighbour_cells = [self.index.grid_index_dict[c] for c in self.search_neighbor_cells(candidate.cell)]
                self.push_cells(neighbour_cells, query_point)
            return self.get_next_neighbour(query_point)
        else:
            return None

    def search(self, point: DataFrame, k):
        self.initialize_search(point)

        generator = self.nearest_k_generator(point)
        print('Search results:')
        for i in range(k):
            try:
                p = next(generator)
                if p is not None:
                    print(f"{p.identifier} {p.x_coordinate} {p.y_coordinate}")
                    pass
                else:
                    break
            except StopIteration:
                break
        print('Cells with their contents read:')
        print(self.visited_cells)
        self.clear()

    def clear(self):
        self.visited_cells = set()
        self.priority_queue = []
