from time import sleep

from pilot import Pilot
from airplane import ControlSystem, Boeing737, AV8B


def iteration(airplanes):
    for airplane in airplanes:
        airplane.fly()


def show_pilot_info(pilot):
    print("Pilot name:", pilot.name)
    print("Work experience:", pilot.work_experience)
    print("Focus level:", pilot.focus_level)


def show_airplane_info(airplane, show_main=False):
    print("Manufacturer:", airplane.manufacturer)
    if not show_main:
        print("Wing length:", airplane.wing_length)
        print("Engine:", airplane.engine)
        print("Weight:", airplane.weight)
        print("Crew:")
        for p in airplane.crew:
            print(" - ", end='')
            print(p)
    print("Traction:", airplane.traction)
    print("Position:", airplane.position)


def main():
    military_airplane = AV8B()
    control_system = ControlSystem(military_airplane)

    crew = [Pilot("Kolya Stepanov", 10), Pilot("Taras Lopasov", 7), "Natalya Kolesnikova"]
    boeing737_airplane = Boeing737(crew)

    show_pilot_info(military_airplane.pilot)

    print("\nMilitary airplane pilot focusing on fly...\n")
    military_airplane.pilot.focus_on_flying()
    show_pilot_info(military_airplane.pilot)

    print("\nAirplane status:")
    show_airplane_info(military_airplane)
    print("\nAirplane status:")
    show_airplane_info(boeing737_airplane)

    print("\nMilitary airplane pilot moving helm 'Up' and pull lever to '6000'...")
    military_airplane.pilot.move_helm("Up", control_system)
    military_airplane.pilot.pull_lever(6000, control_system)

    print("\nAirplane start flying...")
    for _ in range(10):
        print("\nAirplane status (main):")
        show_airplane_info(military_airplane, show_main=True)

        iteration([military_airplane, boeing737_airplane])
        sleep(1)

    print("\nMilitary airplane pilot enabling autopilot...")
    autopilot_status = military_airplane.pilot.enable_autopilot(control_system, 10, debug=True)
    print("\nAutopilot finished work with status", autopilot_status)


if __name__ == '__main__':
    main()
