from pilot import Pilot


class ControlSystem:
    status = "OK"

    def __init__(self, airplane):
        self.airplane = airplane

    def read_flight_indicators(self):
        return {
            "traction": self.airplane.traction,
            "position": self.airplane.position,
            "weight": self.airplane.weight,
            "engine": self.airplane.engine,
        }

    @staticmethod
    def display_message(message):
        print(message)

    def open_flaps(self, direction):
        self.airplane.traction[0] = direction

    def change_traction(self, number):
        self.airplane.traction[1] = number


class Airplane:
    weight = 1000
    wing_length = 3.2
    traction = ["Down", 0]
    engine = "Pratt & Whitney JT5D"
    position = {'x': 0, 'y': 0}

    def fly(self):
        if self.traction[0] == "Up":
            self.position['y'] += self.traction[1] / self.weight
        if self.traction[0] == "Down":
            self.position['y'] -= self.traction[1] / self.weight
        if self.traction[0] == "Left":
            self.position['x'] -= self.traction[1] / self.weight
        if self.traction[0] == "Right":
            self.position['x'] += self.traction[1] / self.weight


class Boeing737(Airplane):
    manufacturer = "Boeing"
    __interior_width = 5.25
    seats_number = 220

    weight = 5000
    wing_length = 6.4
    engine = "Pratt & Whitney JT8D"

    def __init__(self, crew=None):
        if crew is None:
            crew = [Pilot("Michi Kovalsky", 10), Pilot("Kolya Stepanov", 7), "Natalya Kolesnikova"]
        self.crew = crew

    def fly(self):
        if self.crew[0].work_experience > 5:
            if self.traction[0] == "Up" and self.traction[1] > 1000:
                self.position['y'] += self.traction[1] / self.weight
            if self.traction[0] == "Down" and self.traction[1] > 1000:
                self.position['y'] -= self.traction[1] / self.weight
            if self.traction[0] == "Left" and self.traction[1] > 1000:
                self.position['x'] -= self.traction[1] / self.weight
            if self.traction[0] == "Right" and self.traction[1] > 1000:
                self.position['x'] += self.traction[1] / self.weight
            return "OK"
        return "Work experience of the main pilot is lower than 5 years. Change the main pilot."
