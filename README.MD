# Batch export MTB -> ASCII

Script designed to export all `.mtb` files from a directory to `.txt` files.

The script is heavily based on the example script from Movella B.V. `example_mti_parse_logfile.py` that is provided when installing the [MT Software Suite](https://www.movella.com/support/software-documentation).

This script is released under the GNU GPLv3 license.

In order to use it, you should change the `data_dir` (line 138), otherwise it will search for `.mtb` files inside the current directory.
You can also change the data that will be exported, from lines 96 to 122.