#  Copyright (c) 2003-2022 Xsens Technologies B.V. or subsidiaries worldwide.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification,
#  are permitted provided that the following conditions are met:
#
#  1.	Redistributions of source code must retain the above copyright notice,
#  	this list of conditions, and the following disclaimer.
#
#  2.	Redistributions in binary form must reproduce the above copyright notice,
#  	this list of conditions, and the following disclaimer in the documentation
#  	and/or other materials provided with the distribution.
#
#  3.	Neither the names of the copyright holders nor the names of their contributors
#  	may be used to endorse or promote products derived from this software without
#  	specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
#  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
#  THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
#  OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.THE LAWS OF THE NETHERLANDS
#  SHALL BE EXCLUSIVELY APPLICABLE AND ANY DISPUTES SHALL BE FINALLY SETTLED UNDER THE RULES
#  OF ARBITRATION OF THE INTERNATIONAL CHAMBER OF COMMERCE IN THE HAGUE BY ONE OR MORE
#  ARBITRATORS APPOINTED IN ACCORDANCE WITH SAID RULES.
#
# Modifications of the example file "example_mti_parse_logfile.py" from Movella B.V.
# by Victor P. M. Brossard <support@trinoma.fr>, Trinoma SARL, France

from glob import glob
import os
from pathlib import Path
import xsensdeviceapi as xda

source_dir = os.path.expanduser('~/data/kuopio-full-body-dataset/s01_raw/')
results_dir = os.path.expanduser('~/data/kuopio-full-body-dataset/s02_extracted/')

delimiter = "\t"  # Change this to "," for CSV, "|" for pipe-separated, etc.

header_fields = [
    "PacketCounter",
    "Acc_X", "Acc_Y", "Acc_Z",
    "Gyr_X", "Gyr_Y", "Gyr_Z",
    "Mag_X", "Mag_Y", "Mag_Z",
    "Quat_q0", "Quat_q1", "Quat_q2", "Quat_q3",
    "Roll", "Pitch", "Yaw",
    "Mat[1][1]", "Mat[2][1]", "Mat[3][1]",
    "Mat[1][2]", "Mat[2][2]", "Mat[3][2]",
    "Mat[1][3]", "Mat[2][3]", "Mat[3][3]"
]
data_header = delimiter.join(header_fields)


def export_one_file(filename) -> None:
    """Export one MTB file to an ASCII file containing the data.

    Args:
        filename (str): path to the MTB file to be exported

    Returns:
        None
    """

    print("Creating XsControl object...")
    control = xda.XsControl_construct()
    assert (control != 0)

    xdaVersion = xda.XsVersion()
    xda.xdaVersion(xdaVersion)

    print("Using XDA version %s" % xdaVersion.toXsString())

    print("Opening log file...", filename)
    if not control.openLogFile(filename):
        raise RuntimeError("Failed to open log file. Aborting.")
    print("Opened log file: %s" % filename)

    # Get the device object
    print(control.deviceIds())
    devices = control.deviceIds()

    print("Closing XsControl object...")
    control.close()

    # Skip first element which is base station
    for device_id in devices[1:]:
        print("Creating XsControl object...")
        control = xda.XsControl_construct()
        assert (control != 0)

        print("Opening log file...", filename)
        if not control.openLogFile(filename):
            raise RuntimeError("Failed to open log file. Aborting.")
        print("Opened log file: %s" % filename)

        print(device_id)
        device = control.device(device_id)

        assert (device != 0)

        print("Device: %s, with ID: %s found in file" % (device.productCode(), device.deviceId().toXsString()))

        # By default XDA does not retain data for reading it back.
        # By enabling this option XDA keeps the buffered data in a cache so it can be accessed
        # through XsDevice::getDataPacketByIndex or XsDevice::takeFirstDataPacketInQueue
        device.setOptions(xda.XSO_RetainBufferedData, xda.XSO_None)

        # Load the log file and wait until it is loaded
        # Wait for logfile to be fully loaded, there are three ways to do this:
        # - callback: Demonstrated here, which has loading progress information
        # - waitForLoadLogFileDone: Blocking function, returning when file is loaded
        # - isLoadLogFileInProgress: Query function, used to query the device if the loading is done
        #
        # The callback option is not used here.
        header_info = [
            [' General information', ''],
            ['Update Rate', f"{device.updateRate()}Hz"],
            ['MT Manager version', '2022.2.0'],
            ['XDA version', xdaVersion.toXsString()],
            [' Device information', ''],
            ['DeviceId', device.deviceId().toXsString()],
            ['ProductCode', device.productCode()],
            ['Firmware Version', device.firmwareVersion().toXsString()],
            ['Hardware Version', device.hardwareVersion().toXsString()],
            [' Device settings', ''],
            ['Filter Profile', device.xdaFilterProfile().toXsString()],
            ['Option Flags', device.getOptions()],
            # ['Coordinate system', device.outputConfiguration()[0]]
        ]
        print("Loading the device file...")
        device.loadLogFile()
        device.waitForLoadLogFileDone()
        print("File is fully loaded")

        # Get total number of samples
        packetCount = device.getDataPacketCount()

        # Export the data
        print("Exporting the data...", packetCount)
        s = ''
        index = 0
        while index < packetCount:
            # Retrieve a packet
            packet = device.getDataPacketByIndex(index)
            packetCounter = packet.packetCounter()
            # if index == 0:
            #     header_info.append(['Coordinate system', packet.coordinateSystemOrientation()])
            # Assume variables packetCounter and sampleTimeFine are defined elsewhere
            if packet.containsCalibratedData():
                acc = packet.calibratedAcceleration()
                gyr = packet.calibratedGyroscopeData()
                mag = packet.calibratedMagneticField()
            else:
                acc = gyr = mag = [float('nan')] * 3

            if packet.containsOrientation():
                quat = packet.orientationQuaternion()
                euler = packet.orientationEuler()
                matrix = packet.orientationMatrix()  # 3x3 rotation matrix
                # Flatten in column-major order
                mat_vals = [matrix[0][0], matrix[1][0], matrix[2][0],
                            matrix[0][1], matrix[1][1], matrix[2][1],
                            matrix[0][2], matrix[1][2], matrix[2][2]]
                roll = euler.x()
                pitch = euler.y()
                yaw = euler.z()
            else:
                quat = [float('nan')] * 4
                roll = pitch = yaw = float('nan')
                mat_vals = [float('nan')] * 9

            row_parts = [
                f"{packetCounter:05d}",
                f"{acc[0]:.15f}", f"{acc[1]:.15f}", f"{acc[2]:.15f}",
                f"{gyr[0]:.15f}", f"{gyr[1]:.15f}", f"{gyr[2]:.15f}",
                f"{mag[0]:.15f}", f"{mag[1]:.15f}", f"{mag[2]:.15f}",
                f"{quat[0]:.15f}", f"{quat[1]:.15f}", f"{quat[2]:.15f}", f"{quat[3]:.15f}",
                f"{roll:.15f}", f"{pitch:.15f}", f"{yaw:.15f}"
            ] + [f"{val:.15f}" for val in mat_vals]
            row = delimiter.join(row_parts)
            # print(row)
            
            s += row
            s += "\n"

            index += 1
        file_path = Path(filename)
        device_stem = file_path.stem
        exportFileName = f"{device_stem}-{device_id}.txt"
        
        # Maintain the relative path structure
        
        first_parent = file_path.parent
        second_parent = first_parent.parent

        target_dir = Path(results_dir) / second_parent.name / first_parent.name
        target_dir.mkdir(parents=True, exist_ok=True)

        export_file_path = target_dir / exportFileName

        print(export_file_path)

        with open(export_file_path, "w") as outfile:
            header = ''
            for item in header_info:
                if item[1]:  # If there's a value in the second part of the list
                    header += f"// {item[0]}: {item[1]}\n"
                else:  # If there's no value, just print the section title
                    header += f"// {item[0]}\n"
            outfile.write(header)
            outfile.write(data_header + "\n")
            outfile.write(s)

        print("File is exported to: %s" % export_file_path)


        print("Closing XsControl object...")
        control.close()


if __name__ == '__main__':

    all_mtb_files = glob(os.path.join(source_dir, "**", "imu", "*.mtb"), recursive=True)

    # Create the directory
    try:
        os.mkdir(results_dir)
        print(f"Directory '{results_dir}' created successfully.")
    except FileExistsError:
        print(f"Directory '{results_dir}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{results_dir}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
   
    for file in all_mtb_files:
        try:
            export_one_file(file)
        except:
            print("error with file: ", file)
        # break