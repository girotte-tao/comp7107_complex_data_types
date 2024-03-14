class SpatialDataset:
    def __init__(self, file_path):
        self.file_path = file_path
        restaurant_coordinates, x_coordinates, y_coordinates, data_frames = self.construct_dataset()
        self.restaurant_coordinates = restaurant_coordinates
        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.x_max = max(x_coordinates)
        self.x_min = min(x_coordinates)
        self.y_max = max(y_coordinates)
        self.y_min = min(y_coordinates)
        self.data_frames = data_frames

    def construct_dataset(self):
        restaurant_coordinates = []
        x_coordinates = []
        y_coordinates = []
        data_frames = []
        # Open the file for reading
        with open(self.file_path, 'r') as file:
            # Read the first line to get the number of lines (restaurants)
            num_restaurants = int(file.readline().strip())

            # Loop through the remaining lines to read the coordinates
            for i in range(num_restaurants):
                # Read the next line and split it into latitude and longitude
                raw_line = file.readline()
                line = raw_line.strip()
                if line:  # Ensure the line is not empty
                    identifier = i + 1
                    latitude, longitude = map(float, line.split())
                    x_coordinates.append(latitude)
                    y_coordinates.append(longitude)
                    # Store the coordinates as a tuple in the list
                    restaurant_coordinates.append((latitude, longitude))
                    data_frame = DataFrame(identifier, latitude, longitude, raw_line)
                    data_frames.append(data_frame)
        return restaurant_coordinates, x_coordinates, y_coordinates, data_frames

    def print_restaurant_coordinates(self):
        print("restaurant_coordinates")
        print(self.restaurant_coordinates)
        print("x_coordinates")
        print(self.x_coordinates)
        print("y_coordinates")
        print(self.y_coordinates)
        for i in self.data_frames:
            i.print_data_frame_cell()


class DataFrame:
    def __init__(self, identifier, x_coordinate, y_coordinate, raw_data):
        self.raw_data = raw_data
        self.identifier = identifier
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.coordinate = (x_coordinate, y_coordinate)
        self.cell = ()

    def set_cell(self, cell):
        self.cell = cell

    def print_data_frame_cell(self):
        print(self.cell)

    def __str__(self):
        return f'({self.x_coordinate}, {self.y_coordinate}) {self.cell}'


