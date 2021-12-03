window_width = 800
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = 1

def calculate_scale_factor(max_distance):
    global scale_factor
    scale_factor = 0.5*min(window_height, window_width)/max_distance
    print('Scale factor:', scale_factor)

def scale_x(x):
    return int(x*scale_factor) + 0*window_width//2

def scale_y(y):
    return int(y*scale_factor) + 0*window_height//2
