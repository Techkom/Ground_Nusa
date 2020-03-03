import subprocess

# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
python_bin = "/home/pi/Documents/Ground_Nusa/GN-Raspberry/bin/python3"

# Path to the script that must run under the virtualenv
#script_file = "/home/pi/Documents/Ground_Nusa/PiCameraToOpenCV.py"
script_file = "/home/pi/Documents/Ground_Nusa/GUI.py"

subprocess.Popen(['LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0',python_bin, script_file])
