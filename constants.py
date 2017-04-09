
from __future__ import division

# standard parameters
standard_parameters = {
    
    'practice':                                 0,
    'nr_slow_warning':                          6,

    'ratio_empty_trials':                       0.3,
    'empty_trial_duration':                     4.0,
    'initial_grace_period':                     12.,        # rest before and after experiment (fMRI) 
    'final_grace_period':                       20.,        # rest before and after experiment (fMRI) 

    'nr_stim_repetitions_per_run_train':        2,         # number of repetitions per run, of the 30-trial sequences that fully define the probabilities.
    'nr_stim_repetitions_per_run_test':         5,         # number of repetitions per run, of the 15-trial sequences that fully define the probabilities.
    'nr_stim_repetitions_per_run_mapper':       2,        # number of repetitions per run, of the 6x6-trial sequences that fully define the probabilities.
    
    ## spatial dimensions:
    'eyelink_calib_size':                       0.5,       # portion of screen heigth    
    'x_offset':                                 0.0,
    'y_offset':                                 0.0,

    'vertical_stim_size':                       100.0,
    'horizontal_stim_size':                     2000.0,
    'stim_fix_distance':                        20.0,

    # stimulus variables:
    'feedback_height':                          35,
    'win_amount':                               0.1,
    'loss_amount':                              0,

    # timing variables:
    'response_feedback_exp_mean':               0.5,
    'fix_alert_exp_mean':                       0.125,

    'TR':                                       0.945,                 

} 

standard_phase_durations = [-0.000001, -0.000001, 0.5, 3.0, 0.5, 1.0, 0.0]

#response_button_signs = {
#       's':240,
#       'd':180,
#       'f':120,
#       'j':60,
#       'k':0,
#       'l':300
#        }

response_button_signs = {
        'r':240,
        'f':180,
        'v':120,
        'n':60,
        'j':0,
        'i':300
        }

# screen_res = (1920,1080)
# background_color = (0.5,0.5,0.5)#-0.75,-0.75,-0.75)

full_screen = True
FGC = (0,0,0)
BGC = (255*0.5,255*0.5,255*0.5) # this is converted to -1<->1 in SPSession

# K2D-38 (all in cm):
#DISPSIZE = (1024,768)
#SCREENSIZE = (39.0,29.0)
#SCREENDIST = 60.0
#7T scan room (all in cm):
#DISPSIZE = (1024,768)
DISPSIZE = (2560,1440)#(2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)#(2560,1440)
SCREENSIZE = (69.84,39.29) #physical screen size in centimeters
SCREENDIST = 225#60.0#65.0#57.0 # centimeters; distance between screen and participant's eyes
#office screen
# DISPSIZE = (2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)
# SCREENSIZE = (59.83,33.72)# physical screen size in centimeters
# SCREENDIST = 75# centimeters; distance between screen and participant's eyes


