# A Simple Photo Organizer
This photo organizer python script works by extracting timestamp information from photo file metadata and creating a folder structure representing the time when the photo was taken.  It first tries to use the Python Imaging Library (PIL) to find the date and time when the photo was taken and falls back to using the date modified on the file if that does not work.

Since this is a quick and dirty script the path to scan and the path to which to output the organized files are hardcoded at the bottom of the script.  To run, make sure you have a recent version of python 3 installed and then run the following command (tested on a Mac).

`python3 PhotoOrganizer.py`

If you need to install PIL (imported by the script) this command may help.  It actually installs a newer maintained fork of the PIL project.

`python3 -m pip install Pillow`

Happy organizing!
