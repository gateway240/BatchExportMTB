# Batch export MTB -> ASCII

Script designed to export all `.mtb` files from a directory to `.txt` files.

## General information
The script is heavily based on the example script from Movella B.V. `example_mti_parse_logfile.py` that is provided when installing the [MT Software Suite](https://www.movella.com/support/software-documentation).

## Example usage

```bash
# usage: mti_batch_export_MTB.py [-h] --source-dir SOURCE_DIR --results-dir RESULTS_DIR [--pattern PATTERN]

# Kuopio Full Body Dataset format
python3 mti_batch_export_MTB.py --source-dir "~/data/kuopio-full-body-dataset/s01_raw/" --results-dir "~/data/mtb-test/results"

# Generic sample dir with .mtb files
python3 mti_batch_export_MTB.py --source-dir "~/data/mtb-test" --results-dir "~/data/mtb-test/results" --glob_pattern "**/*.mtb"

```

## Usage notes
The source directory, results directory, and file search glob pattern are parameterizable with command line args.

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

For example (MTSDK 2025.5.0 wheel for Python 3.11 on Linux):
pip install /usr/local/xsens/python/xsensdeviceapi-2025.5.0-cp311-none-linux_x86_64.whl

For example (MTSDK 2021.0.0 wheel for Python 3.9 on Windows):
pip install xsensdeviceapi-2021.0.0-cp39-none-win_amd64.whl

3. Now you are ready to run the MT SDK in Python

```

## License
This script is released under the GNU GPLv3 license.
The full license file can be found [here](LICENSE.md)
