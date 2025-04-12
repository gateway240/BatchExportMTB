import os
import random
import string
from pathlib import Path

# Output settings
sensor_ids = ["SYNTH-ABCD", "SYNTH-EFGH", "SYNTH-IJKL", "SYNTH-MNOP"]

results_dir = os.path.expanduser('~/data/test-data')
delimiter = "\t"

# Define the fields
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

# Generate a random 3x3 rotation matrix
def random_rotation_matrix():
    return [[random.uniform(-1, 1) for _ in range(3)] for _ in range(3)]

def generate_device_id(existing_ids):
    while True:
        rand_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        full_id = f"SYNTHETIC-{rand_id}"
        if full_id not in existing_ids:
            return full_id

# Generate synthetic data for one sensor
def export_fake_sensor_data(trial_name, device_id, packet_count=100):
    header_info = [
        [' General information', ''],
        ['Update Rate', "100Hz"],
        ['MT Manager version', 'synthetic'],
        ['XDA version', 'mocked'],
        [' Device information', ''],
        ['DeviceId', device_id],
        ['ProductCode', 'MTWSYNTH'],
        ['Firmware Version', '0.0.1'],
        ['Hardware Version', '1.0'],
        [' Device settings', ''],
        ['Filter Profile', 'SyntheticTest'],
        ['Option Flags', 'None']
    ]

    s = ''
    for i in range(packet_count):
        acc = [random.uniform(-2, 2) for _ in range(3)]
        gyr = [random.uniform(-250, 250) for _ in range(3)]
        mag = [random.uniform(-50, 50) for _ in range(3)]
        quat = [random.uniform(-1, 1) for _ in range(4)]
        roll, pitch, yaw = [random.uniform(-180, 180) for _ in range(3)]
        matrix = random_rotation_matrix()

        mat_vals = [
            matrix[0][0], matrix[1][0], matrix[2][0],
            matrix[0][1], matrix[1][1], matrix[2][1],
            matrix[0][2], matrix[1][2], matrix[2][2]
        ]

        row_parts = [
            f"{i:05d}",
            f"{acc[0]:.15f}", f"{acc[1]:.15f}", f"{acc[2]:.15f}",
            f"{gyr[0]:.15f}", f"{gyr[1]:.15f}", f"{gyr[2]:.15f}",
            f"{mag[0]:.15f}", f"{mag[1]:.15f}", f"{mag[2]:.15f}",
            f"{quat[0]:.15f}", f"{quat[1]:.15f}", f"{quat[2]:.15f}", f"{quat[3]:.15f}",
            f"{roll:.15f}", f"{pitch:.15f}", f"{yaw:.15f}"
        ] + [f"{val:.15f}" for val in mat_vals]
        row = delimiter.join(row_parts)
        s += row + "\n"

    # Output file name
    filename = f"{trial_name}-{device_id}.txt"
    file_path = os.path.join(results_dir, filename)

    try:
        os.makedirs(results_dir, exist_ok=True)
    except Exception as e:
        print(f"❌ Failed to create directory: {e}")
        return

    with open(file_path, "w") as f:
        header = ''
        for item in header_info:
            header += f"// {item[0]}: {item[1]}\n" if item[1] else f"// {item[0]}\n"
        f.write(header)
        f.write(data_header + "\n")
        f.write(s)

    print(f"✅ Exported: {file_path}")

# Main function to generate multiple sensors for the same trial
def export_multiple_sensors(trial_name="testdata", packet_count=100):
    for device_id in sensor_ids:
        export_fake_sensor_data(trial_name, device_id, packet_count)

if __name__ == '__main__':
    export_multiple_sensors(trial_name="synthetic_trial01", packet_count=120)
