import math

from dataSet import SpatialDataset, dataFrame


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

    def get_cell(self, data_frame: dataFrame):
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

    def add_dataframe(self, data_frame: dataFrame):
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

    def add_data_frame(self, data_frame: dataFrame):
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
