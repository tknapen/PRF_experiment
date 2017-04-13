from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
from numpy.random import random, shuffle
from math import *
import random, sys
from psychopy.tools.colorspacetools import hsv2rgb

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Trial import *
from constants import *
import ColorTools as ct

class RLTrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
        super(RLTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
        
        self.run_time = 0.0
        self.instruct_time = self.fixation_signal_time = self.wait_time = self.response_time = self.stimulus_time = self.fb_time = self.iti_time = 0.0

        
    def draw(self):
        """docstring for draw"""
        # only at feedback, do not draw the fixation mark.
        if not self.phase == 5:
            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            self.session.fixation.draw()

        # new sequence
        if self.phase == 0:
            if self.ID == 0:
                self.session.instruction.draw()
        elif self.phase == 2:
            self.session.fixation.setColor((-1,-1,-1))
        elif self.phase == 3:
            self.session.fixation.setColor((1,1,1))
            self.session.RL_stim_1.draw()
            if self.parameters['orientation_2'] >= 0:
                self.session.RL_stim_2.draw()
        elif self.phase == 5:
            if self.parameters['correct'] == -1:
                self.session.no_FB_stim.draw()
            elif self.session.train_test == 'train':
                if (self.parameters['correct'] == 1) & (self.parameters['feedback_if_HR_chosen'] == 1):
                    self.session.pos_FB_stim.draw()
                elif (self.parameters['correct'] == 1) & (self.parameters['feedback_if_HR_chosen'] == 0):
                    self.session.neg_FB_stim.draw()
                elif (self.parameters['correct'] == 0) & (self.parameters['feedback_if_HR_chosen'] == 1):
                    self.session.neg_FB_stim.draw()
                elif (self.parameters['correct'] == 0) & (self.parameters['feedback_if_HR_chosen'] == 0):
                    self.session.pos_FB_stim.draw()
            elif self.session.train_test == 'test':
                self.session.fixation_outer_rim.draw()
                self.session.fixation_rim.draw()
                self.session.fixation.draw()

        super(RLTrial, self).draw()

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape']:
                    self.events.append([-99,self.session.clock.getTime()-self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                # it handles both numeric and lettering modes 
                elif ev in ['space', ' ']:
                    self.events.append([0,self.session.clock.getTime()-self.start_time])
                    if self.phase == 0:
                        self.phase_forward()
                    else:
                        self.events.append([-99,self.session.clock.getTime()-self.start_time])
                        self.stopped = True
                        print 'trial canceled by user'
                elif ev == 't': # TR pulse
                    # self.events.append([99,self.session.clock.getTime()-self.start_time])
                    if self.phase == 0:
                        self.phase_forward()
                elif ev in self.session.response_button_signs.keys():
                    if self.phase == 3:
                        # then check whether one of the correct buttons was pressed:
                        if ev in self.session.response_button_signs.keys():
                            # do we even need an answer?
                            self.parameters['rt'] = self.session.clock.getTime() - self.fixation_signal_time
                            self.parameters['answer'] = self.session.response_button_signs[ev]
                            self.parameters['correct'] = int(self.parameters['HR_orientation'] == self.parameters['answer'])
                            if self.session.response_button_signs[ev] not in [self.parameters['orientation_1'], self.parameters['orientation_2']]:
                                self.parameters['correct'] = -1
                            # feedback bookkeeping
                            if self.session.train_test == 'train':
                                if (self.parameters['correct'] == 1) & (self.parameters['feedback_if_HR_chosen'] == 1):
                                    self.parameters['reward'] = 1
                                    self.parameters['reward_gained'] = standard_parameters['win_amount']
                                    self.parameters['reward_lost'] = 0.0
                                    self.session.reward_counter += standard_parameters['win_amount']
                                elif (self.parameters['correct'] == 1) & (self.parameters['feedback_if_HR_chosen'] == 0):
                                    self.parameters['reward'] = 0
                                    self.parameters['reward_gained'] = 0.0
                                    self.parameters['reward_lost'] = standard_parameters['loss_amount']
                                    self.session.loss_counter += standard_parameters['loss_amount']
                                elif (self.parameters['correct'] == 0) & (self.parameters['feedback_if_HR_chosen'] == 1):
                                    self.parameters['reward'] = 0
                                    self.parameters['reward_gained'] = 0.0
                                    self.parameters['reward_lost'] = standard_parameters['loss_amount']
                                    self.session.loss_counter += standard_parameters['loss_amount']
                                elif (self.parameters['correct'] == 0) & (self.parameters['feedback_if_HR_chosen'] == 0):
                                    self.parameters['reward'] = 1
                                    self.parameters['reward_gained'] = standard_parameters['win_amount']
                                    self.parameters['reward_lost'] = 0.0
                                    self.session.reward_counter += standard_parameters['win_amount']
                            #print self.parameters

                            # how much time remained in the response window?
                            response_time_remainder = self.phase_durations[3] - ( self.stimulus_time - self.fixation_signal_time )
                            self.phase_durations[6] += response_time_remainder

                            self.phase_forward()
                                                                                                                 
            super(RLTrial, self).key_event( ev )

    def run(self, ID = 0):
        self.ID = ID
        super(RLTrial, self).run()
        
        self.session.RL_stim_1.setOri(self.parameters['orientation_1'])
        self.session.RL_stim_2.setOri(self.parameters['orientation_2'])

        if (self.parameters['color_1'] + self.parameters['color_2']) > 0:

            color_a_1 = standard_parameters['stimulus_col_rad'] * np.cos(self.parameters['color_1'])
            color_b_1 = standard_parameters['stimulus_col_rad'] * np.sin(self.parameters['color_1'])
            color_1 = ct.lab2psycho((standard_parameters['stimulus_col_baselum'], color_a_1, color_b_1))
            self.session.RL_stim_1.setFillColor(color_1, 'rgb')

            color_a_2 = standard_parameters['stimulus_col_rad'] * np.cos(self.parameters['color_2'])
            color_b_2 = standard_parameters['stimulus_col_rad'] * np.sin(self.parameters['color_2'])
            color_2 = ct.lab2psycho((standard_parameters['stimulus_col_baselum'], color_a_2, color_b_2))
            self.session.RL_stim_2.setFillColor(color_2, 'rgb')      

        while not self.stopped:
            self.run_time = self.session.clock.getTime() - self.start_time
            # Only in trial 1, phase 0 represents the instruction period.
            # After the first trial, this phase is skipped immediately
            if self.phase == 0:
                self.instruct_time = self.session.clock.getTime()
                if self.ID != 0:
                    self.phase_forward()
            # In phase 1, we wait before the trial should start.
            if self.phase == 1:
                self.wait_time = self.session.clock.getTime()
                if ( self.wait_time - self.instruct_time ) > self.phase_durations[1]:
                    self.phase_forward()
            # In phase 2, we show the signal for the upcoming stimulus
            if self.phase == 2:
                self.fixation_signal_time = self.session.clock.getTime()
                if ( self.fixation_signal_time - self.wait_time ) > self.phase_durations[2]:
                        self.phase_forward()
            # In phase 3, the stimulus is presented
            if self.phase == 3:
                self.stimulus_time = self.session.clock.getTime()
                if ( self.stimulus_time - self.fixation_signal_time ) > self.phase_durations[3]:
                    self.phase_forward()
            # Phase 4 reflects the choice 
            if self.phase == 4:
                self.response_time = self.session.clock.getTime()
                if ( self.response_time - self.stimulus_time ) > self.phase_durations[4]:
                    self.phase_forward()
            # FB
            if self.phase == 5:
                self.fb_time = self.session.clock.getTime()
                if ( self.fb_time - self.response_time ) > self.phase_durations[5]:
                    self.phase_forward()
                    if self.parameters['correct'] == -1:
                        self.session.slow_counter += 1
            # ITI
            if self.phase == 6:
                self.iti_time = self.session.clock.getTime()
                if ( self.iti_time  - self.fb_time ) > self.phase_durations[6]:
                    self.stopped = True

            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
