from __future__ import division
from psychopy import visual, core, misc, event, data
import numpy as np
import itertools
from IPython import embed as shell
from math import *
import time as time_module

import os, sys, time, pickle
import pygame
from pygame.locals import *

sys.path.append( 'exp_tools' )

from Session import *
from Staircase import ThreeUpOneDownStaircase
from RLTrial import *
from RLSession import *
from constants import *
import ColorTools as ct

try: 
	import appnope
	appnope.nope()
except: 
	print 'APPNOPE NOT ACTIVE!'
	
class RLSessionColor(RLSession):
    def __init__(self, subject_number, index_number, scanner, tracker_on):
        super(RLSessionColor, self).__init__( subject_number, index_number, scanner, tracker_on, experiment_name = 'color' )

    def create_training_trials(self):
        """docstring for prepare_trials(self):"""

        # ranges
        # amount_of_colors = range(6) 
        # self.hues = (np.linspace(0,1,len(amount_of_colors), endpoint=False)).reshape(2,3).T
        self.reward_probs = np.array([[0.80,0.20], [0.70,0.30], [0.60,0.40]])       #reward probability sets  

        self.positions_for_subject_number()
        #correct responses 
        AB_correct = np.array(np.r_[np.ones(8), np.zeros(2)]) #80:20 chance to get positive feedback 
        CD_correct = np.array(np.r_[np.ones(7), np.zeros(3)]) #70:30 chance to get positive feedback 
        EF_correct = np.array(np.r_[np.ones(6), np.zeros(4)]) #60:40 chance to get positive feedback  
        for responses in ([AB_correct, CD_correct, EF_correct]): 
            np.random.shuffle(responses)
        feedback = np.vstack([np.array([AB_correct, CD_correct, EF_correct]).T for i in range(standard_parameters['nr_stim_repetitions_per_run_train'])]) #3x10xi array of feedback after correct response 


        self.standard_parameters = standard_parameters              

        # create trials
        self.trials = []

        self.trial_counter = 0
        for i in range(feedback.shape[1]):                  #3 stimulus pair feedback sets                   
            for j in range(feedback.shape[0]):  			#10 x nr_stim_repetitions_per_run_train'             
                params = self.standard_parameters
                # randomize phase durations a bit
                trial_phase_durations = np.copy(np.array(standard_phase_durations))
                trial_phase_durations[2] += np.random.exponential(self.standard_parameters['fix_alert_exp_mean'])                
                trial_phase_durations[4] += np.random.exponential(self.standard_parameters['response_feedback_exp_mean'])
                trial_phase_durations[6] += np.random.exponential(self.standard_parameters['iti_exp_mean'])

                feedback_if_HR_chosen = feedback[j, i]

                reward_probability_1 = self.reward_probs[self.probs_to_stims_this_subject[i][0], int((self.probs_to_stims_this_subject[i][1]+1)/2)]
                reward_probability_2 = self.reward_probs[self.probs_to_stims_this_subject[i][0], int((-self.probs_to_stims_this_subject[i][1]+1)/2)]


                this_orientation = np.random.randint(0,6)
                orientation_1 = self.stim_orientations[this_orientation]
                orientation_2 = (self.stim_orientations[this_orientation] + 180)%360

                # old CIElab code
                #color_1 = (np.pi/180.0) * self.colour_orientations[self.probs_to_stims_this_subject[i][0]] #use other orientations than stim_orientations
                #color_2 = (np.pi/180.0) * self.colour_orientations[(self.probs_to_stims_this_subject[i][0]+3)%6] # fmod(color_1 + np.pi, 2*np.pi)

                color_1 = colour_orientations[self.probs_to_stims_this_subject[i][0]] #use other orientations than stim_orientations
                color_1_lum = colour_luminances[self.probs_to_stims_this_subject[i][0]] 			
								
                color_2 = colour_orientations[(self.probs_to_stims_this_subject[i][0]+3)%6] # fmod(color_1 + np.pi, 2*np.pi)
                color_2_lum = colour_luminances[(self.probs_to_stims_this_subject[i][0]+3)%6]           

                print ('color 1:', color_1)
                print ('color 2:', color_2)

                #define high reward orientation
                if reward_probability_1 > reward_probability_2:
                    if orientation_1 in (240,180,120):
                        HR_orientation = -1
                    else:
                        HR_orientation = 1
                else:
                    if orientation_1 in (240,180,120):
                        HR_orientation = 1
                    else:
                        HR_orientation = -1

                params.update(
                        {   
                        'color_1': color_1, 
                        'color_2': color_2,
                        'color_1_lum': color_1_lum,
						'color_2_lum': color_2_lum,
                        'reward_probability_1': reward_probability_1, 
                        'reward_probability_2': reward_probability_2,
                        'orientation_1': orientation_1,
                        'orientation_2': orientation_2,
                        'HR_orientation': HR_orientation,
                        'feedback_if_HR_chosen': feedback_if_HR_chosen,
                        'eye_movement_error': 0,
                        'answer': 0,
                        'correct': -1,
                        'reward': 0,
                        'reward_gained': 0,
                        'reward_lost': 0,
                        'rt': 0,
                        }
                    )

                self.trials.append(RLTrial(parameters = params, phase_durations = np.array(trial_phase_durations), session = self, screen = self.screen, tracker = self.tracker))
                self.trial_counter += 1

        self.shuffle_trials()

        this_instruction_string = """Two colours will appear simultaneously on the computer screen. \nOne colour will be rewarded more often and the other will be rewarded less often, \nBUT at first you won't know which is which! \nThere is no ABSOLUTE right answer, \nbut some colours will have a higher chance of giving you reward. \nTry to pick the colour that you find to have the highest chance of giving reward! \nCorrect choices will be rewarded with 0.10 points, incorrect responses receive no points.\n\nPress the spacebar to start"""
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 100), italic = True, height = 15, alignHoriz = 'center', wrapWidth = 1200)


    def create_test_trials(self):   
        # ranges
        # amount_of_colors = range(6) 
        # self.hues = (np.linspace(0,1,len(amount_of_colors), endpoint=False)).reshape(2,3).T
        self.reward_probs = np.array([[0.80,0.20], [0.70,0.30], [0.60,0.40]])  #reward probability sets  

        self.positions_for_subject_number()

        combinations = list(itertools.combinations(range(6),2))

        self.standard_parameters = standard_parameters              

        # create trials
        self.trials = []

        self.trial_counter = 0
        for i in range(len(combinations)):       
            for j in range(standard_parameters['nr_stim_repetitions_per_run_test']):              #100 feedback outcomes --> iterate 100 values within the feedback arrays 
                params = self.standard_parameters
                # randomize phase durations a bit
                trial_phase_durations = np.copy(np.array(standard_phase_durations))

                # trial_phase_durations[6] += np.random.randn()*1.0 #SD 0.1 geeft relatief stabiel feedback interval rond 3 seconde

                feedback_if_HR_chosen = 0

                reward_probability_1 = self.reward_probs[self.probs_to_stims_this_subject[combinations[i][0]%3][0],int((self.probs_to_stims_this_subject[combinations[i][0]%3][1]+1)/2)]
                reward_probability_2 = self.reward_probs[self.probs_to_stims_this_subject[combinations[i][1]%3][0],int((self.probs_to_stims_this_subject[combinations[i][1]%3][1]+1)/2)]

                this_orientation = np.random.randint(0,6)
                orientation_1 = self.stim_orientations[this_orientation]
                orientation_2 = (self.stim_orientations[this_orientation] + 180)%360

                color_1 = colour_orientations[combinations[i][0]] #use other orientations than self.stim_orientations
                color_2 = colour_orientations[combinations[i][1]] #use other orientations than self.stim_orientations

                color_1_lum = colour_luminances[combinations[i][0]]             
                color_2_lum = colour_luminances[combinations[i][1]]             


                if reward_probability_1 > reward_probability_2:
                    if orientation_1 in (240,180,120):
                        HR_orientation = -1
                    else:
                        HR_orientation = 1
                else:
                    if orientation_1 in (240,180,120):
                        HR_orientation = 1
                    else:
                        HR_orientation = -1

                params.update(
                        {   
                        'color_1': color_1, 
                        'color_2': color_2, 
                        'color_1_lum': color_1_lum,
                        'color_2_lum': color_2_lum,
                        'reward_probability_1': reward_probability_1, 
                        'reward_probability_2': reward_probability_2,
                        'orientation_1': orientation_1,
                        'orientation_2': orientation_2,
                        'HR_orientation': HR_orientation,
                        'feedback_if_HR_chosen': feedback_if_HR_chosen,
                        'eye_movement_error': 0,
                        'answer': 0,
                        'correct': -1,
                        'reward': 0,
                        'reward_gained': 0,
                        'reward_lost': 0,
                        'rt': 0,
                        }
                    )

                self.trials.append(RLTrial(parameters = params, phase_durations = np.array(trial_phase_durations), session = self, screen = self.screen, tracker = self.tracker))
                self.trial_counter += 1

        self.shuffle_trials()

        this_instruction_string = """It's time  to test what you've learned!\n During this set of trials you will NOT receive feedback (or rewards) to your responses. \nDuring this phase you will see new combinations of colours. \nPlease choose the colour that 'feels' more correct based on the training. \nIf you are not sure which one to pick, just go with your gut instinct! \n\nPress the spacebar to start..."""
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 100), italic = True, height = 15, alignHoriz = 'center', wrapWidth = 1200)


    def create_mapper_trials(self):   

        self.standard_parameters = standard_parameters              

        # create trials
        self.trials = []

        self.trial_counter = 0
        for i in range(len(self.stim_orientations)): 		#6 orientations     
            for j in range(len(self.stim_orientations)):    #6 colors 
                for k in range(standard_parameters['nr_stim_repetitions_per_run_colour_mapper']):              
                    params = self.standard_parameters
                    # randomize phase durations NOT!
                    trial_phase_durations = np.copy(np.array(standard_phase_durations))
                    trial_phase_durations[4] = 1.5                      
                    trial_phase_durations[5] = 0.75                       
                    trial_phase_durations[6] = 0.75 # np.random.randn()*1.0 #SD 0.1 geeft relatief stabiel feedback interval rond 3 seconde

                    feedback_if_HR_chosen = 1
                    orientation_1 = self.stim_orientations[i]
                    orientation_2 = -1
                    HR_orientation = orientation_1

                    color_1 = colour_orientations[j]    #use other colours than self.stim_orientations
                    color_1_lum = colour_luminances[j]

                    params.update(
                            {   
                            'color_1': color_1, 
                            'color_2': 0, 
                            'color_1_lum': color_1_lum,
                            'color_2_lum': 0,
                            'reward_probability_1': 0, 
                            'reward_probability_2': 0,
                            'orientation_1': orientation_1,
                            'orientation_2': orientation_2,
                            'HR_orientation': HR_orientation,
                            'feedback_if_HR_chosen': feedback_if_HR_chosen,
                            'eye_movement_error': 0,
                            'answer': 0,
                            'correct': -1,
                            'reward': 0,
                            'reward_gained': 0,
                            'reward_lost': 0,
                            'rt': 0,
                            }
                        )

                    self.trials.append(RLTrial(parameters = params, phase_durations = np.array(trial_phase_durations), session = self, screen = self.screen, tracker = self.tracker))
                    self.trial_counter += 1

        self.shuffle_trials()
  
        # this_instruction_string = """Respond as quickly as possible by pushing the correct button for the appearing stimulus."""
        this_instruction_string = """"""
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 100), italic = True, height = 15, alignHoriz = 'center', wrapWidth = 1200)

    

