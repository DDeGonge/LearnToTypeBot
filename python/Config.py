import numpy as np

""" PI PINOUTS """
SHOCK_PIN = 4                           # OUTPUT
LED_PINS = [15, 27]                       # OUTPUT
SENSE_PINS = [26, 20, 13, 6, 5, 16, 12, 23]   # INPUT


""" OPERATION PARAMETERS """
saveimg_path = '/home/pi/imgs'

window_update_hz = 25
window_size_s = 4
led_strobe_hz = 10


""" CAMERA PARAMETERS """
video_resolution = (1920, 1080)


""" NEURAL NET PARAMETERS...RIP"""
train_path = 'assets/training.csv'
test_path  = 'assets/testing.csv'
model_path = 'assets/NeuralModel.h5'
in_len = 8 # int(window_update_hz * window_size_s)
out_len = 1
net_layers = [3]    # Guess? idfk
net_epochs = 2000    # Larger is more accurate?
net_learnrate = 0.01

active_thresh = 0.7
pecking_thresh = 0.1


""" IM SMAHTER THAN NEURAL NET PARAMETERS """
changes_thresh = 5
idle_sum_thresh = None
peck_sum_thresh = 0.6
score_inc_up = 0.005
score_inc_dn = 0.03


""" TIME TRIAL PARAMETERS """
thresh_times = np.linspace(0, 1000, 101)
thresh_increment = 5
wpm_window_s = 20


""" PUNISHMENTS """
zaptime_s = 5
strobe_warn_on_s = 1
strobe_warn_off_s = 4


""" AUDIO STUFF """
audio_path = 'assets'
audio_catagories = {
    'tea': 'tea',
    'chop': 'chop',
    'thud': 'thud',
    'safen': 'safen',
    'safes': 'safes',
    'score': 'score',
    'oops': 'oops',
    'thank': 'thank'
}  # I know this dict is useless now but eh it's fine, 'futureproofing' ya?
freq = 44100
bitsize = -16
channels = 2
buffer = 2048
volume = 0.95


""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_FRAMES = True
