from __future__ import division
from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Trial import *

class RLTrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
        super(RLTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
        
        self.stim = PRFStim(self.screen, self, self.session, orientation = self.parameters['orientation'])
        
        this_instruction_string = """Two colours will appear simultaneously on the computer screen. \n
                                    One colour will be rewarded more often and the other will be rewarded less often, \n
                                    BUT at first you won't know which is which! \nThere is no ABSOLUTE right answer, \n
                                    but some colours will have a higher chance of giving you reward. \n
                                    Try to pick the colour that you find to have the highest chance of giving reward!"""
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
        self.instruction.setSize((1200,50))

        self.run_time = 0.0
        self.instruct_time = self.t_time = self.response_time = self.stimulus_time = self.fb_time = self.iti_time = 0.0

        
    def draw(self):
        """docstring for draw"""
            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            self.session.fixation.draw()
        if self.phase == 0:
            if self.ID == 0:
                self.instruction.draw()
        elif self.phase == 2:
            self.session.RL_stim_1.draw()
            self.session.RL_stim_2.draw()
        elif self.phase == 4 and self.session.train_test == 'train':
            if sign(self.parameters['answer']) == 0:
                self.session.no_FB_stim.draw()
            elif (self.parameters['answer'] * self.parameters['feedback_if_1_chosen']) < 0:
                self.session.pos_FB_stim.draw()
            elif (self.parameters['answer'] * self.parameters['feedback_if_1_chosen']) > 0:
                self.session.neg_FB_stim.draw()

        super(RLTrial, self).draw( )

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape']:
                    self.events.append([-99,self.session.clock.getTime()-self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                # it handles both numeric and lettering modes 
                elif ev == ' ':
                    self.events.append([0,self.session.clock.getTime()-self.start_time])
                    if self.phase == 0:
                        self.phase_forward()
                    else:
                        self.events.append([-99,self.session.clock.getTime()-self.start_time])
                        self.stopped = True
                        print 'trial canceled by user'
                elif ev == 't': # TR pulse
                    self.events.append([99,self.session.clock.getTime()-self.start_time])
                    if self.phase==1:
                        self.phase_forward()
                elif ev in self.session.response_button_signs.keys():
                    if self.phase in (2, 3):
                        # then check whether one of the correct buttons was pressed:
                        if ev in self.session.response_button_signs.keys():
                            # do we even need an answer?
                            self.parameters['answer'] = self.session.response_button_signs[ev]

                            self.events.append( log_msg )
                            print log_msg
                            if self.session.tracker:
                                self.session.tracker.log( log_msg )

                            # feedback bookkeeping
                            if (self.parameters['answer'] * self.parameters['feedback_if_1_chosen']) < 0:
                                self.parameters['reward'] = 1
                                self.parameters['reward_gained'] = WIN_AMOUNT
                                self.parameters['reward_lost'] = 0.0
                                self.session.reward_counter += WIN_AMOUNT
                            elif (self.parameters['answer'] * self.parameters['feedback_if_1_chosen']) > 0:
                                self.parameters['reward'] = 0
                                self.parameters['reward_gained'] = 0.0
                                self.parameters['reward_lost'] = -LOSS_AMOUNT
                                self.session.loss_counter += LOSS_AMOUNT

                event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                self.events.append(event_msg)
        
            super(RLTrial, self).key_event( ev )

    def run(self, ID = 0):
        self.ID = ID
        super(RLTrial, self).run()
        
        self.session.RL_stim_1.setOri(self.parameters['orientation'])
        self.session.RL_stim_2.setOri(self.parameters['orientation']+180.0)

        while not self.stopped:
            self.run_time = self.session.clock.getTime() - self.start_time
            # Only in trial 1, phase 0 represents the instruction period.
            # After the first trial, this phase is skipped immediately
            if self.phase == 0:
                self.instruct_time = self.session.clock.getTime()
                if self.ID != 0:
                    self.phase_forward()
            # In phase 1, we wait for the scanner pulse (t)
            if self.phase == 1:
                self.t_time = self.session.clock.getTime()
                if self.session.scanner == 'n' && self.ID == 0:
                    self.phase_forward()
                else:
                    if ( self.t_time - self.instruct_time ) > self.phase_durations[1]:
                        self.phase_forward()
            # In phase 2, the stimulus is presented
            if self.phase == 2:
                self.stimulus_time = self.session.clock.getTime()
                if ( self.stimulus_time - self.t_time ) > self.phase_durations[2]:
                    self.phase_forward()
            # Phase 3 reflects the choice 
            if self.phase == 3:
               self.response_time = self.session.clock.getTime()
                if ( self.response_time - self.stimulus_time ) > self.phase_durations[3]:
                    self.phase_forward()
            # FB
            if self.phase == 4:
                self.fb_time = self.session.clock.getTime()
                if ( self.fb_time - self.response_time ) > self.phase_durations[4]:
                    self.phase_forward()
            # ITI
            if self.phase == 5:
                self.iti_time = self.session.clock.getTime()
                if ( self.iti_time  - self.fb_time ) > self.phase_durations[5]:
                    self.stopped = True

            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
