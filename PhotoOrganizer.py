from math import floor
import shutil
import sys, os
from time import strftime, localtime
from PIL import Image
import datetime as dt
import re

class clPhotoOrganizer(object):

    def __init__(self, aSourcePath, aDestPath, aTestMode=False):
        # Check that the source path exists and is a directory.
        if os.path.isdir(aSourcePath):
            self._srcPath = aSourcePath
        else:
            raise IsADirectoryError('Path is not a directory: {}'.format(aSourcePath))

        self._dstPath = aDestPath
        self._testMode = aTestMode

    def run(self):
        '''
        Organize the photos by time modified.
        '''

        # Get a list of ALL files.  We want to organize everything, regardless of file extension since folks in the
        # future might change the file extensions for photos and videos.

        lFilenames = []
        for lRoot, lDirs, lFiles in os.walk(self._srcPath):
            for lFile in lFiles:
                if not lFile.endswith(('.DS_Store')):
                    lFilenames.append(os.path.join(lRoot, lFile))

        # Organize the files.
        lCurrentFile = 0
        lTotalFiles = len(lFilenames)

        for lFilename in lFilenames:
            lCurrentFile += 1

            # Get the time modified.
            lFolder = self._dstPath
            try:
                lRawTimeTaken = self.get_date_taken(lFilename)
                dt_taken = dt.datetime.strptime(lRawTimeTaken, "%Y:%m:%d %H:%M:%S")

                lYear = dt_taken.strftime('%Y')
                lMonth = dt_taken.strftime('%B')
                lDayAbbrev = dt_taken.strftime("%a")
                lDayOfMonthNum = dt_taken.strftime('%d')
            except Exception as e:
                print('Falling back to using date modified for file {} due to error {}.'.format(lFilename, e))

                # Fall back to using the date modified and log a warning
                lTimeModified = localtime(os.path.getmtime(lFilename))
                lYear = strftime('%Y', lTimeModified)
                lMonth = strftime('%B', lTimeModified)
                lDayAbbrev = strftime('%a', lTimeModified)
                lDayOfMonthNum = strftime('%d', lTimeModified)

                lFolder = os.path.join(lFolder, 'ByDateModified')

            lFolder = os.path.join(lFolder, lYear)
            lFolder = os.path.join(lFolder, lMonth)
            lBasename = os.path.basename(lFilename)

            # Remove any portion of the beginning of the picture filename that looks like a previously added day number and string, like '02 Sat_'
            lNewBaseName = re.sub('^[0-9]{2}[ -][A-Z]{1}[a-z]{2}[_]', '', lBasename)

            # Prepend the day of the week and the day of the month to the filename.
            lNewFilenamePrefix = '{} {}_'.format(lDayOfMonthNum, lDayAbbrev)
            lNewFilename = '{}{}'.format(lNewFilenamePrefix, lNewBaseName)
            lFinalPath = os.path.join(lFolder, lNewFilename)

            # Print the current status.
            lSizeInBytes = os.path.getsize(lFilename)
            lReadableSize = None
            if lSizeInBytes < 1024:
                lReadableSize = '{}B'.format(lSizeInBytes)
            elif lSizeInBytes < pow(1024, 2):
                lReadableSize = '{:0.3f}KB'.format(lSizeInBytes / 1024)
            elif lSizeInBytes < pow(1024, 3):
                lReadableSize = '{:0.3f}MB'.format(lSizeInBytes / pow(1024, 2))
            else:
                lReadableSize = '{:0.3f}GB'.format(lSizeInBytes / pow(1024, 3))

            print('{:>3}% {} of {} ({}) {} => {}'.format(
                floor(lCurrentFile / lTotalFiles * 100),
                lCurrentFile,
                lTotalFiles,
                lReadableSize,
                lBasename,
                lFinalPath
            ))

            # If the destination path does not exist, create it.
            # if not os.path.isdir(self._dstPath):
            os.makedirs(os.path.dirname(lFinalPath), exist_ok=True)

            # Copy over the new file.
            if not self._testMode:
                try:
                    shutil.copy(lFilename, lFinalPath)
                except Exception as e:
                    print('Error! Caught exception [{}] while copying [{}] to [{}].'.format(e, lFilename, lFinalPath))

    # See https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
    @staticmethod
    def get_date_taken(path):
        try :
            return Image.open(path)._getexif()[36867]
        except Exception as e:
            raise Exception("Could not get date taken from image: " + path)


if __name__ == '__main__':
    lSrc = r'/Users/adam/Pictures/todo'
    lDst = r'/Users/adam/Pictures/Managed2'
    lPhotoOrganizer = clPhotoOrganizer(lSrc, lDst, False)
    sys.exit(lPhotoOrganizer.run())