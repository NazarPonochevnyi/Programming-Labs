from time import sleep
from random import choice, randint


class Pilot:
    focus_level = 0

    def __init__(self, name="Vasya Pechkin", work_experience=0):
        self.name = name
        self.work_experience = work_experience

    def __str__(self):
        return self.name

    @property
    def work_experience(self):
        return self.__work_experience

    @work_experience.setter
    def work_experience(self, work_experience):
        if work_experience < 0:
            self.__work_experience = 0
        elif work_experience > 100:
            self.__work_experience = 100
        else:
            self.__work_experience = work_experience

    @staticmethod
    def move_helm(direction, control_system):
        control_system.open_flaps(direction)

    @staticmethod
    def pull_lever(number, control_system):
        control_system.change_traction(number)

    @staticmethod
    def enable_autopilot(control_system, time, debug=False):
        autopilot = Autopilot(control_system)
        autopilot.run(time, debug)
        return autopilot.status

    def focus_on_flying(self):
        self.focus_level += 10


class Autopilot:
    status = 0

    def __init__(self, control_system):
        self.control_system = control_system

    def run(self, time, debug=False):
        self.status = 1
        for _ in range(time):
            route = self.get_route()
            airplane_data = self.get_airplane_data()
            if debug:
                print("\nAutopilot ask for the route from dispatcher...")
                print("Route from dispatcher:", route)
                print("Airplane traction:", airplane_data['traction'])
                print("Autopilot corrected airplane's traction")
            self.correct_airplane_data(route, airplane_data)
            sleep(1)
        self.status = 0

    @staticmethod
    def get_route():
        # actually, we need to get the route from dispatcher,
        # but we don't want to build a complex system, so we will generate route randomly
        direction = choice(["Up", "Down", "Left", "Right"])
        power = randint(1000, 5000)
        traction = [direction, power]
        return traction

    def get_airplane_data(self):
        return self.control_system.read_flight_indicators()

    def correct_airplane_data(self, route, airplane_data):
        route_direction, route_power = route
        direction, power = airplane_data['traction']
        if direction != route_direction:
            self.control_system.open_flaps(route_direction)
        if power != route_power:
            self.control_system.change_traction(route_power)
