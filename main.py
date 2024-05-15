import irsdk
import json
import pyautogui
import pyscreeze
from overlay import Overlay
import time

# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1


def _load_tracks_json():
    try:
        with open("tracks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except ValueError:
        return []
    
def _save_tracks_json(joined_tracks):
    with open("tracks.json", "w") as file:
        json.dump(joined_tracks, file)

def check_track_json(track_name): #checks if we have saved cars in this track
    joined_tracks = _load_tracks_json()
    for track in joined_tracks:
        if(next(iter(track)) == track_name):
            return True
    return False

def add_track_to_list(track_name, cars=[None]):
    joined_tracks = _load_tracks_json()
    if not check_track_json(track_name):
        new_track = {
            track_name: cars
        }
        joined_tracks.append(new_track)
        _save_tracks_json(joined_tracks)

def get_cars_json(track_name):
    if(check_track_json(track_name)): #if track exists lets find the cars
        joined_tracks = _load_tracks_json()
        for track in joined_tracks:
            if(next(iter(track)) == track_name):
                return track[track_name]
    return [None]
def add_cars_json(track_name, cars):
    if(check_track_json(track_name)): #if track exists lets find the cars
        joined_tracks = _load_tracks_json()
        for i in range(0, len(joined_tracks)):
            if(next(iter(joined_tracks[i])) == track_name):
                joined_tracks[i][track_name] = cars
                _save_tracks_json(joined_tracks)

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def track_stuff():
    track_name = ir['WeekendInfo']['TrackDisplayName']
    if not check_track_json(track_name): #if track has been added on before
        add_track_to_list(track_name)
    return track_name
        
    
def update_cars_callback(track_name, cars):
    add_cars_json(track_name, cars)

def change_car(filename):
    x, y = pyscreeze.locateCenterOnScreen('images/garage.jpg', confidence="0.6")
    pyautogui.click(x,y)
    time.sleep(0.25)
    x, y = pyscreeze.locateCenterOnScreen('images/my_setups.png', confidence="0.9")
    pyautogui.click(x,y)
    x, y = pyscreeze.locateCenterOnScreen('images/file_name.png', confidence="0.9")
    pyautogui.click(x,y)
    pyautogui.write(f'{filename.split("/")[-1]}\n')
    x, y = pyscreeze.locateCenterOnScreen('images/exit.png', confidence="0.9")
    pyautogui.click(x,y)


def main_loop():
    if not ir['IsOnTrack']: #if player not in game
        overlay.alpha(1)
    else:
        overlay.alpha(0)
    

if __name__ == '__main__':
    # initializing ir and state
    
    pyautogui.PAUSE = 0.2
    ir = irsdk.IRSDK()
    ir.startup()
    state = State()

    track_name = track_stuff()
    overlay = Overlay(track_name, cars=get_cars_json(track_name), update_cars_callback=update_cars_callback, call_change_car_callback=change_car, main_loop_callback=main_loop)
    overlay.render()
    

