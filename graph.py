import numpy as np
from tkinter import *
import matplotlib
from matplotlib.figure import Figure
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Tatyana_Prod.arps_function import CombinedArps


def get_start_date(data, dob_neft):
    dataline = dob_neft.columns.to_numpy()
    month = np.where(dataline==data)[0][0]
    data_fact = dataline[np.where(dataline < data)]
    month_fact_delta = (data_fact[-1].year - data_fact[1].year) * 12 + data_fact[-1].month - data_fact[1].month
    #fm = month - month_fact_delta
    return month, month_fact_delta


def bring_output(root, logs, oil_prediction, START_DATE, ):
    label2 = Label(text='Выберите скважину из списка:', justify='center')
    wells = logs[6]

    # Создание виджета - список скважин
    root.update()
    s1 = Scrollbar(root)
    menu_wells = Listbox(listvariable=wells, width='55', height='10', yscrollcommand=s1.set, exportselection=0)

    s1.config(command=menu_wells.yview)
    for i in wells:
        # Поиск скв из поля ввода
        menu_wells.insert('end', str(i))
        search_entry = Entry(width=27)

        def search(event, obj1=menu_wells):
            new_symbol = search_entry.get()
            obj1.delete(0, obj1.size() - 1)  # Удаление существующего виджета - списка объектов
            if new_symbol == "":
                names_objects = wells
                for element in names_objects:
                    obj1.insert('end', str(element))
            else:
                new_names = []
                for element in wells:
                    if str(new_symbol) in str(element):
                        new_names.append(element)
                for element in new_names:
                    obj1.insert('end', str(element))

        search_entry.bind("<KeyRelease>", lambda event, obj1=menu_wells: search(obj1))

    root.geometry("1200x650")
    matplotlib.use('TkAgg')
    frame = Frame(root)
    fig = Figure(figsize=(8, 7), dpi=100)
    #fig.subplots_adjust(wspace=0, hspace=0.5)

    menu_wells.bind('<<ListboxSelect>>',
                    lambda event, menu_wells=menu_wells, frame=frame:
                    show_graph(menu_wells, fig, frame, root, logs, oil_prediction, START_DATE))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=1, column=5, columnspan=5, rowspan=20, sticky=W)
    menu_wells.grid(row=3, column=3, columnspan=2)
    label2.grid(row=2, column=3, sticky=E)
    search_entry.grid(row=2, column=4, sticky=W)

    canvas.draw()


def show_graph(menu_wells, fig,  frame, root, dd, oil_prediction, START_DATE):
    fig.clear()
    root.update()

    oil_data = dd[0]
    liq_data = dd[1]
    wc_data = dd[2]
    vrem_dob = dd[3]
    irr = dd[4]
    const = dd[5]
    #wells = dd[5]

    well = oil_data.index.tolist()[list(menu_wells.curselection())[0]]

    # Исxодные данные для визуалзации
    dob_neft = oil_data.loc[oil_data.index == well]
    #first_month, _ = get_start_date(START_DATE, dob_neft)
    dob_neft = np.squeeze(dob_neft.to_numpy())[1:]

    dob_liq = liq_data.loc[liq_data.index == well]
    dob_liq = np.squeeze(dob_liq.to_numpy())[1:]

    vrem_dob = vrem_dob.loc[vrem_dob.index == well]
    #vrem_dob = vrem_dob.loc[vrem_dob.loc[well, :] > 0]
    vrem_dob = np.squeeze(vrem_dob.to_numpy())

    dob_neft = dob_neft[np.where(dob_neft > 0)]
    dob_liq = dob_liq[np.where(dob_liq > 0)]
    vrem_dob = vrem_dob[np.where(vrem_dob > 0)]
    first_month = np.size(vrem_dob)-1

    niz = irr.loc[well, 'NIZ']

    fact_neft = dob_neft[:np.size(vrem_dob)]
    fact_liq = dob_liq[:np.size(vrem_dob)]
    Wc_fact = (fact_liq - fact_neft) / fact_liq
    Wc_fact[Wc_fact == -np.inf] = 0
    Wc_fact[Wc_fact == np.inf] = 0

    Q_nak = np.cumsum(fact_neft*(vrem_dob/24))/ 1000
    RF_fact = Q_nak/ niz
    #RF_last = RF_fact[first_month-1]
    RF_fact = RF_fact[np.where(Wc_fact > 0)]
    Wc_fact = Wc_fact[np.where(Wc_fact > 0)]

    t_1 = np.arange(0, 1, 0.01)
    Co, Cw, mef = const.loc[well,'CoreyO'], const.loc[well,'CoreyW'], const.loc[well,'Mu']
    b1, b2, D1, tau = const.loc[well, 'b1'], const.loc[well, 'b2'], const.loc[well, 'd1'], const.loc[well, 'tau']
    arps_coeffs = [b1, b2, D1, tau]
    qst = const.loc[well, 'qst']
    ke = const.loc[well, 'ke']
    Wc_model = mef * t_1 ** Cw / ((1 - t_1) ** Co + mef * t_1 ** Cw)

    #REDO
    ct_fact = np.cumsum(vrem_dob) /(24 * 30.45)
    ct_fact = np.insert(ct_fact, 0, 0, axis=0)
    ct_pred = np.zeros(120 - np.size(ct_fact))
    #ct_pred = np.zeros(120)
    ct_pred[:] = ke
    #ct = np.cumsum(ct_pred)
    ct_pred = np.cumsum(ct_pred)[:] + ct_fact[-1]
    ct = np.concatenate((ct_fact, ct_pred))

    t = np.arange(0, 119, 1)

    if oil_prediction == 'arps':
        Oil_model_f = []
        Liq_model_f = []
        Wc = []
        rf_1 = RF_fact[0]
        for i in range(len(ct) - 1):
            Oil_model_f.append(qst *CombinedArps.calc_integral(ct[i], ct[i + 1], *arps_coeffs)/(ct[i+1] - ct[i]))
        #Oil_model_f = qst * np.array(Oil_model_f) / ke
        #Oil_model_f = np.insert(Oil_model_f, 0, 0)

        for i in range(120):
            rf_1 = rf_1 + Oil_model_f[i] * 30.5 / niz / 1000
            if rf_1 >= 1: rf_1 = 0.99999999999
            Wc.append(mef * rf_1 ** Cw / ((1 - rf_1) ** Co + mef * rf_1 ** Cw))
            Liq_model_f.append(Oil_model_f[i] / (1 - Wc[-1]))
    else:
        Liq_model_f = []
        Oil_model_f = []
        Wc = []
        oil1 = [0]
        rf = RF_fact[0]

        for i in range(len(ct) - 1):
            Liq_model_f.append(qst * CombinedArps.calc_integral(ct[i], ct[i+1], *arps_coeffs) / (ct[i+1] - ct[i]))

        oil_fact = [0]
        wc_fact = []
        rf_fact = RF_fact[first_month]
        for i in range(120 - first_month -1):
            rf_fact = rf_fact + oil_fact[-1] * 30.45/ niz / 1000
            wc_fact.append(mef * rf_fact ** Cw / ((1 - rf_fact) ** Co + mef * rf_fact ** Cw))
            oil_fact.append(Liq_model_f[i+first_month] * (1 - wc_fact[-1]))

        oil_fact2 = [0]
        wc_fact2 = []
        num_fact2 = int(first_month / 8)
        rf_fact2 = RF_fact[num_fact2]
        for i in range(120 - num_fact2 - 1):
            rf_fact2 = rf_fact2 + oil_fact2[-1] * 30.45 / niz / 1000
            wc_fact2.append(mef * rf_fact2 ** Cw / ((1 - rf_fact2) ** Co + mef * rf_fact2 ** Cw))
            oil_fact2.append(Liq_model_f[i + num_fact2] * (1 - wc_fact2[-1]))

        oil_fact3 = [0]
        wc_fact3 = []
        num_fact3 = int(first_month / 4)
        rf_fact3 = RF_fact[num_fact3]
        for i in range(120 - num_fact3 - 1):
            rf_fact3 = rf_fact3 + oil_fact3[-1] * 30.45 / niz / 1000
            wc_fact3.append(mef * rf_fact3 ** Cw / ((1 - rf_fact3) ** Co + mef * rf_fact3 ** Cw))
            oil_fact3.append(Liq_model_f[i + num_fact3] * (1 - wc_fact3[-1]))

        for i in range(120-1):
            if i == 47:
                print(i)
            rf = rf + oil1[-1] / niz / 1000
            w1 = mef * rf ** Cw / ((1 - rf) ** Co + mef * rf ** Cw)
            v2 = rf + Liq_model_f[i] * (1 - w1) / 2 / niz / 1000 * 30.45
            w2 = mef * v2 ** Cw / ((1 - v2) ** Co + mef * v2 ** Cw)
            v3 = rf + Liq_model_f[i] * (1 - w2) / 2 / niz / 1000 * 30.45
            w3 = mef * v3 ** Cw / ((1 - v3) ** Co + mef * v3 ** Cw)
            v4 = rf + Liq_model_f[i] * (1 - w3) / 2 / niz / 1000 * 30.45
            w4 = mef * v4 ** Cw / ((1 - v4) ** Co + mef * v4 ** Cw)

            #rf = (rf + 2 * v2 + 2 * v3 + v4) / 6
            #wc = mef * rf ** Cw / ((1 - rf) ** Co + mef * rf ** Cw)
            wc = ((1 - w1) + 2 * (1 - w2) + 2 * (1 - w3) + (1 - w4)) / 6
            Oil_model_f.append(Liq_model_f[i] * (wc))

            #Wc.append(mef * rf ** Cw / ((1 - rf) ** Co + mef * rf ** Cw))
            #Oil_model_f.append(Liq_model_f[i] * (1 - Wc[-1]))
            oil1.append(Oil_model_f[-1] * 30.5)



    # График ХВ
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 3])
    ax_1 = fig.add_subplot(gs[0])
    ax_1.set_title('Характеристика вытеснения', size=9, weight='bold')
    #ax_1.set_xlabel('Выработка, д.ед.', fontsize=7)
    ax_1.set_ylabel('Обводненность, д.ед.', fontsize=7)
    ax_1.grid(zorder=1)
    ax_1.scatter(RF_fact[:], Wc_fact[:], color='blue', s=5, zorder=3, label='fact data')
    ax_1.plot(t_1, Wc_model, color='black', zorder=2)
    #ax_1.scatter(RF_fact[-1], Wc_fact[-1], color='red', s=5, zorder=3)
    ax_1.axis([0, 1, 0, 1])
    ax_1.tick_params(axis='both', which='major', labelsize=7)


    # График Жидкости и Нефти
    ax_2 = fig.add_subplot(gs[1])
    ax_2.set_title('Дебит жидкости и нефти', size=9, weight='bold')
    ax_2.tick_params(axis='both', which='major', labelsize=7)
    ax_2.set_xlabel('Месяцы', fontsize=7)
    ax_2.set_ylabel('т/сут', fontsize=7)
    ax_2.grid(zorder=1)
    t_2 = np.arange(1, dob_liq.size+1, 1)

    ax_2.fill_between(t, Liq_model_f, np.zeros_like(Liq_model_f), color='green', alpha=0.4)
    ax_2.fill_between(t, Oil_model_f, np.zeros_like(Oil_model_f), color='m',
                      alpha=0.4)
    ax_2.plot(t, Oil_model_f, color='black', linewidth=1.7, label='oil from RF = '+str(RF_fact[1])[:4])
    ax_2.plot(t, Liq_model_f, color='green', linewidth=1.6, label='liq')

    t_fact = np.arange(first_month-1, 119, 1)
    t_fact2 = np.arange(num_fact2-1, 119, 1)
    t_fact3 = np.arange(num_fact3-1, 119, 1)
    ax_2.plot(t_fact[1:], oil_fact[1:], color='cyan', linewidth=1.6, label='oil from RF = '+str(RF_fact[first_month])[:4])
    ax_2.plot(t_fact2[1:], oil_fact2[1:], color='m', linewidth=1.6, label='oil from RF = '+str(RF_fact[num_fact2])[:4])
    ax_2.plot(t_fact3[1:], oil_fact3[1:], color='blue', linewidth=1.6, label='oil from RF = '+str(RF_fact[num_fact3])[:4])
    ax_2.scatter(t_2, dob_liq, color='blue', s=5, zorder=3, label='fact liq')
    ax_2.scatter(t_2, dob_neft, color='cyan', s=5, zorder=3, label='fact oil')
    ax_2.axis([5, 119, 0, Liq_model_f[5]])
    ax_2.tick_params(axis='both', which='major', labelsize=7)
    ax_2.legend(title='Qж и Qн для ' + str(well))



    for widget in frame.winfo_children():
        widget.destroy()


    fig.canvas.draw_idle()
    root.update()

    pass
