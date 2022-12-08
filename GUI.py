import tkinter.ttk as ttk
from tkinter import *
import os
from datetime import *
from dateutil.relativedelta import relativedelta
from tkinter import filedialog as fd, Tk,\
    Label, Button, TOP, Entry, Checkbutton, BooleanVar
from pathlib import Path

from Tatyana_Prod.calculator import Calculator, \
                    OilPredictionMethod, \
                    FluidPredictionMethod, \
                    WCPredictionMethod
from graph import bring_output


def Choose_file_upload(event):
    global DATA_DIR
    global data_file
    file_name = fd.askopenfile(defaultextension='.xlsx', title='Choose .xlsx file')
    data_file = file_name.name
    path = os.path.dirname(os.path.abspath(data_file))
    DATA_DIR = Path(path)
    return


def Choose_file_count(event):
    if '.xlsx' in data_file:
        START_DATE = get_data_start() + relativedelta(months=-1)
        END_DATE = get_data_end()
        CUT_DATE = get_data_cut()

        oil_prediction = get_oil_method()
        liq_prediction = get_liq_method()
        wc_prediction = get_wc_method()

        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("300x50")
        label1 = Label(text='Расчет в процессе...', justify='right')
        label1.pack(side=TOP)
        root.update()

        calc = Calculator.load(
            data_base_prod=DATA_DIR,
            data_mer=DATA_DIR,
            input_date=START_DATE,
            end_date=END_DATE,
        )

        logs = calc.run(
                  oil_method=oil_prediction,
                  fluid_method=liq_prediction,
                  watercut_method=wc_prediction,
                  start_date=START_DATE,
                  cut_date=CUT_DATE,
                  account_condensate=False,
                  mean_use_coef=True,
                  binding_to_mean=get_bind(),
             )

        label1.destroy()

        bring_output(root, logs, oil_prediction, START_DATE)
        #root.quit()
        #root.winfo_children().widget.destroy()



def get_data_start():
    try:
        date_obj = entry_date_start.get()
        date_start = datetime.strptime(date_obj, "%d %m %Y")
    except:
        date_start = datetime.strptime('01 01 2022', "%d %m %Y")
    return date_start


def get_data_end():
    try:
        date_obj = entry_date_end.get()
        date_end = datetime.strptime(date_obj, "%d %m %Y")
    except:
        date_end = datetime.strptime('01 12 2022', "%d %m %Y")
    return date_end


def get_data_cut():
    try:
        date_obj = entry_date_cut.get()
        date_cut = datetime.strptime(date_obj, "%d %m %Y")
    except:
        date_cut = datetime.strptime('01 01 2019', "%d %m %Y")
    return date_cut


def get_oil_method():
    selection_oil = menu_oil.get()
    if selection_oil == oil_var[0]:
        selection = OilPredictionMethod.WC
    else:
        selection = OilPredictionMethod.ARPS
    return selection


def get_liq_method():
    selection_liq = menu_liq.get()
    if selection_liq == liq_var[0]:
        selection = FluidPredictionMethod.ARPS
    elif selection_liq == liq_var[1]:
        selection = FluidPredictionMethod.EXP
    else:
        selection = FluidPredictionMethod.BL
    return selection


def get_wc_method():
    if wc_depend.get() == 0:
        selection = WCPredictionMethod.COREY
    else:
        selection = WCPredictionMethod.COMB
    return selection


def get_bind():
    if bind_to_last.get() == 0:
        return True
    else:
        return False



root = Tk()
root.title('Прототип поскважинного прогнозирования')
root.resizable(width=False, height=False)  # Нельзя развернуть окно
root.geometry("550x550")


#кнопка загруки
button = Button(root, text="Загрузить файл")
button.bind('<Button-1>', Choose_file_upload)
button.place(x=230, y=20)

#верхняя подпись
label_data = Label(text='Введите дату начала и конца прогноза',  justify='right')
label_data.place(x=80, y=60)

label_oil = Label(text='Выберите способ расчёта модели нефти', justify='right')
label_oil.place(x=80, y=210)

label_liq = Label(text='Выберите способ расчёта модели жидкости', justify='right')
label_liq.place(x=80, y=270)

label_data_start = Label(text='Первый месяц прогноза: ', justify='right')
label_data_start.place(x=80, y=100)

label_data_end = Label(text='Последний месяц прогноза: ', justify='right')
label_data_end.place(x=80, y=130)

label_data_cut = Label(text='Месяц обрезки прогноза: ', justify='right')
label_data_cut.place(x=80, y=160)


#окошко ввода
entry_date_start = Entry(width=35)
entry_date_start.insert(0, "01 01 2022")
#entry_date_start.configure(state='disabled')
entry_date_start.place(x=250, y=100)

entry_date_end = Entry(width=35)
entry_date_end.insert(0, "01 12 2022")
#entry_date_end.configure(state='disabled')
entry_date_end.place(x=250, y=130)

entry_date_cut = Entry(width=35)
entry_date_cut.insert(0, "01 12 2019")
#entry_date_end.configure(state='disabled')
entry_date_cut.place(x=250, y=160)

#список
oil_var = ['Расчёт через ХВ и жидкость', 'Арпс']
default_oil = StringVar(value=oil_var[0])
menu_oil = ttk.Combobox(textvariable=default_oil, values=oil_var, width=60)
menu_oil.place(x=80, y=240)

liq_var = ['Арпс', 'Экспоненциальный выход на полку', 'Баклей-Леверетт']
default_liq = StringVar(value=liq_var[0])
menu_liq = ttk.Combobox(textvariable=default_liq, values=liq_var, width=60)
menu_liq.place(x=80, y=300)


#чекбокс
bind_to_last = BooleanVar()
bind_to_last.set(0)
check_bind = Checkbutton(root, text="Привязка к последнему месяцу факта", variable=bind_to_last, onvalue=1, offvalue=0)
check_bind.place(x=80, y=350)

wc_depend = BooleanVar()
wc_depend.set(0)
check_wc = Checkbutton(root, text="ХВ зависит от обводнённости", variable=wc_depend, onvalue=1, offvalue=0)
check_wc.place(x=80, y=380)

gtm_ = BooleanVar()
gtm_.set(0)
check_gtm = Checkbutton(root, text="Включить фильтр ГТМ", variable=gtm_, onvalue=1, offvalue=0)
check_gtm.place(x=80, y=410)

#кнопка расчёта
button_01 = Button(root, text="Рассчитать")
button_01.bind('<Button-1>', Choose_file_count)
button_01.place(x=230, y=440)





root.mainloop()