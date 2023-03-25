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
                gen_connection(conn, CONN_NUMBER, filename)
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
        dpg.add_button(label="Fermer", callback=lambda: dpg.configure_item("my_super_button_id", show=False))


def check_callback(sender, appdata):
    state = dpg.get_value(sender)
    dpg.configure_item("f_output", show=state)
    dpg.configure_item("check_output", show=state)
        


def gen_connection(conn, n, filename):

    with dpg.window(label=f"Connection {n} ({filename})", width=350, height=400, pos=[350*n+200, 0]):
        # executer depuis un fichier
        dpg.add_text("Executer depuis un fichier :")
        f_input = dpg.add_input_text()
        dpg.add_button(label="Executer")
        
        # saut de ligne
        dpg.add_text()
        
        # executer depuis l'input
        dpg.add_text("Executer depuis l'entrée :")
        querry_input = dpg.add_input_text(multiline=True)
        dpg.add_button(label="Executer")
        
        dpg.add_text()
        
        dpg.add_checkbox(label="Afficher la sortie", default_value=True)
        dpg.add_checkbox(label="Enregistrer la sortie dans un fichier", default_value=False, callback=check_callback)
        f_output = dpg.add_input_text(tag="f_output")
        dpg.add_checkbox(label="créer le fichier de sortie si il n'existe pas", default_value=True, tag="check_output")
        dpg.configure_item("f_output", show=False)
        dpg.configure_item("check_output", show=False)


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