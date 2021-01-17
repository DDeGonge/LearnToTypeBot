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

""" MY PRECIOUS... """
ree_positionz = [
    [0,   225, 340],
    [3,   225, 285],
    [3.2, 225, 290],
    [3.4, 230, 285],
    [3.6, 225, 290],
    [3.8, 230, 285],
    [4.0, 235, 280],
    [4.2, 230, 285],
    [4.4, 225, 280],
    [4.6, 220, 295],
    [4.8, 215, 290],
    [5.0, 220, 285],
    [5.0, 225, 290],
    [5.2, 220, 285],
    [5.4, 215, 280],
    [5.6, 220, 285],
    [5.8, 225, 290],
    [6.0, 230, 290],
    [6.1, -50, 200],
    [8.0, 500, 100],
    [8.1, 300, -40],
    [10.0, 100, 350],
    [10.1, 500, 0],
    [12.0, 300, 350],
    [12.1, -50, 0],
    [14.0, 500, 50],
    [14.1, 500, 250],
    [16.0, 300, -50],
    [16.1, -50, 250],
    [18.0, 500, -50],
    [18.1, 200, -50],
    [20.0, 300, 350],
    [20.1, -50, 200],
    [22.0, 500, 100],
    [22.1, 300, -40],
    [24.0, 100, 350],
    [24.1, 500, 0],
    [26.0, 300, 350],
    [26.1, -50, 0],
    [28.0, 500, 50],
    [28.1, 500, 250],
    [30.0, 300, -50],
    [30.1, -50, 250],
    [32.0, 500, -50],
    [32.1, 200, -50],
    [34.0, 300, 350],
    [34.1, 500, 250],
    [36.0, 300, -50],
    [36.1, -50, 250],
    [38.0, 500, -50],
    [38.1, 200, -50],
    [40.0, 300, 350],
    [40.1, -50, 200],
    [42.0, 500, 100],
    [42.1, 300, -40],
    [44.0, 100, 350],
    [44.1, 500, 0],
    [46.0, 300, 350],
    [46.1, -50, 0],
    [48.0, 500, 50],
    [48.1, 500, 250],
    [50.0, 300, -50],
    [50.1, -50, 250],
    [52.0, 500, -50],
    [52.1, 200, -50],
    [54.0, 300, 350]
]


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
volume = 0.10


""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_FRAMES = True
