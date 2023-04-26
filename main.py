from pydub import AudioSegment
import PySimpleGUI as sg
from pathlib import Path
import os

sg.theme('DarkAmber')

work_path = Path.cwd()

song_info = 'Файл не выбран'

layout = [
    [sg.Button('Выбрать файл', key='-OPEN-', size=(20), pad=(0,5))],
    [sg.Text(text = song_info, key='-FILEINFO-')],
    [sg.Text('Total song time'),sg.Text(text='0:00', key='-TOTALTIME-')],
    [sg.HSeparator(pad=(0,10))],
    [sg.Text('Start time', key='-FILESTARTINFO-')],
    [sg.Text(text='Min', size=(9)), sg.Text(text='Sec')],
    [sg.Input(key='-STARTLENGTHMIN-', size=(10, 20), default_text='0'), sg.Input(key='-STARTLENGTHSEC-', size=(10,20), default_text='0')],
    [sg.HSeparator(pad=(0,15))],
    [sg.Text('End time', key='-FILEENDINFO-')],
    [sg.Text(text='Min', size=(9)), sg.Text(text='Sec')],
    [sg.Input(key='-ENDLENGTHMIN-', size=(10, 20), default_text='0'), sg.Input(key='-ENDLENGTHSEC-', size=(10,20), default_text='0')],
    [sg.HSeparator(pad=(0,20))],
    [sg.Button('Обрезать и сохранить', key='-SAVE-', size=(20))]
]


window = sg.Window('Song editor', layout, finalize = True, size=(450,400))
window.bind('<Key-Escape>', 'Esc')

def cut_update(Min, Sec):
    time = Min*60*1000+Sec*1000
    return time

def extraction(song, song_info):
    extract = song[cut_update(int(values['-STARTLENGTHMIN-']), int(values['-STARTLENGTHSEC-'])): \
                       cut_update(int(values['-ENDLENGTHMIN-']),int(values['-ENDLENGTHSEC-']))]
    song_info = ' '.join([f for f in song_info.split('.') if 'mp3' not in f])
    print(song_info)
    extracted = extract.export(f'{song_info}_cutted.mp3', format="mp3", bitrate='320k')
    return extracted


while True:
    event, values = window.read(timeout=50)

    if event == sg.WIN_CLOSED or event == 'Esc':
        break

    if event == '-OPEN-':
        song_name = sg.popup_get_file('Open', no_window=True)
        song_path = (Path(work_path, song_name))
        song = AudioSegment.from_mp3(song_path)
        song_info = song_path.name
        window['-FILEINFO-'].update(song_info)
        window['-TOTALTIME-'].update(f'{int(len(song)//60000)}:{int(int(len(song)%60000)/1000)}')
        window['-ENDLENGTHMIN-'].update(f'{int(len(song)//60000)}')
        window['-ENDLENGTHSEC-'].update(f'{int(int(len(song)%60000)/1000)}')

    if event == '-SAVE-':
        if int(values['-ENDLENGTHSEC-']) > 60:
            window['-ENDLENGTHSEC-'].update(str(int(int(len(song)%60000)/1000)))
        if int(values['-ENDLENGTHMIN-']) > int(len(song)//60000) or int(values['-ENDLENGTHMIN-']) <= 0:
            window['-ENDLENGTHMIN-'].update(str(int(len(song)//60000)))
        #file_path = sg.popup_get_file('Save', no_window = True, save_as = True, default_extension = 'mp3')
        extraction(song, song_info)
        dir_list = os.listdir(work_path)
        cutted_song_info = f"{' '.join([f for f in song_info.split('.') if 'mp3' not in f])}_cutted.mp3"
        try:
            if cutted_song_info in set(dir_list):
                sg.popup('Готово', modal=False)
            else:
                sg.popup('Ошибка обработки', modal=False)
        except:
            sg.popup('Ошибка обработки', modal=False)


window.close()
