import sys, datetime
# from Tkinter import *

sys.path.append( 'exp_tools' )

from RLSession import *
# from plot_staircases import *
try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

def main():
    subject_nr = raw_input('Your subject_nr: ')
    run_nr = int(raw_input('Run number: [-1=mapper, 0=training, 1=test]'))
    scanner = raw_input('Are you in the scanner (y/n)?: ')
    track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False

    ts = RLSession( subject_nr, run_nr, scanner, tracker_on )
    ts.run()

if __name__ == '__main__':
    main()
