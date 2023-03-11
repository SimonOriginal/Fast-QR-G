import PySimpleGUI as sg
import webbrowser
import qrcode as qr
from PIL import Image, ImageTk
import glob


def qrmaker(code):
    qr_img = qr.make(str(code))
    qr_img.save('temp.png',format="png")

    return qr_img

def parse_folder(path):
    images = glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.png')
    return images

def load_image(path, window):
    try:
        image = Image.open(path)
        image.thumbnail((400, 400))
        photo_img = ImageTk.PhotoImage(image)
        window["-qr_img-"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")

    

def make_win1():
    
    sg.theme('LightGreen6')
    
    menu_def = [['Настройки',['О программе']]]
    menu = [[sg.Menu(menu_def, key='-MENU-', text_color='black', background_color='white')]]
    element_user = [[sg.Text('Введите текст:', font=("Helvetica", 14))],
                [sg.Multiline(size=(60, 4), key='-qr_data-')],
                [sg.Submit('Генерировать', font=("Helvetica", 12), size=(14, 1))],
                [sg.Text('Сохранить имя:', font=("Helvetica", 12), size=(12, 1)), sg.Input(key='-qr_name-')],
                [sg.Button('Сохранить', size=(14, 1), font=("Helvetica", 12)),
                 sg.Button('Очистить', size=(16, 1), font=("Helvetica", 12), button_color=('black', 'orange'))],
                 [sg.Text('Расположение файла:',font=("Helvetica", 12))],
                 [sg.Input(enable_events=True, key="file"),
                 sg.FolderBrowse('Папка',size=(11, 1),font=("Helvetica", 12))],
                [sg.Button("Предыдущий", size=(14, 1), font=("Helvetica", 12)),
                 sg.Button("Следующий",size=(14, 1), font=("Helvetica", 12))]]

    element_viewer = [[sg.Image(key='-qr_img-')]]
    
    layout = [[sg.Column(menu),
           sg.Column(element_user),
           sg.VSeperator(),
           sg.Column(element_viewer)]]
    
    return sg.Window('Fast QR-G', layout, location=(500,200), finalize=True)



def make_win2():
    sg.theme('Reddit')
    font=("Arial", 12)
    
    layout = [[sg.Text("Программа створена Безрученко Семеном,",font=font)],
              [sg.Text("cтудентом 481 групи.",font=font)],
              [sg.Text("Для курсового проекуту за темою:",font=font)],
              [sg.Text("Автоматичне формування QR-кодів.",font=font)],
              [sg.Button('Мой GitHub', size=(14, 1), key=('GitHub'),font=("Arial", 11),button_color=('black', 'yellow'))]]

    return sg.Window('О программе', layout,  finalize=True)

window1, window2 = make_win1(), None        
images = []
location = 0



while True:             
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED:
        window.close()
        
        if window == window2:       
            window2 = None
        elif window == window1:     
            break

    elif event == 'О программе' and not window2:
        window2 = make_win2()
        
    elif event in 'Генерировать':
        print('QR code Text: {}'.format(values['-qr_data-']))
        qr_img = qrmaker(values['-qr_data-'])
        window['-qr_img-'].update('temp.png')

    elif event in 'Сохранить':
        save_qr_name = '{}.png'.format(values['-qr_name-'])
        qr_img = qrmaker(values['-qr_data-'])
        qr_img.save(save_qr_name)

    if event == 'file':
        images = parse_folder(values["file"])
        if images:
            load_image(images[0], window)
    if event == 'Следующий' and images:
        if location == len(images) - 1:
            location = 0
        else:
            location += 1
        load_image(images[location], window)
    if event == "Предыдущий" and images:
        if location == 0:
            location = len(images) - 1
        else:
            location -= 1
        load_image(images[location], window)

    if event == 'Очистить':
        window['-qr_data-'].update('')
        window['-qr_name-'].update('')
        window['-qr_img-'].update('')
    if event == 'GitHub':
         webbrowser.open_new_tab('https://github.com/SimonW0rk/Fast-QR-G.git')
        
window.close()
