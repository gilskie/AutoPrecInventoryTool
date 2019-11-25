import configparser
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import tempfile, shutil
import re


def generate_list_from_list_box(list_box, dirs):
    for item in dirs:
        list_box.insert(END, item)


def generate_view(input_source_location, output_report_location, log_location, state_flags_json):
    window = tkinter.Tk()
    window.title("TPCPP17_AutoPrecInventoryTool")
    window.geometry("500x260")

    # generate list box to display folders available on directory!
    list_box_folders = tkinter.Listbox(window,
                                       selectmode=EXTENDED)
    root, dirs, files = os.walk(input_source_location).__next__()

    generate_list_from_list_box(list_box_folders,
                                dirs)

    list_box_folders.grid(row=0,
                          column=0,
                          ipadx=50,
                          ipady=1,
                          sticky=tkinter.W)

    # generate label view, wrap text no matter how long the text is!
    label_status_viewer = tkinter.Label(window,
                                        wraplength=250,
                                        text="Status: Waiting for file selection."
                                                     " Please use mouse scroll wheel to"
                                                     "reach on bottom part.")
    label_status_viewer.grid(row=0,
                             column=1,
                             sticky=tkinter.W)

    # generate button browse path!
    def browse_file():
        new_browse_file_location = filedialog.askdirectory(initialdir=input_source_location,
                                                           title="Select new source directory location:")
        root, new_dirs, files = os.walk(new_browse_file_location).__next__()
        list_box_folders.delete(0, END)
        generate_list_from_list_box(list_box_folders,
                                    new_dirs)

    button_browse_file = tkinter.Button(window,
                                        text="Browse Source Directory",
                                        fg="Blue",
                                        command=browse_file)

    button_browse_file.grid(row=1,
                            column=0,
                            sticky=tkinter.W)

    # generate button generating prec inventory report!
    def generate_prec_report():
        selected_items = list_box_folders.curselection()

        # display error if no file selected!
        if len(selected_items) == 0:
            messagebox.showerror(title="Error",
                                 message="No file selected!")
        else:
            for item in selected_items:
                folder_location = root + "\\" + list_box_folders.get(item)
                generate_bmp_excel_report(folder_location, output_report_location, log_location, state_flags_json)

    button_generate_prec_report = tkinter.Button(window,
                                                 text="Generate Prec Report",
                                                 fg="Black",
                                                 command=generate_prec_report)

    button_generate_prec_report.grid(row=2,
                                     column=0,
                                     sticky=tkinter.W)

    # must be always at last!
    window.mainloop()


def generate_bmp_excel_report(folder_location, output_report_location, log_location, state_flags_json):
    sgml_key_files = os.listdir(folder_location)
    # print(sgml_key_files)
    for sgml_key_file in sgml_key_files:
        file_location = folder_location + '\\' + sgml_key_file

        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, sgml_key_file)
        shutil.copy2(file_location, temp_path)

        # pre, ext = os.path.splitext(sgml_key_file)
        # temp_xml_file_extension = temp_dir + '\\' + pre + '.xml'

        # rename file from .key to .xml to feed on xml parser!
        # os.rename(temp_path , temp_xml_file_extension)

        bundle_number = date_created = ""

        if len(bundle_number) == 0 and len(date_created) == 0:
            root_folder_name = os.path.basename(folder_location)
            match_date = re.search(r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', root_folder_name)
            match_bundle_number = re.search(r'(\w[^_]+_[^_]+)_', root_folder_name)

            date_created = match_date.group()
            bundle_number = match_bundle_number.group()[:-1]

        print(f"{date_created}, {bundle_number}")

        # file_open = open(temp_path, "r")
        # lines = file_open.readline()
        # graphic_filename_bmp = link_text_content = carswell_cite = soc_value = ()
        # comments = ""

        # os.remove(temp_xml_file_extension)
        os.remove(temp_path)


def generate_pdf_excel_report():
    pass


def generate_sgm_excel_report():
    pass


def get_configuration_settings():
    config = configparser.ConfigParser()
    configuration_file = sys.path[0] + '\configurationFile.ini'

    config.read(configuration_file)

    default_setting = config["DEFAULT"]
    input_directory = default_setting["input_directory"]
    output_report = default_setting["output_report"]
    log_path = default_setting["log_path"]

    state_flag_setting = config["STATEFLAG"]
    state_flags = state_flag_setting["state_flags"]
    state_flags_json = json.loads(state_flags)

    return input_directory, output_report, log_path, state_flags_json


def main():
    try:
        input_source_location, output_report_location, log_location, state_flags_json = get_configuration_settings()
        generate_view(input_source_location, output_report_location, log_location, state_flags_json)

    except Exception as e:
        print(f"Error: {e}")


main()
