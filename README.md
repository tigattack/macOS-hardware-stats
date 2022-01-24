# macOS Hardware Stats

> Get CPU & GPU temperatures and fan and battery statistics from your Mac.

This simple script will output a JSON array containing hardware statistics from your Mac.

## Prerequisites

* Install [sensei](https://github.com/DrPsychick/homebrew-sensei).
  `brew install drpsychick/sensei/sensei`
* Install the `smc` binary.
  * Method 1:
    * Copy the [smc](smc) file to `/usr/local/bin` or your preferred location. You can specify the path with the `--smc-path` argument.
    * Run `chmod +x /usr/local/bin/smc`
  * Method 2:
    * Compile smc from the [included source](smc-command_src) (original source [here](github.com/hholtmann/smcFanControl/tree/master/smc-command)):
      ```bash
      cd ./smc-command_src
      make
      make install
      ```

## Usage

`./stats.py [-h] [--collection {all,temps} | --component {cpu,gpu,fans,battery} --fan {0,1}] [--smc-path SMC_PATH] [--sensei-path SENSEI_PATH]`

| **Argument**         | **Description**                                                                                                                                                                                                                 |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h`, `--help`       | Show help message.                                                                                                                                                                                                              |
| `-l`, `--collection` | The collection to query. Defaults to `all`.<br>Collections:<br>- `all`: Query supported statistics.<br>- `temperatures`: Query all supported temperature statistics.                                                            |
| `-c`, `--component`  | The component to query.<br>Components:<br>- `cpu`: Query supported CPU statistics.<br>- `gpu`: Query supported GPU statistics.<br>- `fans`: Query supported fan statistics.<br>- `battery`: Query supported battery statistics. |
| `-f`, `--fan`        | Fan number to query. Can ONLY be used with '{--component,-c} fans' argument. Defaults to all.<br>Fans:<br>- `0`: Left<br>- `1`: Right<br>- `all`: Query all fans.                                                               |

Example: `./stats.py`  
Output: `{"cpu": {"temperature": 76.9}, "gpu": {"temperature": 69.0}, "fans": [{"current_speed": 4437.0, "current_speed_pct": 60.4, "min_rpm": 2160, "max_rpm": 5927, "side": "left", "id": 0}, {"current_speed": 4079.0, "current_speed_pct": 59.5, "min_rpm": 2000, "max_rpm": 5489, "side": "right", "id": 1}]}`
