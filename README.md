# RL_experiment
experimental software for RL experiment, using psychopy as a backend and pygaze for the eyetracking.

# HOWTO

```bash
python run_RL_exp.py
>>> Your subject_nr:
>>> Run number: [-1=mapper, 0=training, 1=test]
>>> Are you in the scanner (y/n)?: 
>>> Are you recording gaze (y/n)?: 
```

Use a number between 1 and 48 as a subject number. These define the mappings between rewards and stimuli. Runs are now created to be short, with both training and test to be run 4 times in a row. You can keep the run number the same for each time the experiment is run, as the datetime will be appended to the filenames.

# To Do:

- Fix Test phase trial distribution
- Balance L/R Test phase pairing balance
-