import tkinter as tk
import irsdk
import time
import json
import pyautogui
import pyscreeze
from overlay import Overlay

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
    return track_name in joined_tracks

def add_track_to_list(track_name):
    joined_tracks = _load_tracks_json()
    if track_name not in joined_tracks:
        joined_tracks.append(track_name)
        _save_tracks_json(joined_tracks)

# def get_cars()

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
    if(check_track_json(track_name)): #if track has been added on before
        return (track_name, ['get_cars'])
    else: #if track doesnt exist in json
        add_track_to_list(track_name)
    

def loop():


    # retrieve CarSetup from session data
    # we also check if CarSetup data has been updated
    # with ir.get_session_info_update_by_key(key)
    # but first you need to request data, before checking if its updated
    car_setup = ir['CarSetup']
    if car_setup:
        car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
        if car_setup_tick != state.last_car_setup_tick:
            state.last_car_setup_tick = car_setup_tick
            print('car setup update count:', car_setup['UpdateCount'])
            # now you can go to garage, and do some changes with your setup
            # this line will be printed, only when you change something
            # and press apply button, but not every 1 sec
    

def change_car(filename):
    x, y = pyscreeze.locateCenterOnScreen('images/garage.jpg', confidence="0.6")
    pyautogui.click(x,y)
    x, y = pyscreeze.locateCenterOnScreen('images/my_setups.png', confidence="0.9")
    pyautogui.click(x,y)
    x, y = pyscreeze.locateCenterOnScreen('images/file_name.png', confidence="0.9")
    pyautogui.click(x,y)
    pyautogui.write(f'{filename}\n')
    x, y = pyscreeze.locateCenterOnScreen('images/exit.png', confidence="0.9")
    pyautogui.click(x,y)

if __name__ == '__main__':
    # initializing ir and state
    
    pyautogui.PAUSE = 0.2
    ir = irsdk.IRSDK()
    state = State()
    ir.freeze_var_buffer_latest()

    track_stuff()
    #Overlay(track_name, ['none'])

    change_car('baseline.sto')

    # try:
    #     # infinite loop
    #     while True:
    #         # check if we are connected to iracing
    #         check_iracing()
    #         # if we are, then process data
    #         if state.ir_connected:
    #             pass
                
    #         # sleep for 1 second
    #         # maximum you can use is 1/60
    #         # cause iracing updates data with 60 fps
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     # press ctrl+c to exit
    #     pass