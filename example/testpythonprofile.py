import os
import sys
import re
from ctypes import create_string_buffer, c_int, byref, cast, POINTER
import yaml
from pathlib import Path

from libximc import lib, Result, EnumerateFlags

from pyximc.settings.setting import ll_settings

if sys.version_info >= (3,0):
    import urllib.parse

def main():
    yml_file = Path(__file__).parent / "8MT173_25_MEn1.yml"

    print("//***************************************************************//")
    print("// This example demonstrates loading a profile for a positioner. //")
    print("//           The example uses the profile 8MT173-25-MEn1.        //")
    print("//If you use a different positioner, these settings may break it.//")
    print("//***************************************************************//")
    print(" ")
    confirm = input("To continue with the example, press y/n and press Enter: ")

    if not(confirm in {"y", "yes", "Y", "Yes"}):
        exit()

    sbuf = create_string_buffer(64)
    lib.ximc_version(sbuf)
    print("Library version: " + sbuf.raw.decode().rstrip("\0"))

    # This is device search and enumeration with probing. It gives more information about devices.
    probe_flags = EnumerateFlags.ENUMERATE_NETWORK # EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
    enum_hints = b"addr="
    devenum = lib.enumerate_devices(probe_flags, enum_hints)
    print("Device enum handle: " + repr(devenum))
    print("Device enum handle type: " + repr(type(devenum)))

    dev_count = lib.get_device_count(devenum)
    print("Device count: " + repr(dev_count))

    for dev_ind in range(0, dev_count):
        enum_name = lib.get_device_name(devenum, dev_ind)
        print(f"Enumerated device #{dev_ind} name (port name): " + repr(enum_name) + ". Friendly name: ")

    dev_name = lib.get_device_name(devenum, 0)
    if len(sys.argv) > 1:
        dev_name = sys.argv[1]
    elif dev_count > 0:
        dev_name = lib.get_device_name(devenum, 0)
    elif sys.version_info >= (3,0):
        # use URI for virtual device when there is new urllib python3 API
        tempdir = os.path.expanduser('~') + "/testdevice.bin"
        if os.altsep:
            tempdir = tempdir.replace(os.sep, os.altsep)
        # urlparse build wrong path if scheme is not file
        uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
                netloc=None, path=tempdir, params=None, query=None, fragment=None))
        dev_name = re.sub(r'^file', 'xi-emu', uri).encode()
        print()
        print("The real controller is NOT found or busy with another app.")
        print("The virtual controller is opened to check the operation of the library.")
        print("If you want to open a real controller, connect it or close the application that uses it.")

    if not dev_name:
        sys.exit()

    if isinstance(dev_name, str):
        dev_name = dev_name.encode()

    print("\nOpen device " + repr(dev_name))
    device_id = lib.open_device(dev_name)
    print("Device id: " + repr(device_id))

    with open(yml_file, "r", encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    if ll_settings(lib, device_id, settings, module="pyximc.settings.ll_flags") == Result.Ok:
        print("Download profile has been successfully completed.")
    else:
        print("The profile was loaded with errors.")

    print("\nClosing")

    # The device_t device parameter in this function is a C pointer, unlike most library functions that use this parameter
    lib.close_device(byref(cast(device_id, POINTER(c_int))))
    print("Done")

if __name__ == "__main__":
    main()
