""" PI PINOUTS """
SHOCK_PIN = 4                           # OUTPUT
LED_PINS = [15, 27]                       # OUTPUT
SENSE_PINS = [26, 20, 13, 6, 5, 16, 12, 23]   # INPUT


""" OPERATION PARAMETERS """
saveimg_path = '/home/pi/imgs'

window_update_hz = 10
window_size_s = 5
led_strobe_hz = 10


""" CAMERA PARAMETERS """
video_resolution = (1920, 1080)


""" NEURAL NET PARAMETERS...RIP"""
train_path = 'assets/training.csv'
test_path  = 'assets/testing.csv'
model_path = 'assets/NeuralModel.h5'
in_len = 50
out_len = 2
net_layers = [4, 2]    # Guess? idfk
net_epochs = 1000    # Larger is more accurate?
net_learnrate = 0.01

active_thresh = 0.7
pecking_thresh = 0.5


""" IM SMAHTER THAN NEURAL NET PARAMETERS """
changes_thresh = 7
idle_sum_thresh = 50
peck_sum_thresh = 65
score_inc = 0.01


""" TIME TRIAL PARAMETERS """
thresh_times = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 10]
thresh_increment = 5


""" CHOPPING PARAMETERS """
crust_thickness_mm = 8
fine_slice_mm = 1
coarse_slice_mm = 3
dice_spacing_mm = 5


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
