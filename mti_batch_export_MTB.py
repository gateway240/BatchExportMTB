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
import xsensdeviceapi as xda


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

    print("Opening log file...")
    if not control.openLogFile(filename):
        raise RuntimeError("Failed to open log file. Aborting.")
    print("Opened log file: %s" % filename)

    # Get the device object
    device = control.device(control.deviceIds()[1])
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

    print("Loading the file...")
    device.loadLogFile()
    device.waitForLoadLogFileDone()
    print("File is fully loaded")

    # Get total number of samples
    packetCount = device.getDataPacketCount()

    # Export the data
    print("Exporting the data...")
    s = ''
    index = 0
    while index < packetCount:
        # Retrieve a packet
        packet = device.getDataPacketByIndex(index)

        if packet.containsCalibratedData():
            acc = packet.calibratedAcceleration()
            s += f"Acc X: {acc[0]:.2f}, Acc Y: {acc[1]:.2f}, Acc Z: {acc[2]:.2f}"

            gyr = packet.calibratedGyroscopeData()
            s += f" |Gyr X: {gyr[0]:.2f}, Gyr Y: {gyr[1]:.2f}, Gyr Z: {gyr[2]:.2f}"

            mag = packet.calibratedMagneticField()
            s += f" |Mag X: {mag[0]:.2f}, Mag Y: {mag[1]:.2f}, Mag Z: {mag[2]:.2f}"

        if packet.containsOrientation():
            quaternion = packet.orientationQuaternion()
            s += f"q0: {quaternion[0]:.2f}, q1: {quaternion[1]:.2f}, q2: {quaternion[2]:.2f}, q3: {quaternion[3]:.2f}"

            euler = packet.orientationEuler()
            s += f" |Roll: {euler.x():.2f}, Pitch: {euler.y():.2f}, Yaw: {euler.z():.2f}"

        if packet.containsLatitudeLongitude():
            latlon = packet.latitudeLongitude()
            s += f" |Lat: {latlon[0]:7.2f}, Lon: {latlon[1]:7.2f}"

        if packet.containsAltitude():
            s += f" |Alt: {packet.altitude():7.2f}"

        if packet.containsVelocity():
            vel = packet.velocity(xda.XDI_CoordSysEnu)
            s += f" |E: {vel[0]:7.2f}, N: {vel[1]:7.2f}, U: {vel[2]:7.2f}"

        s += "\n"

        index += 1

    exportFileName = f"{filename.split('.mtb')[0]}.txt"
    with open(exportFileName, "w") as outfile:
        outfile.write(s)
    print("File is exported to: %s" % exportFileName)

    print("Closing XsControl object...")
    control.close()


if __name__ == '__main__':
    data_dir = os.getcwd()
    all_mtb_files = glob(os.path.join(data_dir, "**", "*.mtb"), recursive=True)
    for file in all_mtb_files:
        export_one_file(file)
