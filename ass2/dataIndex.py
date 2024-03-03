import math

from dataset_constructor import SpatialDataset, DataFrame


class SpatialDataIndex:
    def __init__(self, dataset: SpatialDataset):
        self.dataset = dataset
        self.x_levels = [dataset.x_min + i * (dataset.x_max - dataset.x_min) / 10 for i in range(11)]
        self.y_levels = [dataset.y_min + i * (dataset.y_max - dataset.y_min) / 10 for i in range(11)]
        self.cell_domain_manager = CellDomainManager()
        self.set_cells()
        self.sorted_points = sorted(dataset.data_frames, key=lambda df: df.cell)
        self.sorted_domains = self.cell_domain_manager.get_sorted_cell_domain()

    def get_level(self, value, levels):
        level = 0
        for i in range(len(levels)):
            if value > levels[i]:
                level = i
            else:
                break
        return level

    def get_cell(self, data_frame: DataFrame):
        x_level = self.get_level(data_frame.x_coordinate, self.x_levels)
        y_level = self.get_level(data_frame.y_coordinate, self.y_levels)
        cell = (x_level, y_level)
        return cell

    def set_cells(self):
        for data_frame in self.dataset.data_frames:
            cell = self.get_cell(data_frame)
            data_frame.set_cell(cell)
            self.cell_domain_manager.add_data_frame(data_frame)

    def save_sorted_coordinates(self, file_path):
        with open(file_path, 'w') as file:
            for point in self.sorted_points:
                # Writing the coordinate of each point to the file, line by line
                file.write(f"{point.identifier} {point.coordinate[0]:.6f} {point.coordinate[1]:.6f}\n")
        print(f"Coordinates of sorted points have been saved to f{file_path}")

    def save_cell_index(self, file_path):
        with open(file_path, 'w') as file:
            file.write(
                f"{self.dataset.x_min:.6f} {self.dataset.x_max:.6f} {self.dataset.y_min:.6f} {self.dataset.y_max:.6f}\n")

            cur_character_num = 0
            for domain in self.sorted_domains:
                # Writing the coordinate of each point to the file, line by line
                file.write(f"{domain.cell[0]} {domain.cell[1]} {cur_character_num} {domain.data_frame_number}\n")
                cur_character_num += domain.character_length
        print(f"Coordinates of sorted points have been saved to f{file_path}")


class CellDomain:
    def __init__(self, cell):
        self.cell = cell
        self.first_identifier = math.inf
        self.data_frame_number = 0
        self.character_length = 0

    def add_dataframe(self, data_frame: DataFrame):
        assert self.cell == data_frame.cell
        if data_frame.identifier < self.first_identifier:
            self.first_identifier = data_frame.identifier
        self.data_frame_number = self.data_frame_number + 1
        self.character_length = self.character_length + len(f"{data_frame.x_coordinate:.6f}") + len(
            f"{data_frame.y_coordinate:.6f}") + len(str(data_frame.identifier)) + 3


class CellDomainManager:
    def __init__(self):
        self.cell_domain_dict = {}

    def add_cell_domain(self, cell):
        self.cell_domain_dict[str(cell)] = self.cell_domain_dict.get(str(cell), CellDomain(cell))

    def add_data_frame(self, data_frame: DataFrame):
        cell = data_frame.cell
        if self.is_exist(cell):
            self.cell_domain_dict[str(cell)].add_dataframe(data_frame)
        else:
            self.add_cell_domain(cell)
            self.cell_domain_dict[str(cell)].add_dataframe(data_frame)

    def is_exist(self, cell):
        return str(cell) in self.cell_domain_dict

    def get_cell_info(self, cell):
        return self.cell_domain_dict[str(cell)]

    def get_sorted_cell_domain(self):
        sorted_domains = [domain for key, domain in sorted(self.cell_domain_dict.items())]
        return sorted_domains


class GridBound:
    def __init__(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        self.x_lower_bound = x_lower_bound
        self.x_upper_bound = x_upper_bound
        self.y_lower_bound = y_lower_bound
        self.y_upper_bound = y_upper_bound


class GridDirIndexFrame:
    def __init__(self, cell, char_index, point_num, grid_bound: GridBound):
        self.cell = cell
        self.char_index = char_index
        self.point_num = point_num
        self.grid_bound = grid_bound


class GridDirIndex:
    def __init__(self, index_file_path):
        self.index_file_path = index_file_path
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.x_levels = None
        self.y_levels = None
        self.grid_index_dict = {}
        self.construct_index()

    def construct_index(self):
        with open(self.index_file_path, 'r') as file:
            # Read the first line to get the number of lines (restaurants)
            x_min, x_max, y_min, y_max = map(float, file.readline().strip().split())
            self.x_min = x_min
            self.x_max = x_max
            self.y_min = y_min
            self.y_max = y_max
            self.x_levels = [x_min + i * (x_max - x_min) / 10 for i in range(11)]
            self.y_levels = [y_min + i * (y_max - y_min) / 10 for i in range(11)]
            print(self.x_levels)
            print(self.y_levels)

            for i in range(100):
                raw_line = file.readline()
                line = raw_line.strip()
                if line:
                    cell0, cell1, char_index, point_num = map(int, line.split())
                    cell = (cell0, cell1)
                    grid_bound = GridBound(self.x_levels[cell0], self.x_levels[cell0 + 1], self.y_levels[cell0],
                                           self.y_levels[cell1])
                    grid_dir_index_frame = GridDirIndexFrame(cell, char_index, point_num, grid_bound)
                    self.grid_index_dict[cell] = grid_dir_index_frame
        return

    def get_level(self, value, levels):
        level = 0
        for i in range(len(levels)):
            if value > levels[i]:
                level = i
            else:
                break
        return level

    def get_cells_in_between(self, grid_bound: GridBound):
        x_lower_bound_level = self.get_level(grid_bound.x_lower_bound, self.x_levels)
        x_upper_bound_level = self.get_level(grid_bound.x_upper_bound, self.x_levels) + 1
        y_lower_bound_level = self.get_level(grid_bound.y_lower_bound, self.y_levels)
        y_upper_bound_level = self.get_level(grid_bound.y_upper_bound, self.y_levels) + 1

        cells_in_between = []

        for cell in list(self.grid_index_dict.keys()):
            if x_lower_bound_level < cell[0] < x_upper_bound_level and y_lower_bound_level < cell[1] < y_upper_bound_level:
                cells_in_between.append(cell)

        return cells_in_between

    def is_point_in_between(self, data_frame: DataFrame, grid_bound: GridBound):
        return grid_bound.x_lower_bound < data_frame.x_coordinate < grid_bound.x_upper_bound and grid_bound.y_lower_bound < data_frame.y_coordinate < grid_bound.y_upper_bound

    def get_bound_cells(self, grid_bound: GridBound):
        x_lower_bound_level = self.get_level(grid_bound.x_lower_bound, self.x_levels)
        x_upper_bound_level = self.get_level(grid_bound.x_upper_bound, self.x_levels)
        y_lower_bound_level = self.get_level(grid_bound.y_lower_bound, self.y_levels)
        y_upper_bound_level = self.get_level(grid_bound.y_upper_bound, self.y_levels)

        cells = set()
        cells.add((x_lower_bound_level, y_lower_bound_level))
        for x in range(x_upper_bound_level - x_lower_bound_level):
            cells.add((x_lower_bound_level + x + 1, y_lower_bound_level))
            cells.add((x_lower_bound_level + x + 1, y_upper_bound_level))
        for y in range(y_upper_bound_level - y_lower_bound_level):
            cells.add((y_lower_bound_level + y + 1, x_lower_bound_level))
            cells.add((y_lower_bound_level + y + 1, x_upper_bound_level))

        return list(cells)


