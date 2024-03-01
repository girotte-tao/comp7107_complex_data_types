from dataSet import SpatialDataset, dataFrame

class SpatialDataIndex:
    def __init__(self, dataset: SpatialDataset):
        self.dataset = dataset
        self.x_levels = [dataset.x_min + i*(dataset.x_max - dataset.x_min)/10 for i in range(11)]
        self.y_levels = [dataset.y_min + i*(dataset.y_max - dataset.y_min)/10 for i in range(11)]
        self.set_cells()

    def get_level(self, value, levels):
        level = 0
        for i in range(len(levels)):
            if value > levels[i]:
                level = i
            else:
                break
        return level

    def get_cell(self, data_frame: dataFrame):
        x_level = self.get_level(data_frame.x_coordinate,self.x_levels)
        y_level = self.get_level(data_frame.y_coordinate, self.y_levels)
        cell = (x_level, y_level)
        data_frame.set_cell(cell)

    def set_cells(self):
        for data_frame in self.dataset.data_frames:
            self.get_cell(data_frame)


    # def construct_index(self):


