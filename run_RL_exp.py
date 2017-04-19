import sys, datetime

sys.path.append( 'exp_tools' )

from RLSessionLocation import *
from RLSessionColor import *

try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

def main():
    subject_nr = raw_input('Your subject_nr: ')
    run_nr = int(raw_input('Run number: [-1=mapper (fMRI only), 0=training (fMRI & pupil), 1=test (fMRI & pupil)] '))
    scanner = 'n' # raw_input('Are you in the scanner (y/n)?: ')
    track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False

    ts = RLSessionColor( subject_nr, run_nr, scanner, tracker_on )
    ts.run()

if __name__ == '__main__':
    main()
