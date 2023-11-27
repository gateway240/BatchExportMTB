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
            s += "Acc X: %.2f" % acc[0] + ", Acc Y: %.2f" % acc[1] + ", Acc Z: %.2f" % acc[2]

            gyr = packet.calibratedGyroscopeData()
            s += " |Gyr X: %.2f" % gyr[0] + ", Gyr Y: %.2f" % gyr[1] + ", Gyr Z: %.2f" % gyr[2]

            mag = packet.calibratedMagneticField()
            s += " |Mag X: %.2f" % mag[0] + ", Mag Y: %.2f" % mag[1] + ", Mag Z: %.2f" % mag[2]

        if packet.containsOrientation():
            quaternion = packet.orientationQuaternion()
            s += "q0: %.2f" % quaternion[0] + ", q1: %.2f" % quaternion[1] + ", q2: %.2f" % quaternion[2] + ", q3: %.2f " % quaternion[3]

            euler = packet.orientationEuler()
            s += " |Roll: %.2f" % euler.x() + ", Pitch: %.2f" % euler.y() + ", Yaw: %.2f " % euler.z()

        if packet.containsLatitudeLongitude():
            latlon = packet.latitudeLongitude()
            s += " |Lat: %7.2f" % latlon[0] + ", Lon: %7.2f " % latlon[1]

        if packet.containsAltitude():
            s += " |Alt: %7.2f " % packet.altitude()

        if packet.containsVelocity():
            vel = packet.velocity(xda.XDI_CoordSysEnu)
            s += " |E: %7.2f" % vel[0] + ", N: %7.2f" % vel[1] + ", U: %7.2f " % vel[2]

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
