# Batch export MTB -> ASCII

Script designed to export all `.mtb` files from a directory to `.txt` files.

## General information
The script is heavily based on the example script from Movella B.V. `example_mti_parse_logfile.py` that is provided when installing the [MT Software Suite](https://www.movella.com/support/software-documentation).

## Usage notes
In order to use it, you should change the `data_dir` (line 138), otherwise it will search for all `.mtb` files inside the current directory (and sub-directories, recursively).
You can also change the data that will be exported, from lines 96 to 122.

If you have several MTw devices recorded in your `.mtb` file, change the index of the device to be loaded (line 62).

By default, the script will write one `.txt` file for each `.mtb` file it has found.
The output filename will be the same as the input filename, except for the file extension (i.e., `data01.mtb` will be exported as `data01.txt`).

The ASCII file can then be read with softwares such as LibreOffice Calc.
In that case, set the separators to `,` and `|`.

## License
This script is released under the GNU GPLv3 license.
The full license file can be found [here](LICENSE.md)