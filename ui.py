import dearpygui.dearpygui as dpg
import json
import os
from interpreter import sqldb

os.chdir(os.path.dirname(__file__))


CONN_NUMBER = 0

def print_error(error_txt):
    dpg.set_value("my_super_error_displaying", error_txt)
    dpg.configure_item("my_super_button_id", show=True)
            


def login_button_callback(sender, appdata, text_input):
    global CONN_NUMBER
    
    path = dpg.get_value(text_input[0])
    create_file = dpg.get_value(text_input[1])
    
    # faire un test si le fichier existe
    basedir = os.path.dirname(path).replace("./", f"{os.getcwd()}/")
    filename = os.path.basename(path)
    
    try:
        ls = os.listdir(basedir)
        if (filename in ls and not create_file) or (not filename in ls and create_file):
            conn = sqldb(path)
            
            if conn.connection != None:
                gen_connection(conn, CONN_NUMBER)
                CONN_NUMBER += 1
            else:
                print_error("Erreur pendant l'ouverture de la db")
        else:
            print_error("Mauvais nom de fichier")
    except FileNotFoundError:
        print_error("Mauvais chemin d'accès")


def login():
    dpg.create_context()

    with dpg.window(label="Connection a la db", width=200, height=100):
        input1 = dpg.add_input_text(label="DB path", default_value="")
        chk_box = dpg.add_checkbox(label="Créer un fichier", default_value=False)
        login_button = dpg.add_button(label="Connection", callback=login_button_callback, user_data=(input1, chk_box))
      
      # popup widow in case of error  
    with dpg.popup(login_button, modal=True, tag="my_super_button_id"):
        dpg.add_text("", tag="my_super_error_displaying")
        dpg.add_button(label="Close", callback=lambda: dpg.configure_item("my_super_button_id", show=False))



def gen_connection(conn, n):
    
    with dpg.window(label=f"Connection {n}", width=200, height=400, pos=[200, 0]):
        pass


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


    


run()