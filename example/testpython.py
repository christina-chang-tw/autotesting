import time
import sys

import libximc.highlevel as ximc

from pyximc.manager.selection_manager import SelectionManager

def test_status(axis: ximc.Axis) -> None:
    print("\nGet status")
    status = axis.get_status()
    print(f"Status.Ipwr: {status.Ipwr}")
    print(f"Status.Upwr: {status.Upwr}")
    print(f"Status.Iusb: {status.Iusb}")
    print(f"Status.Flags: {status.Flags}")


def test_get_position(axis: ximc.Axis) -> 'tuple':
    print("\nRead position")
    pos = axis.get_position()
    print(f"Position: {pos.Position} steps, {pos.uPosition} microsteps")
    return pos.Position, pos.uPosition


def test_left(axis: ximc.Axis) -> None:
    print("\nMoving left")
    axis.command_left()


def test_move(axis: ximc.Axis, distance: int, udistance: int) -> None:
    print(f"\nGoing to {distance} steps, {udistance} microsteps")
    axis.command_move(distance, udistance)


def test_wait_for_stop(axis: ximc.Axis, interval: int) -> None:
    print("\nWaiting for stop...")
    axis.command_wait_for_stop(interval)


def test_get_speed(axis: ximc.Axis) -> int:
    print("\nGet speed")
    move_settings = axis.get_move_settings()
    return move_settings.Speed


def test_set_speed(axis: ximc.Axis, speed: int) -> None:
    print("\nSet speed")
    move_settings = axis.get_move_settings()
    print(f"The speed was equal to {move_settings.Speed}. We will change it to {speed}")
    move_settings.Speed = speed
    axis.set_move_settings(move_settings)


def test_set_microstep_mode_256(axis: ximc.Axis) -> None:
    print("\nSet microstep mode to 256")
    engine_settings = axis.get_engine_settings()

    # Change MicrostepMode parameter to MICROSTEP_MODE_FRAC_256
    # (use MICROSTEP_MODE_FRAC_128, MICROSTEP_MODE_FRAC_64 ... for other microstep modes)
    engine_settings.MicrostepMode = ximc.MicrostepMode.MICROSTEP_MODE_FRAC_256
    axis.set_engine_settings(engine_settings)

def main():
    print("Library version: " + ximc.ximc_version())

    devs = SelectionManager.get_devices_enumeration()
    print(f"Device count: {len(devs)}")
    print("Found devices:\n", devs)

    if len(sys.argv) > 1:
        uri = sys.argv[1]
    elif len(devs) > 0:
        uri = devs[0]["uri"]
    else:
        # set path to virtual device file to be created
        uri = SelectionManager.create_virtual_device()
        print("The real controller is NOT found or busy with another app.")
        print("The virtual controller is opened to check the operation of the library.")
        print("If you want to open a real controller, connect it or close the application that uses it.")


    # ******************************************** #
    #              Create axis object              #
    # ******************************************** #
    # Axis is the main libximc.highlevel class. It allows you to interact with the device.
    # Axis takes one argument - URI of the device
    axis = ximc.Axis(uri)
    print("\nOpen device: " + axis.uri)
    axis.open_device()  # The connection must be opened manually

    # ******************************************* #
    #                    Tests                    #
    # ******************************************* #
    test_status(axis)
    test_set_microstep_mode_256(axis)
    start_pos, ustart_pos = test_get_position(axis)
    # First move
    test_left(axis)
    time.sleep(3)
    test_get_position(axis)
    # Second move
    current_speed = test_get_speed(axis)
    test_set_speed(axis, current_speed // 2)
    test_move(axis, start_pos, ustart_pos)
    test_wait_for_stop(axis, 100)
    test_status(axis)

    print("\nClosing")
    axis.close_device()
    print("Done.")

if __name__ == "__main__":
    main()
