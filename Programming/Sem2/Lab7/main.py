from time import sleep

from pilot import Pilot
from airplane import ControlSystem, Boeing737


def show_pilot_info(pilot):
    print("Pilot name:", pilot.name)
    print("Work experience:", pilot.work_experience)
    print("Focus level:", pilot.focus_level)


def show_airplane_info(airplane, show_main=False):
    print("Manufacturer:", airplane.manufacturer)
    if not show_main:
        print("Seats number:", airplane.seats_number)
        print("Wing length:", airplane.wing_length)
        print("Engine:", airplane.engine)
        print("Weight:", airplane.weight)
        print("Crew: {}, {}, {}".format(airplane.crew[0], airplane.crew[1], airplane.crew[2]))
    print("Traction:", airplane.traction)
    print("Position:", airplane.position)


def main():
    crew = [Pilot("Michi Kovalsky", 10), Pilot("Kolya Stepanov", 7), "Natalya Kolesnikova"]
    boeing737_airplane = Boeing737(crew)
    control_system = ControlSystem(boeing737_airplane)

    main_pilot = crew[0]
    show_pilot_info(main_pilot)

    print("\nMain pilot focusing on fly...\n")
    main_pilot.focus_on_flying()
    show_pilot_info(main_pilot)

    print("\nAirplane status:")
    show_airplane_info(boeing737_airplane)

    print("\nMain pilot moving helm 'Up' and pull lever to '6000'...")
    main_pilot.move_helm("Up", control_system)
    main_pilot.pull_lever(6000, control_system)

    print("\nAirplane start flying...")
    for _ in range(10):
        print("\nAirplane status (main):")
        show_airplane_info(boeing737_airplane, show_main=True)

        boeing737_airplane.fly()
        sleep(1)

    print("\nMain pilot enabling autopilot...")
    autopilot_status = main_pilot.enable_autopilot(control_system, 10, debug=True)
    print("\nAutopilot finished work with status", autopilot_status)


if __name__ == '__main__':
    main()
