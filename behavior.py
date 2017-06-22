from __future__ import division
import pickle
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as pl
import glob, os

sn.set_style('ticks')


orientation_sides = [[240, -1],[120, -1],[180, -1],[0, 1],[60, 1],[300, 1]]
pair_names = ['AB','CD','EF']

working_dir = '/Users/knapen/Downloads/'
# subject_number = 3

#####################################################################################################
#####
#####   Define Functions
#####
#####################################################################################################

def read_pickle_file(filename, selected_columns=['orientation_1', 'orientation_2', 'color_1', 'color_2', 'reward_probability_1',
                'reward_probability_2', 'HR_orientation', 'answer', 'correct', 'reward', 'feedback_if_HR_chosen']):
    with open(filename, 'rU') as f:
        op = pickle.load(f)
    return pd.DataFrame(op['parameterArray'])[selected_columns]

def df_from_pickles(filename_list, selected_columns=['orientation_1', 'orientation_2', 'color_1', 'color_2', 'reward_probability_1',
                'reward_probability_2', 'HR_orientation', 'answer', 'correct', 'reward', 'feedback_if_HR_chosen']):
    return pd.concat([read_pickle_file(f, selected_columns) for f in sorted(filename_list)])

#####################################################################################################
#####
#####   Across subjects
#####
#####################################################################################################


for subject_number in [1,3,6,12,15,19,20,22,27,31,33]:
    os.chdir(os.path.join(working_dir, 'subject %i'%subject_number))

    #####################################################################################################
    #####
    #####   Get Files and Set Variables
    #####
    #####################################################################################################


    training_files = sorted(glob.glob('*_0_*.pickle'))
    test_files = sorted(glob.glob('*_1_*.pickle'))

    train_wpa = df_from_pickles(training_files)
    test_wpa = df_from_pickles(test_files)

    #####################################################################################################
    #####
    #####   Train Phase
    #####
    #####################################################################################################



    # which side is each orientation
    for column in ['orientation_1', 'orientation_2']:
        # new column in df
        train_wpa[column+'_side'] = np.ones(len(train_wpa))
        for ori in orientation_sides:
            train_wpa[column+'_side'][train_wpa[column] == ori[0]] = ori[1]

    train_wpa['correct_color'] = (np.array(train_wpa['reward_probability_1'] > train_wpa['reward_probability_2']) * 2) -1
    train_wpa['correct_side'] = train_wpa['correct_color'] * train_wpa['orientation_1_side']
    train_wpa['correct_reconstructed'] = train_wpa['answer'] * train_wpa['correct_side']

    # which side is each orientation
    # new column in df
    train_wpa['pair'] = np.ones(len(train_wpa))
    for ps, name in zip([[.8,.2],[.7,.3],[.6,.4]], pair_names):
        indices = (train_wpa['reward_probability_1'] == ps[0]) + (train_wpa['reward_probability_1'] == ps[1])
        train_wpa['pair'][indices] = name

    corrects = []
    rewards = []
    feedback_if_HR_chosen = []
    crps = []
    for pair in pair_names:
        these_pair_trials = train_wpa[train_wpa['pair'] == pair]
        corrects.append(these_pair_trials['correct_reconstructed'])
        rewards.append(these_pair_trials['reward'])
        feedback_if_HR_chosen.append(these_pair_trials['feedback_if_HR_chosen'])
        crps.append(these_pair_trials[['color_1','color_2','reward_probability_1','reward_probability_2']].iloc[0])

    corrects = np.array(corrects)
    rewards = np.array(rewards)
    feedback_if_HR_chosen = np.array(feedback_if_HR_chosen)

    correct_trajectory = corrects.cumsum(axis = 1)
    reward_trajectory = rewards.cumsum(axis = 1)



    # f = pl.figure()
    # for x in range(3):
    #     pl.plot(np.arange(len(correct_trajectory[x])), correct_trajectory[x], label = pair_names[x], color = ['r','g','b'][x])
    #     pl.plot(np.arange(len(reward_trajectory[x])), reward_trajectory[x], ['r--','g--','b--'][x], label = pair_names[x])
    # pl.legend()
    # pl.savefig(os.path.join(working_dir, 'tc_%i.pdf'%subject_number))


    mean_correct = (np.array(corrects).mean(axis = 1) + 1) / 2
    mean_reward = np.array(rewards).mean(axis = 1)
    mean_feedback_if_HR_chosen = np.array(feedback_if_HR_chosen).mean(axis = 1)

    # print subject_number, mean_correct, mean_reward, mean_feedback_if_HR_chosen

    pairing_order = np.argsort(mean_feedback_if_HR_chosen)[::-1]

    color_RP_mapping_dict = {}
    for i, po in enumerate(pairing_order):
        for j, ci in enumerate(np.round(crps[po][['reward_probability_1','reward_probability_2']]).astype(int)+1):
            color_RP_mapping_dict.update({pair_names[i][1-j]: crps[po]['color_%i'%ci]})

    print color_RP_mapping_dict

    f = pl.figure()
    for x in range(3):
        pl.bar(left=[0,1,2][x], height=mean_correct[pairing_order[x]], width = 0.2, color = ['r','g','b'][x])
        pl.bar(left=[0.25, 1.25, 2.25][x], height=mean_reward[pairing_order[x]], width = 0.2, color = ['r','g','b'][x])
        pl.bar(left=[0.5, 1.5, 2.5][x], height=mean_feedback_if_HR_chosen[pairing_order[x]], width = 0.2, color = ['r','g','b'][x])
    sn.despine(offset=10)
    pl.gca().set_xticks([0.1,1.1,2.1,0.35,1.35,2.35,0.6,1.6,2.6])
    pl.gca().set_xticklabels(['AB_Corr','CD_Corr','EF_Corr','AB_R','CD_R','EF_R','AB_FB','CD_FB','EF_FB'], rotation='vertical')
    pl.gca().set_xlim([-0.25,3.0])
    pl.gca().set_ylim([0,1])
    pl.tight_layout()
    pl.savefig(os.path.join(working_dir, 'bars_tc', 'bar_%i.pdf'%subject_number))


# , label = pair_names[x]

    #####################################################################################################
    #####
    #####   Test Phase
    #####
    #####################################################################################################

    training_contingencies = np.vstack(
            (np.array([[np.unique(train_wpa['reward_probability_1'][train_wpa['color_1'] == c]).mean(), c]
                for c in np.unique(train_wpa['color_1'])]),
            np.array([[np.unique(train_wpa['reward_probability_2'][train_wpa['color_2'] == c]).mean(), c]
                for c in np.unique(train_wpa['color_2'])]))
    )

    # which rp for which color, taken from training set
    for column in ['color_1', 'color_2']:
        # new column in df
        test_wpa[column+'_rp'] = np.ones(len(test_wpa))
        for tc in training_contingencies:
            test_wpa[column+'_rp'][test_wpa[column] == tc[1]] = tc[0]

    # which side is each orientation
    for column in ['orientation_1', 'orientation_2']:
        # new column in df
        test_wpa[column+'_side'] = np.ones(len(test_wpa))
        for ori in orientation_sides:
            test_wpa[column+'_side'][test_wpa[column] == ori[0]] = ori[1]

    # re-work colors, rps and orientations to get to the correct answer.        
    test_wpa['correct_color'] = (np.array(test_wpa['color_1_rp'] > test_wpa['color_2_rp']) * 2) -1
    test_wpa['correct_side'] = test_wpa['correct_color'] * test_wpa['orientation_1_side']
    test_wpa['correct_reconstructed'] = test_wpa['answer'] * test_wpa['correct_side']

    easy_trials = np.abs(test_wpa['color_1_rp'] - test_wpa['color_2_rp']) > 0.5
    hard_trials = np.abs(test_wpa['color_1_rp'] - test_wpa['color_2_rp']) <= 0.2

    gain_trials = (test_wpa['color_1_rp'] + test_wpa['color_2_rp']) > 1.3
    loss_trials = (test_wpa['color_1_rp'] + test_wpa['color_2_rp']) < 0.7
