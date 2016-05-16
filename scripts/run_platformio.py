import subprocess
import dialog
import os

TOP_BOARDS = ['uno', 'diecimilaatmega328', 'megaatmega2560', 'nanoatmega328',
              'leonardo']

SOURCE_DIR = "firmware/respirometro"

shexec = lambda command:\
    subprocess.check_output(command, shell=True).decode('ascii')

def get_plataformio_serial_ports():
    '''

    '''
    serial_raw = shexec("platformio serialports list").splitlines()
    serial_ports = [serial_raw[i-1] 
            for i,x in enumerate(serial_raw) if '----' in x]
    
    return [(x,x) for x in serial_ports]


def get_platformio_atmelavr_boards(top_boards=[]):
    ''' Executes platformio board list command and parse results to a
        nice and clean Python list of tuples.
    '''
    boards_lines = shexec("platformio boards atmelavr").splitlines()[5:]

    boards, top_names = [], {}
    for b in boards_lines:
        cols = [x.strip() for x in b.split('  ') if x.strip() != '']
        if cols[0] in top_boards:
            top_names[cols[0]] = cols[-1]
        else:
            boards.append((cols[0], cols[-1]))

    return [(x, top_names[x]) for x in TOP_BOARDS] + boards


def exec_dialog_select(description, choices):
    ''' Launch a dialog with a list of boards for the user to choose.
        Return the platformio board name selected.
    '''

    d = dialog.Dialog(dialog="dialog")
    code, tag = d.menu(description, choices=choices,
                       no_cancel=True, no_ok=True, no_tags=True)
    return tag

def exec_dialog_select_serial_port():
    ''' Launch a dialog with a list of boards for the user to choose.
        Return the platformio board name selected.
    '''
    return exec_dialog_select(
            description = "Select your serialport:", 
            choices = get_plataformio_serial_ports())


def exec_dialog_select_board():
    ''' Launch a dialog with a list of boards for the user to choose.
        Return the platformio board name selected.
    '''
    return exec_dialog_select(
            description = "Select your board:", 
            choices = get_platformio_atmelavr_boards(top_boards=TOP_BOARDS))


def platformio_setup(source_dir, build_dir='.build'):
    board_name = exec_dialog_select_board()
    serial_port = exec_dialog_select_serial_port()
    os.system("""
        rm -rf {build_dir} &&
        mkdir -p {build_dir} &&
        cd {build_dir} &&
        yes | platformio init --board {board_name} &&
        cp -r ../{source_dir}/* src/. &&
        platformio run -t upload --upload-port {serial_port}
        """.format(**locals()).strip())


platformio_setup(source_dir=SOURCE_DIR)

