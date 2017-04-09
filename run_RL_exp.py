import sys, datetime
# from Tkinter import *

sys.path.append( 'exp_tools' )

from RLSessionLocation import *
from RLSessionColor import *

try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

def main():
    experiment = '1' # raw_input('The Experiment you wish to run: [0: Location, 1: Color] ')
    subject_nr = '10' # raw_input('Your subject_nr: ')
    run_nr = 1 # int(raw_input('Run number: [-2=buttontraining pupil, -1=mapper (fMRI only), 0=training (fMRI & pupil), 1=test (fMRI & pupil)] '))
    scanner = 'n' # raw_input('Are you in the scanner (y/n)?: ')
    track_eyes = 'n' # raw_input('Are you recording gaze (y/n)?: ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False

    if experiment == '0':
        ts = RLSessionLocation( subject_nr, run_nr, scanner, tracker_on )
    elif experiment == '1':
        ts = RLSessionColor( subject_nr, run_nr, scanner, tracker_on )
    ts.run()

if __name__ == '__main__':
    main()
