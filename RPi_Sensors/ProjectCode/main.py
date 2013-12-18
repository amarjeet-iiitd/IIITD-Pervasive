# Main File
# Author: Rishav Jain
#
# Initializes profile and logger, and start task according to the Mode
#

# Import variables from other project files
from store import StoreTask
from sample import SampleTask
from profile import profile
import logger

# initialize the profile and logger
profile.profileInit()
logger.logInit()

# log the profile parameters
profile.printProfile()

# enter into user defined Mode
if profile.Mode == 1:
	logger.log('info', 'Real-Time Sample/Post Mode')
	SampleTask()

elif profile.Mode == 2:
	logger.log('info', 'Store & Upload Mode')
	StoreTask()
