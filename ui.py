import dearpygui.dearpygui as dpg
import json
import os

os.chdir(os.path.dirname(__file__))

def run():
    
    with open("./config.json", 'r') as f:
        WINDOW_LENGTH = json.load(f)["length"]
        
    login()

    dpg.create_viewport(title='Interpreteur SQL', width=WINDOW_LENGTH[0], height=WINDOW_LENGTH[1])
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    
    w = dpg.get_viewport_client_width()
    h = dpg.get_viewport_client_height()
    
    with open("./config.json", "r") as f:
        ORIGINAL_JSON = json.load(f)
    
    ORIGINAL_JSON["length"] = [w, h]
    
    with open("./config.json", "w") as f:
        json.dump(ORIGINAL_JSON, f)
    
    
    dpg.destroy_context()


def login():
    dpg.create_context()

    with dpg.window(label="Tutorial"):
        b0 = dpg.add_button(label="button 0")
        b1 = dpg.add_button(tag=100, label="Button 1")
        dpg.add_button(tag="Btn2", label="Button 2")
    


run()