# Batch export MTB -> ASCII

Script designed to export all `.mtb` files from a directory to `.txt` files.

## General information
The script is heavily based on the example script from Movella B.V. `example_mti_parse_logfile.py` that is provided when installing the [MT Software Suite](https://www.movella.com/support/software-documentation).

## Usage notes
In order to use it, you should change the `data_dir` (line 138), otherwise it will search for all `.mtb` files inside the current directory (and subdirectories, recursively).
You can also change the data that will be exported, from lines 96 to 122.

If you have several MTw devices recorded in your `.mtb` file, change the index of the device to be loaded (line 62).

By default, the script will write one `.txt` file for each `.mtb` file it has found.
The output filename will be the same as the input filename, except for the file extension (i.e., `data01.mtb` will be exported as `data01.txt`).

The ASCII file can then be read with software such as LibreOffice Calc.
In that case, set the separators to `,` and `|`.

## Requirements
Do not forget to install the Xsens device API, using the following instructions (provided by Movella B.V.):

```txt
Before running the MT SDK Python example, the XDA (xsensdeviceapi)
Python interface needs to be installed using the included XDA wheel file.
Make sure to have the correct version of python and pip are installed on your machine.

Supported Python versions: 3.7.x up to 3.9.x

1. Make sure to have "wheel" installed on your machine:

pip install wheel

2. Install xsensdeviceapi wheel:

Located in 
Windows: <INSTALL_FOLDER>\MTSDK\Python\x64 or Win32
Linux: <INSTALL_FOLDER>/xsens/python

pip install xsensdeviceapi-<xda version>-cp<Python version>-none-<os type>.whl

For example (MTSDK 2021.0.0 wheel for Python 3.9 on Linux):
pip install xsensdeviceapi-2021.0.0-cp39-none-linux_x86_64.whl or

For example (MTSDK 2021.0.0 wheel for Python 3.9 on Windows):
pip install xsensdeviceapi-2021.0.0-cp39-none-win_amd64.whl

3. Now you are ready to run the MT SDK in Python

```

## License
This script is released under the GNU GPLv3 license.
The full license file can be found [here](LICENSE.md)