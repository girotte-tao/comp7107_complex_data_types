from dataIndex import GridDirIndex
from dataset_constructor import DataFrame


class GridDataset:
    def __init__(self, file_path, index: GridDirIndex):
        self.file_path = file_path
        self.cell_points_dict = {}

        if index:
            self.index = index
            self.construct_with_index()

        return

    def construct_with_index(self):
        filename = self.file_path
        try:
            with open(filename, 'r') as file:
                for cell, value in list(self.index.grid_index_dict.items()):
                    start_position = value.char_index
                    num_points = value.point_num
                    file.seek(start_position)  # 移动到指定的起始位置
                    lines = []
                    for _ in range(num_points):
                        line = file.readline()
                        lines.append(line)
                    self.cell_points_dict[cell] = self.get_data_frames_by_lines(lines)
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except IOError:
            print(f"Error when reading file {filename}.")
        except Exception as e:
            print(f"Error：{e}")

    def get_data_frames_by_lines(self, lines):
        data_frames = []
        for line in lines:
            identifier, x, y = line.split()
            d = DataFrame(int(identifier), float(x), float(y), line)
            data_frames.append(d)
        return data_frames
