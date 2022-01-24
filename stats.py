#! /usr/local/bin/python3
"""
Get macOS CPU & GPU temps and fan speeds.
This utility relies on https://github.com/hholtmann/smcFanControl/tree/master/smc-command
"""

# Imports
import argparse
import distutils.spawn
import json
import math
import os
import re
import subprocess
import sys

# Define SMC keys
SMC_KEYS = {
    "cpu_temp": "TCXC",
    "gpu_temp": "TCGC",
    "fan": {
        0: {"current": "F0Ac", "min": "F0Mn", "max": "F0Mx"},
        1: {"current": "F1Ac", "min": "F1Mn", "max": "F1Mx"},
    },
}


# Create argument parser
parser = argparse.ArgumentParser(description="Get Mac CPU & GPU temps, fan speeds, and\
    battery information. Select a component OR collection to query.")

# Create mutually exclusive arg group
arg_group = parser.add_mutually_exclusive_group()

# Add component and collection args
arg_group.add_argument(
    "--collection", "-l",
    choices = ["all", "temps"],
    help    = "Collection to query. Defaults to all"
)
arg_group.add_argument(
    "--component", "-c",
    choices = ["cpu", "gpu", "fans", "battery"],
    help    = "Component to query."
)
# Add fan selection arg
parser.add_argument(
    "--fan", "-f",
    choices = [0, 1],
    type    = int,
    help    = "fan number to query. Can ONLY be used with '{--component,-c} fans' argument.\
                Defaults to all."
)
# Add binary path args
parser.add_argument(
    "--smc-path",
    action  = "store",
    default = distutils.spawn.find_executable("smc"),
    help    = "path to smc binary (default: detected from PATH)"
)
parser.add_argument(
    "--sensei-path",
    action  = "store",
    default = distutils.spawn.find_executable("sensei"),
    help    = "path to sensei binary (default: detected from PATH)"
)


def smc_query(smc_key: str) -> dict:
    """Helper function to query SMC information."""

    # Create empty dict
    data = {}

    # Query the given SMC key and decode as utf-8
    query_result = (
        subprocess.check_output([SMC_PATH, "-k", smc_key, "-r"])
    ).decode("utf-8")

    # Compile regex pattern
    # pylint: disable=line-too-long
    pattern = re.compile(
        r"^\s{2}(?P<Key>(\w){4})\s{2}(\[(?P<Type>\w{3,4})\s?])\s{2}(?P<Value>.*?)?(\s)?(\(bytes\s(?P<Bytes>.*)\))$")

    # Search input_str data for pattern
    query_search = pattern.search(query_result)

    # If pattern is found
    if query_search:
        # Construct data
        data["Key"]     = query_search.group("Key")
        data["Type"]    = query_search.group("Type")
        data["Value"]   = query_search.group("Value")
        data["Bytes"]   = query_search.group("Bytes").replace(
            " ", "")  # Remove whitespace

        output = data

    # If pattern is not found
    else:
        output = f"No matches found in input_str data.\nRaw output:\n{data}\n"

    # Return query
    return output

def battery_query() -> dict:
    """Function to retrieve battery information."""

    # Create empty dict
    battery_dat = {}

    # Query battery information
    query_result = subprocess.check_output([SENSEI_PATH]).decode("utf-8").strip()

    # Parse output as dict
    for field in query_result.split(','):
        field_list = field.split('=')
        battery_dat[field_list[0]] = field_list[1]

    # Set data types
    battery_dat["temperature"]          = float(battery_dat["temperature"])
    battery_dat["charging"]             = bool(int(battery_dat["charging"]))
    battery_dat["remaining_cycles"]     = float(battery_dat["remaining_cycles"])
    battery_dat["remaining_capacity"]   = float(battery_dat["remaining_capacity"])
    battery_dat["capacity"]             = float(battery_dat["capacity"])

    # Rename capacity key
    battery_dat["charge_pct"]     = battery_dat.pop("capacity")

    # battery_dat[field_list[0].split('=')[0]] = float(field_list[0].split('=')[1])

    # Return battery information
    return battery_dat


def fan_count() -> int:
    """Helper function to return the number of fans in the system."""

    # Query fan count and return
    return int(smc_query("FNum")["Value"])


def truncate(number, digits) -> float:
    """Function to truncate numbers.
    https://stackoverflow.com/a/37697840/5209106"""

    stepper = 10.0 ** digits
    truncated_figure = math.trunc(stepper * number) / stepper
    return truncated_figure


def get_fan(fan_num: int) -> dict:
    """Helper function to return fan information."""

    # Define constants
    fan_dat = {}
    side    = {0: "left", 1: "right"}

    # Get fan data
    fan_current = float(smc_query(SMC_KEYS["fan"][fan_num]["current"])["Value"])
    fan_min     = int(smc_query(SMC_KEYS["fan"][fan_num]["min"])["Value"])
    fan_max     = int(smc_query(SMC_KEYS["fan"][fan_num]["max"])["Value"])

    # Calculate fan speed percentage
    fan_percent = (fan_current - fan_min) / (fan_max - fan_min) * 100

    # # Add info to dict, truncating all results to 1 decimal place. Truncation is only required
    # for fan_current, which by is returned with 12 decimal places by default. However, all
    # ints are truncated for the sake of consistency.
    fan_dat["current_rpm"]        = truncate(fan_current, 1)
    fan_dat["current_rpm_pct"]    = truncate(fan_percent, 1)
    fan_dat["min_rpm"]              = fan_min
    fan_dat["max_rpm"]              = fan_max
    fan_dat["side"]                 = side[fan_num]
    fan_dat["id"]                   = fan_num

    # Return fan information
    return fan_dat


def fan_info(fan_num: int = None):
    """Function to retrieve fan speed information."""

    # Define constants
    fan_dat = []

    # If fan_num is specified, gather information for that fan
    if fan_num is not None:
        fan_dat = get_fan(fan_num)

    # If fan_num is not specified, gather information for all fans
    else:
        for i in range(0, fan_count()):
            fan_dat.append(get_fan(i))

    # Return fan information
    return fan_dat


def cpu_temp() -> float:
    """Function to retrieve CPU temperature."""

    # Query CPU temperature
    query_result = smc_query(SMC_KEYS["cpu_temp"])["Value"]

    # Truncate result to 1 decimal place
    query_result = truncate(float(query_result), 1)

    # Return CPU temperature
    return query_result


def gpu_temp() -> float:
    """Function to retrieve GPU temperature."""

    # Query GPU temperature
    query_result = smc_query(SMC_KEYS["gpu_temp"])["Value"]

    # Truncate result to 1 decimal place
    query_result = truncate(float(query_result), 1)

    # Return GPU temperature
    return query_result


# Define main function
def main(input_str: str, fan_num: int = None) -> None:
    """Main function."""

    # Get all data
    if input_str == "all":
        stats = json.dumps({
            "cpu": {
                "temperature": cpu_temp()},
            "gpu": {
                "temperature": gpu_temp()},
            "fans": fan_info(),
            "battery": battery_query()
        })

    # Get battery data
    if input_str == "battery":
        stats = json.dumps(battery_query())

    # Get CPU data
    if input_str == "cpu":
        stats = json.dumps({"temperature": cpu_temp()})

    # Get GPU data
    if input_str == "gpu":
        stats = json.dumps({"temperature": gpu_temp()})

    # Get fan data
    if input_str == 'fans':
        if fan_num is None:
            stats = json.dumps(fan_info())
        else:
            if fan_num in range(fan_count()):
                stats = json.dumps(fan_info(fan_num))
            else:
                try:
                    raise KeyError('Invalid fan number.')
                except KeyError:
                    print(f"Fan number {fan_num} does not exist. Try 0 or 1.\n")
                    raise

    # Get temperature data
    if input_str == 'temps':
        stats = json.dumps({
            "cpu": {
                "temperature": cpu_temp()},
            "gpu": {
                "temperature": gpu_temp()},
            "battery": {
                "temperature": battery_query()["temperature"]}
        })

    # Output data
    print(stats)


if __name__ == "__main__":

    # Get command line arguments
    args = parser.parse_args()

    # Check binary paths exist
    if os.path.isfile(str(args.smc_path)):
        SMC_PATH = str(args.smc_path)
    else:
        print(f"smc binary path does not exist: {args.smc_path}\n" +
                "Please check/specify the '--smc-path' argument.")
        sys.exit(1)
    if os.path.isfile(str(args.sensei_path)):
        SENSEI_PATH = str(args.sensei_path)
    else:
        print(f"sensei binary path does not exist: {args.sensei_path}\n" +
                "Please check/specify the '--sensei-path' argument.")
        sys.exit(1)

    # Run main
    if args.component:
        if args.fan is None:
            main(args.component)
        else:
            main(args.component, args.fan)
    elif args.collection:
        if args.fan is None:
            main(args.collection)
        else:
            print("Invalid argument combination: {--fan,-f} can only be sepcified with " +
                "'{--component,-c} --fans'.\nSee --help for more information.")
    else:
        main("all")

# TODO
# Add pretty output
# Get more info using powermetrics.
# `sudo powermetrics --help` for some info on available stats.
