import os

from dataclasses import dataclass


def create_characters_array(num_el):
    return str(("?, ")*num_el).replace('"', '')[:-2]


ARF_RES_GENERAL_PARAM = """                 id_parent INTEGER, 
                                            timeindex_dataframe TEXT,
                                            dobycha_nefti REAL,
                                            dobycha_gaza REAL,
                                            dobycha_kondensata REAL,
                                            neft_tovarnaya REAL,
                                            png_k_realizacii REAL,
                                            pg_k_realizacii REAL,
                                            kondensat_k_realizacii REAL,
                                            dobycha_png_dlya_raschetnoj_vyruchki_ndd REAL,
                                            dobycha_pg_dlya_raschetnoj_vyruchki_ndd REAL,
                                            capex_so_srokom_amort_3_goda_sejsmika_kap REAL,
                                            capex_so_srokom_amort_4_goda_onvss REAL,
                                            capex_so_srokom_amort_5_let_nir_plus_pir_v_grr_prochie_grr REAL,
                                            capex_so_srokom_amort_7_let_burenie_osvoenie_i_dr_pri_burenii REAL,
                                            capex_so_srokom_amort_10_let_obustr_stroitelstvo_rekonstr REAL,
                                            capex_so_srokom_amort_20_let_vneshn_tr_minus_t_krome_ploshch_obektov REAL,
                                            capex_so_srokom_amort_25_let_morskie_platformy REAL,
                                            onvss_na_podderzhanie REAL,
                                            zarezki_uglubleniya REAL,
                                            priobretenie_aktiva REAL,
                                            kv_ne_uchityvaemye_dlya_ndd REAL,
                                            amortizaciya_proshlyh_let REAL,
                                            ostatochnaya_stoimost_of_proshlyh_let REAL,
                                            opex REAL,
                                            prochie_platezhi_v_s_del_ti__plus__soc_strah_dlya_min_ndd REAL,
                                            revex_investicii_iz_opex__minus__grr_refraki_opz_i_td REAL,
                                            raskhody_iz_chistoj_pribyli_shtrafy_za_sverhnorm_szhig_socialka REAL,
                                            vyruchka_ot_gazovogo_biznesa REAL,
                                            bazhen_da__minus__0_del_net__minus__1 REAL,
                                            proverka_kgpn_dlya_pg REAL,
                                            koefficient_v_stavke_ndpi_pg REAL,
                                            lgota_po_nalogu_na_imushch_minus_vo REAL,
                                            dobycha_zhidkosti REAL,
                                            stavka_diskontirovaniya REAL,
                                            kurs_dol REAL,
                                            brent REAL,
                                            urals REAL,
                                            skidka_na_urals REAL,
                                            koeff_v_poshline_na_neft REAL,
                                            kkorr_po_ep_dlya_rasch_ndpi REAL,
                                            bazovaya_stavka_ndpi_manevr REAL,
                                            bazovaya_stavka_ndpi_do_manevra REAL,
                                            k_barr_dlya_rascheta_ep REAL,
                                            kman REAL,
                                            kdt REAL,
                                            kk REAL,
                                            transport_nefti REAL,
                                            k_barr_dlya_urals REAL,
                                            eksportnaya_poshlina REAL,
                                            nb_neft REAL,
                                            nb_png REAL,
                                            stavka_naloga_na_imushch REAL,
                                            stavka_naloga_na_pribyl REAL,
                                            lgota_po_np REAL,
                                            nb_pg REAL,
                                            nb_gk REAL,
                                            ndpi_gaz_kgpn__mensh__035 REAL,
                                            ndpi_gaz_kgpn__bolsh__035 REAL,
                                            ndpi_gk REAL,
                                            nalogovyj_rezhim REAL,
                                            kg REAL,
                                            ogranicheniya_po_spisaniyu_ubytkov REAL,
                                            indeksaciya_ubytkov REAL,
                                            stavka_otsecheniya_korrektirovki_raskhodov REAL,
                                            fakt_ndpi REAL,
                                            lgotnyj_k_minus_t_k_ndpi__minus__kd REAL,
                                            lgotnyj_k_minus_t_k_ndpi__minus__kv REAL,
                                            lgotnyj_k_minus_t_k_ndpi__minus__kz REAL,
                                            lgotnyj_k_minus_t_k_ndpi__minus__kkan REAL,
                                            nb_png_ndd REAL,
                                            nb_pg_ndd REAL,
                                            _nomer__gruppy_uchastka_mestorozhdeniya REAL,
                                            riski_dobycha_nefti REAL,
                                            rychagi_nalogi REAL,
                                            riski_dobycha_zhidkosti REAL,
                                            rychagi_opex REAL,
                                            kv_bur REAL,
                                            kv_obus REAL,
                                            god_nachala_diskontirovaniya REAL,
                                            period_ocenki REAL,
                                            stavka_ndd REAL,
                                            korrektirovka_denezhnogo_potoka REAL,
                                            ndpi_bez_ucheta_koefficienta_stavki REAL,
                                            ndpi REAL,
                                            polnaya_stavka_ndpi_v_ndd REAL,
                                            stavka_ndpi_v_ndd_s_uch_kg REAL,
                                            ndpi_neft REAL,
                                            ndpi_gaz REAL,
                                            cena_nefti_do_vycheta_ep_i_komissii_trejdinga REAL,
                                            raschetnaya_vyruchka REAL,
                                            fakticheskie_raskhody REAL,
                                            ep_raskhody REAL,
                                            tr_raskhody REAL,
                                            ndpi_raskhody REAL,
                                            raschetnye_raskhody REAL,
                                            baza_ndd REAL,
                                            baza_ndd_pribyl_god REAL,
                                            baza_ndd_ubytok_god REAL,
                                            ogranichenie_perenosa_ndd REAL,
                                            ostatok_ubytkov_dlya_perenosa REAL,
                                            perenesennye_ubytki_ndd REAL,
                                            baza_ndd_s_perenosom REAL,
                                            zatraty_ogranichennye_limitom REAL,
                                            limit_raskhodov REAL,
                                            minimalnyj_ndd REAL,
                                            fakticheskij_ndd REAL,
                                            ndd REAL,
                                            nalogi REAL,
                                            zatraty REAL,
                                            realizaciya_nefti REAL,
                                            realizaciya_png REAL,
                                            vyruchka REAL,
                                            baza_po_np_bez_ucheta_perenosa_ubytkov REAL,
                                            ebitda REAL,
                                            ebit REAL,
                                            nalog_na_pribyl REAL,
                                            nopat REAL,
                                            ocf REAL,
                                            fcf REAL,
                                            period_diskontirovaniya REAL,
                                            stoimost_denezhnoj_edinicy REAL,
                                            dcf REAL,
                                            npv REAL,
                                            investicii_v_grr_burenie_i_ob_minus_vo REAL, 
                                            pvi REAL,
                                            pi REAL,
                                            date_creation TEXT,"""


@dataclass
class CompanyDictionary:
    names = {'Арчинское': 'ГПН-Восток',
        'Западно-Лугинецкое': 'ГПН-Восток',
        'Крапивинское': 'ГПН-Восток',
        'Кулгинское': 'ГПН-Восток',
        'Нижнелугинецкое': 'ГПН-Восток',
        'Смоляное': 'ГПН-Восток',
        'Урманское': 'ГПН-Восток',
        'Шингинское': 'ГПН-Восток',
        'Южно-Табаганское': 'ГПН-Восток',
        'Аганское': 'СН-МНГ',
        'Аригольское': 'СН-МНГ',
        'Ачимовское': 'СН-МНГ',
        'Ватинское': 'СН-МНГ',
        'Восточно-Охтеурское': 'СН-МНГ',
        'Западно-Асомкинское': 'СН-МНГ',
        'Западно-Усть-Балыкское': 'СН-МНГ',
        'Западно-Чистинное': 'СН-МНГ',
        'Ининское': 'СН-МНГ',
        'Кетовское': 'СН-МНГ',
        'Кысомское': 'СН-МНГ',
        'Луговое': 'СН-МНГ',
        'Максимкинское': 'СН-МНГ',
        'Мегионское': 'СН-МНГ',
        'Мыхпайское': 'СН-МНГ',
        'Ново-Покурское': 'СН-МНГ',
        'Островное': 'СН-МНГ',
        'Покамасовское': 'СН-МНГ',
        'Северо-Ореховское': 'СН-МНГ',
        'Северо-Островное': 'СН-МНГ',
        'Северо-Покурское': 'СН-МНГ',
        'Тайлаковское': 'СН-МНГ',
        'Узунское': 'СН-МНГ',
        'Чистинное': 'СН-МНГ',
        'Южно-Аганское': 'СН-МНГ',
        'Южно-Островное': 'СН-МНГ',
        'Южно-Покамасовское': 'СН-МНГ',
        'Восточно-Мессояхское': 'Мессояха',
        'Валынтойское': 'ГПН-ННГ',
        'Восточно-Пякутинское': 'ГПН-ННГ',
        'Вынгаяхинское': 'ГПН-ННГ',
        'Еты-Пуровское': 'ГПН-ННГ',
        'Крайнее': 'ГПН-ННГ',
        'Муравленковское': 'ГПН-ННГ',
        'Пякутинское': 'ГПН-ННГ',
        'Романовское': 'ГПН-ННГ',
        'Северо-Пямалияхское': 'ГПН-ННГ',
        'Северо-Янгтинское': 'ГПН-ННГ',
        'Сугмутское': 'ГПН-ННГ',
        'Суторминское': 'ГПН-ННГ',
        'Умсейское+Южно-Пурпейское': 'ГПН-ННГ',
        'Вынгапуровское': 'ГПН-ННГ',
        'Западно-Чатылькинское': 'ГПН-ННГ',
        'Карамовское': 'ГПН-ННГ',
        'Новогоднее': 'ГПН-ННГ',
        'Отдельное': 'ГПН-ННГ',
        'Пограничное': 'ГПН-ННГ',
        'Спорышевское': 'ГПН-ННГ',
        'Средне-Итурское': 'ГПН-ННГ',
        'Холмистое': 'ГПН-ННГ',
        'Холмогорское': 'ГПН-ННГ',
        'Чатылькинское': 'ГПН-ННГ',
        'Южно-Ноябрьское': 'ГПН-ННГ',
        'Ярайнерское': 'ГПН-ННГ',
        'Балейкинское': 'ГПН-Оренбург',
        'Землянское': 'ГПН-Оренбург',
        'Капитоновское': 'ГПН-Оренбург',
        'Новозаринское': 'ГПН-Оренбург',
        'Новосамарское': 'ГПН-Оренбург',
        'Оренбургское': 'ГПН-Оренбург',
        'Рощинское': 'ГПН-Оренбург',
        'Царичанское+Филатовское': 'ГПН-Оренбург',
        'Зимнее': 'ГПН-Хантос',
        'Им. Александра Жагрина': 'ГПН-Хантос',
        'Красноленинское': 'ГПН-Хантос',
        'Орехово-Ермаковское': 'ГПН-Хантос',
        'Приобское': 'ГПН-Хантос',
        'Южное': 'ГПН-Хантос',
        'Южно-Киняминское': 'ГПН-Хантос',
        'Новопортовское': 'ГПН-Хантос'}


@dataclass
class MerakObjConst:
    DROP_UNUSED_ROW = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                       30, 31, 32, 33, 34, 35, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                       58, 59, 60, 61, 62, 63, 64, 77, 202]

    USED_ROW_DEFAULT_MB = [4, 8, 12, 15, 3, 30, 37, 38, 212, 213, 214, 215, 216, 218, 219, 220, 222, 223, 224, 226, 6,
                           5, 7, 239, 240, 241, 242, 9, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                           28, 29, 31, 32, 33, 34, 36, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55,
                           56, 57, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                           78, 79, 80, 81, 82, 83, 188, 59, 60, 192, 61, 194, 62, 196, 63, 200, 64, 198, 65, 202, 66,
                           204, 35, 206, 207, 208, 229, 230, 231, 232, 233, 234, 238, 235, 236, 237, 252, 253, 165, 154,
                           155, 156, 157, 243, 244, 246, 245, 167, 166, 168, 169, 170, 171, 172, 173, 174, 247, 248,
                           249, 250, 251, 254, 160, 161, 162, 163, 96, 97, 98, 99, 101, 102, 103, 104, 105, 106, 107,
                           109, 110, 119, 111, 127, 122, 123, 124, 125, 112, 128, 113, 129, 114, 130, 115, 131, 116,
                           132, 117, 133, 118, 134, 120, 136, 137, 138, 139, 141, 142, 143, 144, 146, 147, 148, 149,
                           151, 88, 89, 90, 91, 92, 93, 94]

    MAPPING_NAME_MB = {"Сейсмика": "Сейсмика (капитализируемая)",
                       "Бурение поисково-разведочное": "Бурение поисково-разведочное", "НИР+ПИР в ГРР": "НИР+ПИР в ГРР",
                       "Прочие КВ в ГРР": "Прочие КВ в ГРР", "Бурение эксплуатац-е": "Бурение эксплуатационное",
                       "Подготовит работы, ВМР": "Подготовит работы, ВМР",
                       "Обустройство при бурении": "Обустройство при бурении", "Освоение": "Освоение",
                       "ГРП при бурении": "ГРП при бурении", "Затраты на Зарезки": "Затраты на Зарезки",
                       "Затраты на Углубления": "Затраты на Углубления",
                       "Подготовит работы": "Подготовительные работы стр",
                       "Обустройство кустов и скважин": "Обустройство кустов и скважин стр",
                       "Платформа (шельф)": "Платформа (шельф) стр",
                       "Объекты сбора и трансп продук скв / стр-во": "Объекты сбора и транспорта продукции скважин стр",
                       "Объекты сбора и трансп продук скв / рек-ция": "Объекты сбора и транспорта продукции скважин",
                       "Терминал по наливу нефти": "Терминал по наливу нефти", "Трубопроводы / транс-т": "Трубопроводы",
                       "Газопроводы / транс-т": "Газопроводы", "Площад объекты/ транс-т": "Площадочные объекты",
                       "Объекты подготовки нефти и газа / стр-во": "Объекты подготовки нефти и газа стр",
                       "Объекты подготовки нефти и газа / рек-ция": "Объекты подготовки нефти и газа",
                       "Объекты системы ППД / стр-во": "Объекты системы ППД стр",
                       "Объекты системы ППД / рек-ция": 'Объекты системы ППД',
                       "Объекты МТО и ремонтного обеспеч / стр-во": "Объекты МТО и ремонтного обеспечения стр",
                       "Объекты МТО и ремонтного обеспеч / рек-ция": "Объекты МТО и ремонтного обеспечения",
                       "Объекты энергоснабжения / стр-во": "Объекты энергоснабжения стр",
                       "Объекты энергоснабжения / рек-ция": "Объекты энергоснабжения",
                       "Автодороги/ стр-во": "Автодороги стр", "Автодороги/ рек-ция": "Автодороги",
                       "Утилизация ПНГ/ стр-во": "Утилизация ПНГ стр", "Утилизация ПНГ/ рек-ция": "Утилизация ПНГ",
                       "Объекты соц назнач/ стр-во": "Объекты соц назначения стр",
                       "Объекты соц назнач/ рек-ция": "Объекты соц назначения",
                       "ПИР будущих лет": "ПИР будущих лет стр", "Оборуд НВСС при бурении": "ОНВСС при бурении",
                       "Оборуд НВСС при ГТМ": "ОНВСС при ГТМ", "Оборуд НВСС на поддерж": "ОНВСС на поддержание",
                       "Оборуд НВСС прочие": "ОНВСС прочие",
                       "Целевая программа трубопроводов": "Целевая программа повышения надежности трубопроводов",
                       "Прочие целевые программы": "Прочие целевые программы",
                       "Непромышленное строительство": "Непромышленное строительство",
                       "КВ по НЗС прошлых лет": "КВ по НЗС прошлых лет", "АУР капитал-й": "АУР капитализируемый",
                       "Выкуп земельного участка": "Выкуп земельного участка", "НМА": "НМА", "Прочие КВ": "Прочие КВ ",
                       "КВ не учитываемые для НДД": "КВ не учитываемые для НДД",
                       "Ввод ОФ с пулом 3 года": "Ввод ОФ с пулом 3 года",
                       "Ввод ОФ с пулом 4 года": "Ввод ОФ с пулом 4 года",
                       "Ввод ОФ с пулом 5 лет": "Ввод ОФ с пулом 5 лет",
                       "Ввод ОФ с пулом 7 лет": "Ввод ОФ с пулом 7 лет",
                       "Ввод ОФ с пулом 10 лет": "Ввод ОФ с пулом 10 лет",
                       "Ввод ОФ с пулом 20 лет": "Ввод ОФ с пулом 20 лет",
                       "Ввод ОФ с пулом 25 лет": "Ввод ОФ с пулом 25 лет"}

    DEFAULT_NAME_MB = {
        "Для проектов ГРП + Проч": "Для проектов ГРП + Прочие", "Строительство стр": "Строительство",
        "Подготовительные работы стр": "Подготовительные работы",
        "Обустройство кустов и скважин стр": "Обустройство кустов и скважин",
        "Объекты сбора и транспорта продукции скважин стр": "Объекты сбора и транспорта продукции скважин",
        "Объекты подготовки нефти и газа стр": "Объекты подготовки нефти и газа",
        "Объекты системы ППД стр": "Объекты системы ППД",
        "Объекты МТО и ремонтного обеспечения стр": "Объекты МТО и ремонтного обеспечения",
        "Объекты энергоснабжения стр": "Объекты энергоснабжения", "Автодороги стр": "Автодороги",
        "Утилизация ПНГ стр": "Утилизация ПНГ", "Объекты соц назначения стр": "Объекты соц назначения",
        "Платформа (шельф) стр": "Платформа (шельф)", "ПИР будущих лет стр": "ПИР будущих лет"
    }


@dataclass
class DBTextCreate:
    CREATE_PP_CASE_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_pp_case (
                                       case_id NUMERIC NOT NULL UNIQUE,
                                       name TEXT NOT NULL,
                                       user_id TEXT,
                                       well_link TEXT,
                                       peep_type NUMERIC NOT NULL,
                                       model_name TEXT NOT NULL,
                                       portfolio_flag NUMERIC DEFAULT 0,
                                       guid_id TEXT NOT NULL UNIQUE,
                                       sensitivity_id INTEGER,
                                       last_applied_edit NUMERIC DEFAULT 0,
                                       fds_connection_parameter TEXT,
                                       well_document_category TEXT,
                                       well_document_id TEXT,
                                       well_document_name TEXT)"""

    CREATE_PP_DEPENDENCY_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_pp_dependency (
                                             source_object_type INTEGER NOT NULL,
                                             source_object_id INTEGER NOT NULL,
                                             target_object_type INTEGER NOT NULL,
                                             target_object_id INTEGER NOT NULL,
                                             target_object_name TEXT NOT NULL)"""

    CREATE_PP_CONSOLIDATION_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_pp_consolidation (
                                                cons_id INTEGER NOT NULL,
                                                name TEXT NOT NULL,
                                                peep_type INTEGER NOT NULL)"""

    CREATE_PP_BATCH_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_pp_batch (
                                        batch_id INTEGER NOT NULL,
                                        name TEXT NOT NULL)"""

    CREATE_ATTR_CASE_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_attr_case (
                                               archive_id INTEGER DEFAULT 0,
                                               link_id INTEGER NOT NULL UNIQUE,
                                               ua_a_blok TEXT,
                                               ua_b_dzo TEXT,
                                               ua_c_active TEXT,
                                               ua_d_field TEXT,
                                               ua_e_case_name TEXT,
                                               ua_f_case_code TEXT,
                                               ua_g_case_view TEXT,
                                               ua_h_case_type TEXT,
                                               ua_i_kp_option TEXT,
                                               ua_j_kp_podoption TEXT,
                                               ua_k_planfakt TEXT,
                                               ua_l_case_length INTEGER,
                                               ua_m_modules_number INTEGER,
                                               ua_n_bp_including TEXT,
                                               ua_o_infra_objects_including TEXT,
                                               ua_p_dop_infra_necessary TEXT,
                                               ua_q_investment_start INTEGER,
                                               ua_r_investment_end INTEGER,
                                               ua_s_pm_ TEXT,
                                               ua_t_pm_job_title TEXT,
                                               ua_u_ps TEXT,
                                               ua_v_ps_job_title TEXT,
                                               ua_w_economist TEXT,
                                               ua_x_case_status TEXT,
                                               ua_y_approval TEXT,
                                               ua_z_budget TEXT,
                                               ua_description TEXT)"""
                                               # ua_start_prom_razrab INTEGER,
                                               # ua_start_ndd INTEGER,
                                               # ua_category_of_area INTEGER,
                                               # ua_ndd_carry_over TEXT,
                                               # ua_za_ndd_return_dns_y INTEGER)"""
    #                                            ua_zb_license_area TEXT DEFAULT NULL)"""
    # # ua_zb_license_area
    CREATE_1_MK_PROIZVOD_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_1_MK_proizvod (
                                             ID INTEGER NOT NULL,
                                             mesyac INTEGER NOT NULL,
                                             god INTEGER NOT NULL,
                                             dob_jidkosti REAL,
                                             dob_nefti REAL,
                                             jidkost_gtm_tek_goda REAL,
                                             neft_gtm_tek_goda REAL,
                                             skolz_dob_nefti REAL,
                                             dob_png REAL,
                                             sjiganie_png REAL,
                                             png_sobstv_nujdy REAL,
                                             zakachka_png_v_plast REAL,
                                             dob_pg REAL,
                                             gaz_na_el_energiu REAL,
                                             zakachka_gaza_v_plast REAL,
                                             dob_kondensata REAL,
                                             vyrab_zapasov REAL,
                                             ispyt_skv REAL,
                                             vvod_nn_dob_skv REAL,
                                             vvod_gs_dob_skv REAL,
                                             vvod_novyh_nagn_skv REAL,
                                             vvod_vodozab_skv REAL,
                                             vvod_poisk_razved_skv REAL,
                                             vvod_poglosh_skv REAL,
                                             vvod_gaz_skv_phg REAL,
                                             vybyt_neft_skv REAL,
                                             vybyt_nagn_skv REAL,
                                             vybyt_gaz_skv REAL,
                                             vybyt_gaz_skv_phg REAL,
                                             perevod_skv_pod_zakachku REAL,
                                             zakachka_vody REAL,
                                             gtm_na_deistv_dob_fond REAL,
                                             gtm_na_deistv_nagn_fond REAL,
                                             gtm_na_bezdeistv_dob_fond REAL,
                                             gtm_na_bezdeistv_nagn_fond REAL,
                                             Neuspesh_gtm REAL,
                                             grp_bur_podhody_flota REAL,
                                             sredn_fond_dob_skv_neft REAL,
                                             sredn_fond_dob_skv_gas REAL,
                                             sredn_fond_nagn_skv REAL,
                                             ekspl_fond_dob_skv REAL,
                                             ecspl_fond_nagn_skv REAL,
                                             ecspl_fond_gaz_skv REAL,
                                             otrab_vrema_dob_neft_skv REAL,
                                             otrab_vrema_nagn_skv REAL,
                                             otrab_vrema_dob_gaz_skv REAL,
                                             pusk_debit_nefti REAL,
                                             burenie_prohodka REAL,
                                             prodolj_burenia REAL,
                                             prodolj_osvoenia REAL,
                                             prohodka_zbs REAL,
                                             prodolj_bur_zbs REAL,
                                             prodolj_osv_zbs REAL,
                                             chislennost_personala REAL,
                                             proizv_personal_mr REAL,
                                             AUP_mr REAL,
                                             AUP_DZO REAL,
                                             prochii_personal_DZO REAL,
                                             dly_proektov_grp REAL,
                                             prodoljit_pzr REAL,
                                             v_t_ch_neuspeshn_pzr REAL,
                                             kol_vo_rir REAL,
                                             kol_vo_gnkt REAL,
                                             kol_vo_pvr REAL,
                                             kol_vo_grp_podhody_flota REAL,
                                             kol_vo_opz_sko REAL,
                                             prodolj_supervaizinga REAL,
                                             blok_krs_prs_invest REAL,
                                             kol_vo_krs_invest REAL,
                                             prodolj_1krs_invest REAL,
                                             zatraty_na_krs_invest REAL,
                                             kol_vo_krs_dop_invest REAL,
                                             prodolj_1krs_dop_invest REAL,
                                             zatraty_na_krs_dop_invest REAL,
                                             kol_vo_prs_invest REAL,
                                             prodolj_1prs_invest REAL,
                                             zatraty_na_prs_invest REAL,
                                             blok_krs_prs_tek REAL,
                                             kol_vo_krs_tek REAL,
                                             prodolj_1krs_tek REAL,
                                             zatraty_na_krs_tek REAL,
                                             kol_vo_prs_tek REAL,
                                             prodolj_1prs_tek REAL,
                                             zatraty_na_prs_tek REAL,
                                             roditel INTEGER)"""
    CREATE_UNIQUE_INDEX_1_MK_PROIZVODL: str = """CREATE UNIQUE INDEX IF NOT EXISTS id_m_y1
                                                 ON fem_1_MK_proizvod (ID, mesyac, god)"""

    CREATE_2_MK_INVEST_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_2_MK_invest (
                                            ID INTEGER NOT NULL,
                                            mesyac INTEGER NOT NULL,
                                            god INTEGER NOT NULL,
                                            inv_vvod_of REAL,
                                            inv_vvod_of_3_goda REAL,
                                            inv_vvod_of_4_goda REAL,
                                            inv_vvod_of_5_let REAL,
                                            inv_vvod_of_7_let REAL,
                                            inv_vvod_of_10_let REAL,
                                            inv_vvod_of_20_let REAL,
                                            inv_vvod_of_25_let REAL,
                                            inv_grr REAL,
                                            inv_seismika_capex REAL,
                                            inv_burenie_poisk_razved REAL,
                                            inv_nir_pir_grr REAL,
                                            inv_prochie_kv_grr REAL,
                                            inv_burenie REAL,
                                            inv_burenie_ekspl REAL,
                                            inv_podgot_raboty_vmr REAL,
                                            inv_obustr_pri_burenii REAL,
                                            inv_osvoenie REAL,
                                            inv_grp_pri_burenii REAL,
                                            inv_na_zarezki REAL,
                                            inv_na_ugleblenia REAL,
                                            stroitelstvo REAL,
                                            str_podgot_raboty REAL,
                                            str_obustr_kustov_skv REAL,
                                            str_obektov_sbora REAL,
                                            str_obektov_podgotovki REAL,
                                            str_obektov_ppd REAL,
                                            str_obektov_mto REAL,
                                            str_obektov_energetiki REAL,
                                            str_avtodorog REAL,
                                            str_obektov_util_png REAL,
                                            str_obektov_soc_naznach REAL,
                                            str_platform_shelf REAL,
                                            pir_budush_let REAL,
                                            vneshnii_transport REAL,
                                            vt_terminal_naliva_neft REAL,
                                            vt_truboprovody REAL,
                                            vt_gazoprovody REAL,
                                            vt_ploshadoch_obekty REAL,
                                            rekonstrukcia_baza REAL,
                                            rek_obektov_sbora_prod_skv REAL,
                                            rek_obektov_podg_nefti_gaza REAL,
                                            rek_obektov_ppd REAL,
                                            rek_obektov_mto REAL,
                                            rek_obektov_energetiki REAL,
                                            rek_avtodorog REAL,
                                            rek_obektov_util_png REAL,
                                            rek_obektov_soc_naznach REAL,
                                            onvss REAL,
                                            onvss_burenia REAL,
                                            onvss_gtm REAL,
                                            onvss_podderj_bazy REAL,
                                            onvss_prochie REAL,
                                            celevye_programmy REAL,
                                            celevay_programma_trubopr REAL,
                                            prochie_celevye_programmy REAL,
                                            nepromyshlennoe_str_vo REAL,
                                            kv_nzs_proshlyh_let REAL,
                                            prochie_kv REAL,
                                            prochie_kv_AUR REAL,
                                            prochie_kv_vykup_zem_uch REAL,
                                            prochie_kv_nma REAL,
                                            prochie_kv_prochie REAL,
                                            kv_neuchit_ndd REAL,
                                            spravochno_kv_obustr REAL,
                                            spravochno_pir REAL,
                                            spravochno_smr REAL,
                                            spravochno_oborud REAL,
                                            spravochno_prochie REAL,
                                            spravochno_valutn_kv REAL,
                                            spravochno_kv_fin_usd REAL,
                                            spravochno_kv_osv_usd REAL,
                                            spravochno_kv_fin_eur REAL,
                                            spravochno_kv_osv_eur REAL,
                                            finansirovanie_proekta REAL,
                                            varuchka_gaz_biznesa REAL,
                                            rashody_na_fin_rezultat REAL,
                                            shtafy_sverhnorm_sjig_png REAL,
                                            priobretenie_aktiva REAL,
                                            plata_operat_uslugi REAL,
                                            zatraty_upr_kompanii REAL,
                                            vaplata_proc_po_kreditu REAL,
                                            prochie_nalogi_v_sebest REAL,
                                            rezerv_nepredv_rashodov REAL,
                                            investicii_v_sebestoim REAL,
                                            zatraty_na_grr REAL,
                                            grr_polev_raboty_2d REAL,
                                            grr_polev_raboty_2d_st_t_1km REAL,
                                            grr_kameral_raboty_2d REAL,
                                            grr_supervaizing_2d REAL,
                                            grr_polev_raboty_3d REAL,
                                            grr_polev_raboty_3d_st_t_1km2 REAL,
                                            grr_kameral_raboty_3d REAL,
                                            grr_supervaizing_3d REAL,
                                            grr_nir_pir_ne_capex REAL,
                                            grr_prochie REAL,
                                            zatraty_neuspeshnye_remonty REAL,
                                            dla_proektov_grp_prochie REAL,
                                            v_zatraty_na_pzr REAL,
                                            v_st_t_operacii_pzr REAL,
                                            v_zatraty_na_rir REAL,
                                            v_st_t_operacii_rir REAL,
                                            v_zatraty_na_gnkt REAL,
                                            v_st_t_operacii_gnkt REAL,
                                            v_zatraty_na_grp REAL,
                                            v_st_t_operacii_grp REAL,
                                            v_zatraty_na_pvr REAL,
                                            v_st_t_operacii_pvr REAL,
                                            v_zatraty_na_opz REAL,
                                            v_st_t_operacii_opz REAL,
                                            v_zatraty_na_supervaizing REAL,
                                            v_st_t_supervaizinga REAL,
                                            v_zatraty_na_neuspeshnye_gtm REAL,
                                            v_st_t_neuspeshnogo_gtm REAL,
                                            v_zatraty_na_soputstv_operacii REAL,
                                            v_prochie_invest_v_sebest REAL,
                                            roditel INTEGER)"""
    CREATE_UNIQUE_INDEX_2_MK_INVEST: str = """CREATE UNIQUE INDEX IF NOT EXISTS id_m_y2
                                              ON fem_2_MK_invest (ID, mesyac, god)"""

    CREATE_3_MK_OPEX_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_3_MK_opex (
                                            ID INTEGER NOT NULL,
                                            mesyac INTEGER NOT NULL,
                                            god INTEGER NOT NULL,
                                            ekspl_zatraty REAL,
                                            peremen_opex REAL,
                                            ud_zatr_na_neft REAL,
                                            ud_zatr_na_jidkost REAL,
                                            ud_zatr_na_zakachku REAL,
                                            ud_zatr_na_pg REAL,
                                            ud_zatr_na_kondensat REAL,
                                            zatr_na_soderj_fonda_skv REAL,
                                            ud_zatr_na_neft_skv REAL,
                                            ud_zatr_na_nagn_skv REAL,
                                            ud_zatr_na_gaz_skv REAL,
                                            _prochie_zatraty REAL,
                                            post_zatr_nezavis_ot_fonda REAL,
                                            AUR_bez_skp REAL,
                                            prochie_rash_s_skp REAL,
                                            rashody_ne_uchit_v_NDD REAL,
                                            roditel INTEGER)"""
    CREATE_UNIQUE_INDEX_3_MK_OPEX: str = """CREATE UNIQUE INDEX IF NOT EXISTS id_m_y3
                                            ON fem_3_MK_opex (ID, mesyac, god)"""

    CREATE_4_MK_DOP_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_4_MK_dop (
                                            ID INTEGER NOT NULL,
                                            mesyac INTEGER NOT NULL,
                                            god INTEGER NOT NULL,
                                            dop_informacia REAL,
                                            flag_krupn_obychny_proekt REAL,
                                            uchet_proekta_v_dfv REAL,
                                            kategoria_slojnosti_proekta REAL,
                                            lgota_po_EP REAL,
                                            lgota_po_NDPI REAL,
                                            lgota_po_nal_na_imush REAL,
                                            lgota_po_Kv REAL,
                                            lgota_po_vazkosti REAL,
                                            lgota_po_Kz REAL,
                                            MRP REAL,
                                            dola_poter_nefti REAL,
                                            dola_poter_png REAL,
                                            dola_poter_pg REAL,
                                            dola_poter_kond REAL,
                                            flag_amort_avto_ruchn REAL,
                                            flag_uskor_amort REAL,
                                            amortizacia_proshl_let REAL,
                                            ost_st_t_of_proshl_let REAL,
                                            strah_vznosy_ot_fot REAL,
                                            prochie_plateji_v_sebest REAL,
                                            prochie_rashody_iz_ch_prib REAL,
                                            chuvstv_revex REAL,
                                            chuvstv_opex REAL,
                                            proverka_kgpn REAL,
                                            k_t_k_NDPI_pg REAL,
                                            k_t_NDPI REAL,
                                            roditel INTEGER)"""
    CREATE_UNIQUE_INDEX_4_MK_DOP: str = """CREATE UNIQUE INDEX IF NOT EXISTS id_m_y4
                                           ON fem_4_MK_dop (ID, mesyac, god)"""

    CREATE_MULT_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_mult (
                                          name_elem TEXT NOT NULL,
                                          ntype_elem INTEGER NOT NULL,
                                          mult_elem REAL NOT NULL,
                                          parent_cons TEXT NOT NULL)"""
    CREATE_UNIQUE_INDEX_MULT: str = """CREATE UNIQUE INDEX IF NOT EXISTS n_t_p
                                       ON fem_mult (name_elem, ntype_elem, parent_cons)"""

    CREATE_ECONOMIC_LIMIT_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_economic_limit(
                                                              case_id INTEGER NOT NULL UNIQUE,
                                                              case_name TEXT NOT NULL,
                                                              month_limit INTEGER NOT NULL,
                                                              year_limit INTEGER NOT NULL,
                                                              type_limit TEXT NOT NULL)"""

    CREATE_DSP_I_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_DSP_I(
                                            case_id INTEGER NOT NULL,
                                            case_date TEXT NOT NULL,
                                            rs_qualifier TEXT NOT NULL,
                                            time_stamp	TEXT NOT NULL,
                                            oil_volume_total REAL DEFAULT 0,
                                            oil_volume_base REAL DEFAULT 0,
                                            oil_volume_addl REAL DEFAULT 0,
                                            oil_prodres_ratio REAL DEFAULT 0,
                                            oil_volume_comm REAL DEFAULT 0,
                                            assoc_gas_volume_total REAL DEFAULT 0,
                                            assoc_gas_volume_util REAL DEFAULT 0,
                                            assoc_gas_util_ratio REAL DEFAULT 0,
                                            assoc_gas_volume_comm REAL DEFAULT 0,
                                            assoc_gas_volume_internal REAL DEFAULT 0,
                                            natural_gas_volume_total REAL DEFAULT 0,
                                            natural_gas_volume_comm REAL DEFAULT 0,
                                            condensate_volume_total REAL DEFAULT 0,
                                            condensate_volume_comm REAL DEFAULT 0,
                                            hc_volume_total REAL DEFAULT 0,
                                            liquid_volume_total REAL DEFAULT 0,
                                            liquid_volume_artlift REAL DEFAULT 0,
                                            water_cut REAL DEFAULT 0,
                                            water_inj_volume REAL DEFAULT 0,
                                            water_inj_comp_ratio REAL DEFAULT 0,
                                            well_total_count REAL DEFAULT 0,
                                            well_prod_count REAL DEFAULT 0,
                                            well_inj_count REAL DEFAULT 0,
                                            well_water_count REAL DEFAULT 0,
                                            well_gas_count REAL DEFAULT 0,
                                            well_prod_count_nominal REAL DEFAULT 0,
                                            well_prod_count_active REAL DEFAULT 0,
                                            well_prod_inactive_ratio REAL DEFAULT 0,
                                            drilled_wells_total REAL DEFAULT 0,
                                            drilled_wells_jurassic REAL DEFAULT 0,
                                            drilled_wells_prod_total REAL DEFAULT 0,
                                            drilled_wells_prod_deviated REAL DEFAULT 0,
                                            drilled_wells_prod_horiz REAL DEFAULT 0,
                                            drilled_wells_inj_total REAL DEFAULT 0,
                                            drilled_wells_water_total REAL DEFAULT 0,
                                            drilled_wells_gas_total REAL DEFAULT 0,
                                            drilled_wells_expl_total REAL DEFAULT 0,
                                            drilled_wells_frac_count REAL DEFAULT 0,
                                            intervention_total_count REAL DEFAULT 0,
                                            intervention_inactive_count REAL DEFAULT 0,
                                            intervention_sidetrack_count REAL DEFAULT 0,
                                            intervention_deephoriz_count REAL DEFAULT 0,
                                            intervention_frac_count REAL DEFAULT 0,
                                            intervention_insulation_count REAL DEFAULT 0,
                                            intervention_shallow_count REAL DEFAULT 0,
                                            intervention_eor_count REAL DEFAULT 0,
                                            intervention_other_count REAL DEFAULT 0,
                                            intervention_failed_count REAL DEFAULT 0,
                                            workover_total_count REAL DEFAULT 0,
                                            workover_prod_count REAL DEFAULT 0,
                                            workover_inj_count REAL DEFAULT 0,
                                            workover_gas_count REAL DEFAULT 0,
                                            servicing_total_count REAL DEFAULT 0,
                                            servicing_inv_count REAL DEFAULT 0,
                                            servicing_noninv_count REAL DEFAULT 0,
                                            personnel_total_count REAL DEFAULT 0,
                                            personnel_prod_count REAL DEFAULT 0,
                                            personnel_mna_field_count REAL DEFAULT 0,
                                            personnel_mna_affil_count REAL DEFAULT 0,
                                            personnel_other_count REAL DEFAULT 0)"""

    CREATE_DSP_II_1_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_DSP_II_1(
                                            case_id INTEGER NOT NULL,
                                            case_date TEXT NOT NULL,
                                            rs_qualifier TEXT NOT NULL,
                                            time_stamp	TEXT NOT NULL,
                                            total_capex REAL DEFAULT 0,
                                            exploration_total_capex REAL DEFAULT 0,
                                            exploration_drilling_capex REAL DEFAULT 0,
                                            exploration_seismic_capex REAL DEFAULT 0,
                                            exploration_research_capex REAL DEFAULT 0,
                                            exploration_other_capex REAL DEFAULT 0,
                                            wells_total_capex REAL DEFAULT 0,
                                            wells_drilling_capex REAL DEFAULT 0,
                                            wells_preparation_capex REAL DEFAULT 0,
                                            wells_development_capex REAL DEFAULT 0,
                                            wells_frac_capex REAL DEFAULT 0,
                                            constr_total_capex REAL DEFAULT 0,
                                            constr_preparation_capex REAL DEFAULT 0,
                                            constr_wellpad_capex REAL DEFAULT 0,
                                            constr_transport_capex REAL DEFAULT 0,
                                            constr_treatment_capex REAL DEFAULT 0,
                                            constr_injection_capex REAL DEFAULT 0,
                                            constr_workshop_capex REAL DEFAULT 0,
                                            constr_energy_supply_capex REAL DEFAULT 0,
                                            constr_roads_capex REAL DEFAULT 0,
                                            constr_assoc_gas_util_capex REAL DEFAULT 0,
                                            constr_social_capex REAL DEFAULT 0,
                                            constr_offshore_capex REAL DEFAULT 0,
                                            constr_future_rnd_capex REAL DEFAULT 0,
                                            transport_total_capex REAL DEFAULT 0,
                                            transport_terminal_capex REAL DEFAULT 0,
                                            transport_pipelines_capex REAL DEFAULT 0,
                                            transport_gas_lines_capex REAL DEFAULT 0,
                                            transport_facilities_capex REAL DEFAULT 0,
                                            reconstr_total_capex REAL DEFAULT 0,
                                            reconstr_transport_capex REAL DEFAULT 0,
                                            reconstr_treatment_capex REAL DEFAULT 0,
                                            reconstr_injection_capex REAL DEFAULT 0,
                                            reconstr_workshop_capex REAL DEFAULT 0,
                                            reconstr_energy_supply_capex REAL DEFAULT 0,
                                            reconstr_roads_capex REAL DEFAULT 0,
                                            reconstr_assoc_gas_util_capex REAL DEFAULT 0,
                                            reconstr_social_capex REAL DEFAULT 0,
                                            equipment_total_capex REAL DEFAULT 0,
                                            equipment_drilling_capex REAL DEFAULT 0,
                                            equipment_intervention_capex REAL DEFAULT 0,
                                            equipment_sustain_capex REAL DEFAULT 0,
                                            equipment_other_capex REAL DEFAULT 0,
                                            program_total_capex REAL DEFAULT 0,
                                            program_reliability_capex REAL DEFAULT 0,
                                            program_misc_capex REAL DEFAULT 0,
                                            program_non_prod_constr_capex REAL DEFAULT 0,
                                            program_in_progress_capex REAL DEFAULT 0,
                                            intervention_sidetrack_capex REAL DEFAULT 0,
                                            intervention_deepening_capex REAL DEFAULT 0,
                                            misc_total_capex REAL DEFAULT 0,
                                            misc_admin_mgmt_capex REAL DEFAULT 0,
                                            misc_land_property_capex REAL DEFAULT 0,
                                            misc_intangible_capex REAL DEFAULT 0,
                                            misc_exploration_capex REAL DEFAULT 0,
                                            misc_other_capex REAL DEFAULT 0)"""

    CREATE_DSP_II_2_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_DSP_II_2(
                                            case_id INTEGER NOT NULL,
                                            case_date TEXT NOT NULL,
                                            rs_qualifier TEXT NOT NULL,
                                            time_stamp	TEXT NOT NULL,
                                            total_revex REAL DEFAULT 0,
                                            intervention_frac_revex REAL DEFAULT 0,
                                            intervention_squeeze_job_revex REAL DEFAULT 0,
                                            coiled_tubing_revex REAL DEFAULT 0,
                                            perforating_operation_revex REAL DEFAULT 0,
                                            completion_preparation_revex REAL DEFAULT 0,
                                            wellbore_treatment_revex REAL DEFAULT 0,
                                            workover_total_revex REAL DEFAULT 0,
                                            workover_base_revex REAL DEFAULT 0,
                                            workover_addl_revex REAL DEFAULT 0,
                                            _workover_total_opex__3 REAL DEFAULT 0,
                                            servicing_total_revex REAL DEFAULT 0,
                                            servicing_inv_revex REAL DEFAULT 0,
                                            _servicing_noninv_opex__3 REAL DEFAULT 0,
                                            intervention_failed_revex REAL DEFAULT 0,
                                            misc_operation_revex REAL DEFAULT 0,
                                            supervising_revex REAL DEFAULT 0,
                                            other_total_revex REAL DEFAULT 0)"""

    CREATE_DSP_III_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_DSP_III(
                                            case_id INTEGER NOT NULL,
                                            case_date TEXT NOT NULL,
                                            rs_qualifier TEXT NOT NULL,
                                            time_stamp	TEXT NOT NULL,
                                            total_opex REAL DEFAULT 0,
                                            variable_total_opex REAL DEFAULT 0,
                                            well_total_opex REAL DEFAULT 0,
                                            well_count_opex REAL DEFAULT 0,
                                            workover_total_opex REAL DEFAULT 0,
                                            servicing_noninv_opex REAL DEFAULT 0,
                                            fixed_total_opex REAL DEFAULT 0,
                                            fixed_nonwell_opex REAL DEFAULT 0,
                                            fixed_admin_mgmt_opex REAL DEFAULT 0,
                                            fixed_other_opex REAL DEFAULT 0)"""

    CREATE_DSP_VI_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_DSP_VI(
                                            case_id INTEGER NOT NULL,
                                            case_date TEXT NOT NULL,
                                            rs_qualifier TEXT NOT NULL,
                                            time_stamp	TEXT NOT NULL,
                                            _мортизация_ВСЕГО REAL DEFAULT 0,
                                            _мортизация_прошлых_лет REAL DEFAULT 0,
                                            _мортизация_новых_ОФ REAL DEFAULT 0,
                                            _алоги_и_затраты_на_фин_резуль REAL DEFAULT 0,
                                            _ДПИ_на_нефть1 REAL DEFAULT 0,
                                            _ДПИ_на_газ_природ1 REAL DEFAULT 0,
                                            _ДПИ_на_конденсат1 REAL DEFAULT 0,
                                            WI_Страховые_взносы__от_ФОТ_ REAL DEFAULT 0,
                                            _рочие_налоги_в_себ_ти REAL DEFAULT 0,
                                            _алог_на_имущество REAL DEFAULT 0,
                                            _рочие_платежи_в_себ_ти REAL DEFAULT 0,
                                            _асходы_отн_на_фин_результат REAL DEFAULT 0,
                                            ndd_tax_pay REAL DEFAULT 0,
                                            WI_Лимитные_расходы_НДД REAL DEFAULT 0,
                                            _актич__расходы_для_лимита REAL DEFAULT 0)"""

    CREATE_DSP_V_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS fem_DSP_V(
                                            case_id INTEGER NOT NULL,
                                            case_date TEXT NOT NULL,
                                            rs_qualifier TEXT NOT NULL,
                                            time_stamp TEXT NOT NULL,
                                            total_revenue REAL DEFAULT 0,
                                            oil_revenue REAL DEFAULT 0,
                                            assoc_gas_revenue REAL DEFAULT 0,
                                            natural_gas_revenue REAL DEFAULT 0,
                                            condensate_revenue REAL DEFAULT 0,
                                            gas_business_revenue REAL DEFAULT 0,
                                            total_expenses REAL DEFAULT 0,
                                            pretax_income REAL DEFAULT 0,
                                            profit_tax REAL DEFAULT 0,
                                            profit_expenses REAL DEFAULT 0,
                                            acquisition_expenses REAL DEFAULT 0,
                                            free_cash_flow REAL DEFAULT 0,
                                            cum_free_cash_flow REAL DEFAULT 0,
                                            disc_cash_flow REAL DEFAULT 0,
                                            cum_disc_cash_flow REAL DEFAULT 0,
                                            ocf_1 REAL DEFAULT 0,
                                            ocf_2 REAL DEFAULT 0,
                                            cum_disc_investment REAL DEFAULT 0,
                                            discount_coef REAL DEFAULT 0,
                                            disc_investment REAL DEFAULT 0,
                                            ocf_not_covered REAL DEFAULT 0,
                                            disc_inv_less_ncocf REAL DEFAULT 0,
                                            correction_fcf REAL DEFAULT 0)"""

    CREATE_ARF_PROD_ECM_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_ecm( 
                                                 {}
    FOREIGN KEY (id_parent) REFERENCES arf_prod_obj_information (id) ON DELETE CASCADE)""".format(ARF_RES_GENERAL_PARAM)
    CREATE_ARF_VBD_PROD_ECM_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_ecm( 
                                                 {}
    FOREIGN KEY (id_parent) REFERENCES arf_prod_obj_information (id) ON DELETE CASCADE)""".format(ARF_RES_GENERAL_PARAM)

    CREATE_ARF_PROD_INFO_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_obj_information (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    type_option TEXT,
                                                    affiliated_company TEXT,
                                                    field TEXT,
                                                    license_area TEXT,
                                                    preparation_object TEXT,
                                                    group_name TEXT,
                                                    well_number TEXT,
                                                    npv_max REAL,
                                                    gap_period REAL,
                                                    fcf_first_month REAL,
                                                    oil_production_full REAL,
                                                    fluid_extraction_full REAL,
                                                    fcf_full REAL,
                                                    oil_production_gap REAL,
                                                    fluid_extraction_gap REAL,
                                                    fcf_gap  REAL,
                                                    calculation_horizon INTEGER,
                                                    oil_production_year REAL,
                                                    fluid_extraction_year REAL,
                                                    fcf_year REAL)"""

    CREATE_ARF_PROD_MONITORING_INFO_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_obj_information (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    affiliated_company TEXT,
                                                    field TEXT,
                                                    license_area TEXT,
                                                    preparation_object TEXT,
                                                    group_name TEXT,
                                                    well_number TEXT)"""

    CREATE_ARF_PROD_MONITORING_SCENARIOS_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_scenarios (
                                                    id_parent INTEGER,
                                                    type_scenarios TEXT,
                                                    npv_max REAL,
                                                    gap_period REAL,
                                                    fcf_first_month REAL,
                                                    oil_production_full REAL,
                                                    fluid_extraction_full REAL,
                                                    fcf_full REAL,
                                                    oil_production_gap REAL,
                                                    fluid_extraction_gap REAL,
                                                    fcf_gap REAL,
                                                    calculation_horizon INTEGER,
                                                    oil_production_year REAL,
                                                    fluid_extraction_year REAL,
                                                    fcf_year REAL,
    FOREIGN KEY (id_parent) REFERENCES arf_prod_obj_information (id) ON DELETE CASCADE)"""

    CREATE_ARF_PROD_MONITORING_SCENARIOS_INDEX_TABLE_SQL: str = """CREATE UNIQUE INDEX IF NOT EXISTS idp_ts_dolc
                                                                    ON arf_prod_scenarios 
                                                                    (id_parent, 
                                                                    type_scenarios, 
                                                                    date_of_last_calculation)"""

    CREATE_ARF_PROD_MONITORING_ECM_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_ecm( 
                                                 {}
    FOREIGN KEY (id_parent) REFERENCES arf_prod_obj_information (id) ON DELETE CASCADE)""".format(ARF_RES_GENERAL_PARAM)

    CREATE_ARF_VBD_PROD_INFO_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_prod_obj_information (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    type_option TEXT,
                                                    affiliated_company TEXT,
                                                    field TEXT,
                                                    license_area TEXT,
                                                    preparation_object TEXT,
                                                    group_name TEXT,
                                                    well_number TEXT,
                                                    npv_max REAL,
                                                    gap_period REAL,
                                                    fcf_first_month REAL,
                                                    oil_production_full REAL,
                                                    fluid_extraction_full REAL,
                                                    fcf_full REAL,
                                                    oil_production_gap REAL,
                                                    fluid_extraction_gap REAL,
                                                    fcf_gap  REAL,
                                                    calculation_horizon INTEGER,
                                                    oil_production_year REAL,
                                                    fluid_extraction_year REAL,
                                                    fcf_year REAL,
                                                    cost_v_b_d REAL,
                                                    comment_gtm TEXT,
                                                    comment_infro TEXT,
                                                    date_of_last_calculation TEXT,
                                                    plan_fact TEXT,
                                                    obj_status TEXT,
                                                    type_obj TEXT,
                                                    plan_date_next_scenario TEXT,
                                                    approval TEXT)"""

    CREATE_ASPID_INFO_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS aspid_info(
                                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                 field TEXT,
                                                 well_number TEXT)"""
    CREATE_ASPID_CONSTANTS_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS aspid_cons( 
                                                 DEBIT_STOP REAL,
                                                 WATER_CUT_STOP REAL,
                                                 MINIMAL_RESERVES REAL,
                                                 YEAR_MINIMAL REAL,
                                                 YEAR_MAXIMAL REAL,
                                                 MAXIMUM_RADIUS REAL,
                                                 HORIZON INTEGER,
                                                 FLAG_SHELF_WATERLOGGING INTEGER,
                                                 FLAG_SHELF_LIQUID INTEGER,
                                                 ANCHOR_POINT_FOR_OIL_ REAL,
                                                 ANCHOR_POINT_FOR_WATER_ REAL,
                                                 COREY_OIL_LEFT_ REAL,
                                                 COREY_WATER_LEFT_ REAL,
                                                 MEF_LEFT_ REAL,
                                                 MEF_RIGHT_ REAL,
                                                 K1_LEFT_ REAL,
                                                 K1_RIGHT_ REAL,
                                                 K2_LEFT_ REAL,
                                                 K2_RIGHT_ REAL)"""
    CREATE_ASPID_PROD_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS aspid_prod( 
                                            id_parent INTEGER, 
                                            timeindex TEXT,
                                            oil_production_mor REAL,
                                            fluid_extraction_mor REAL,
    FOREIGN KEY (id_parent) REFERENCES aspid_info (id) ON DELETE CASCADE)"""

    CREATE_ASPID_FACT_DEBIT_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS aspid_fact_debit( 
                                            id_parent INTEGER, 
                                            timeindex TEXT,
                                            oil_production_fact REAL,
                                            fluid_extraction_fact REAL,
    FOREIGN KEY (id_parent) REFERENCES aspid_info (id) ON DELETE CASCADE)"""

    CREATE_MOR_INFO_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS mor_info(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    affiliated_company TEXT,
                                                    field TEXT,
                                                    stratum TEXT,
                                                    license_area TEXT,
                                                    group_name TEXT,
                                                    well_number TEXT,
                                                    bottom_hole_coordinates_x INTEGER DEFAULT Null,
                                                    bottom_hole_coordinates_y INTEGER DEFAULT Null)"""
    CREATE_MOR_PROD_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS mor_prod(
                                            id_parent INTEGER,
                                            date TEXT,
                                            work_nature TEXT,
                                            end_month_status TEXT,
                                            working_hours_pour_month INTEGER,
                                            oil_production_t_m REAL,
                                            fluid_extraction_t_m REAL,
                                            pumping_m3_m REAL,
    FOREIGN KEY (id_parent) REFERENCES mor_info (id) ON DELETE CASCADE)""" # ONSTRAINT id_date UNIQUE (id_parent, date)

    CREATE_MOR_NGT_INFO_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS mor_info(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    field TEXT,
                                                    group_name TEXT,
                                                    well_number TEXT,
                                                    bottom_hole_coordinates_x INTEGER DEFAULT Null,
                                                    bottom_hole_coordinates_y INTEGER DEFAULT Null)"""
    CREATE_MOR_NGT_PROD_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS mor_prod(
                                            id_parent INTEGER,
                                            stratum TEXT,
                                            date TEXT,
                                            work_nature TEXT,
                                            end_month_status TEXT,
                                            working_hours_pour_month INTEGER,
                                            oil_production_t_m REAL,
                                            fluid_extraction_t_m REAL,
                                            injectivity_last_month_m3_s REAL,
    FOREIGN KEY (id_parent) REFERENCES mor_info (id) ON DELETE CASCADE)""" # ONSTRAINT id_date UNIQUE (id_parent, date)
    CREATE_UNIQUE_INDEX_MOR_NGT_PROD: str = """CREATE UNIQUE INDEX IF NOT EXISTS i_d
                                              ON mor_prod (id_parent, date)"""
    CREATE_ARF_ORIGIN_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS arf_origin(
                 do TEXT,
                 mestorozhdenie TEXT,
                 licenzionnyj_uchastok TEXT,
                 zatraty_vbd REAL,
                 _nomer__skv TEXT,
                 data_ostanovki TEXT,
                 _nomer__kusta TEXT,
                 objekt_podgotovki TEXT,
                 razrabatyvaemye_plasty TEXT,
                 sostoyanie_v_tekhrezhime TEXT,
                 kommentarij_po_nahozhdeniyu_v_nf TEXT,
                 otrabotannoe_vremya_za_mesyac REAL,
                 gazovyj_faktor REAL,
                 debit_zhidk_m3 REAL,
                 debit_zhidk_t REAL,
                 debit_nefti REAL,
                 proc_obv_mass REAL,
                 data_zapuska_po_fondu TEXT,
                 srednee_mrp_po_mestrozhdeniyu REAL,
                 tarif_na_elektroenergiyu_pokupka_generaciya_peredacha REAL,
                 ure_na_ppd REAL,
                 ure_na_podg_nefti REAL,
                 ure_transport_zhidkosti REAL,
                 ure_transp_nefti REAL,
                 ure_transp_podt_vody REAL,
                 ure_vneshnij_transport_nefti REAL,
                 ure_sbor_i_transort_png REAL,
                 procent_realizacii_png REAL,
                 tekhnologicheskie_poteri_nefti REAL,
                 shtrafy_za_szhiganie_png REAL,
                 peremennye_raskhody_po_iskusstvennomu_vozdejstviyu_na_plastkrome_elektroenergii REAL,
                 peremennye_raskhody_po_tekhnologicheskoj_podgotovke_neftikrome_elektroenergii REAL,
                 peremennye_raskhody_po_transportirovke_nefti_krome_elektroenergii REAL,
                 peremennye_raskhody_po_sboru_i_transportirovke_poputnogo_gazakrome_elektroenergii REAL,
                 peremennye_kommercheskie_raskhody REAL,
                 udelnye_ot_nefti_samovyvoz_transp REAL,
                 stoimost_geofizicheskih_issledovanij REAL,
                 stoimost_rtzh_plus_opz REAL,
                 stoimost_tekushchego_remonta__obshchaya REAL,
                 debit_zhidk_mer REAL,
                 debit_nefti_mer REAL,
                 podtovarnaya_voda REAL,
                 zakachka REAL,
                 udelnyj_raskhod_ee_na_mp REAL,
                 sverhnormativnoe_szhiganie_png REAL,
                 stoimost_obsluzhivaniya_uecn REAL,
                 stoimost_prokata_uecn REAL,
                 stoimost_obsluzhivaniya_nkt REAL,
                 stoimost_obsluzhivaniya_shtang REAL,
                 stoimost_obsluzhivaniya_stanka_minus_kachalki REAL,
                 stoimost_obsluzhivaniya_dopoborudovaniya REAL,
                 proc_bazovoj_dobychi_ot_predydushchego_dnya REAL,
                 date_arf TEXT,
                 type_option TEXT)"""
    CREATE_ARF_ORIGIN_INDEX_TABLE_SQL: str = """CREATE UNIQUE INDEX IF NOT EXISTS w_f_t
                                                ON arf_origin (mestorozhdenie, _nomer__skv, type_option)"""
    CREATE_NGT_ALIASES_TABLE_SQL: str = """CREATE TABLE IF NOT EXISTS ngt_aliases(
                                            field_ngt TEXT,
                                            trunk_ngt TEXT,
                                            well_number TEXT)"""


@dataclass
class DBTextInsert:
    INSERTION_PP_CASE_TABLE_SQL: str = """INSERT INTO fem_pp_case VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    INSERTION_PP_DEPENDENCY_TABLE_SQL: str = """INSERT INTO fem_pp_dependency VALUES (?, ?, ?, ?, ?)"""

    INSERTION_PP_CONSOLIDATION_TABLE_SQL: str = """INSERT INTO fem_pp_consolidation VALUES (?, ?, ?)"""

    INSERTION_PP_BATCH_TABLE_SQL: str = """INSERT INTO fem_pp_batch VALUES (?, ?)"""

    INSERTION_ATTR_CASE_TABLE_SQL: str = """INSERT INTO fem_attr_case VALUES ({})""".format(create_characters_array(29))

    INSERTION_1_MK_PROIZVOD_TABLE_SQL: str = """INSERT OR IGNORE
                                                INTO fem_1_MK_proizvod 
                                                VALUES ({}, NULL)""".format(create_characters_array(84))

    INSERTION_2_MK_INVEST_TABLE_SQL: str = """INSERT OR IGNORE
                                              INTO fem_2_MK_invest 
                                              VALUES ({}, NULL)""".format(create_characters_array(119))

    INSERTION_3_MK_OPEX_TABLE_SQL: str = """INSERT OR IGNORE
                                            INTO fem_3_MK_opex VALUES ({},  NULL)""".format(create_characters_array(19))

    INSERTION_4_MK_DOP_TABLE_SQL: str = """INSERT OR IGNORE
                                            INTO fem_4_MK_dop VALUES ({}, NULL)""".format(create_characters_array(30))

    INSERTION_MULT_TABLE_SQL: str = """INSERT OR IGNORE INTO fem_mult VALUES (?, ?, ?, ?)"""

    INSERTION_ECONOMIC_LIMIT_TABLE_SQL: str = """INSERT OR IGNORE INTO fem_economic_limit VALUES (?, ?, ?, ?, ?)"""

    INSERTION_DSP_I_TABLE_SQL: str = """INSERT INTO fem_DSP_I VALUES ({})""".format(create_characters_array(64))

    INSERTION_DSP_II_1_TABLE_SQL: str = """INSERT INTO fem_DSP_II_1 VALUES ({})""".format(create_characters_array(60))

    INSERTION_DSP_II_2_TABLE_SQL: str = """INSERT INTO fem_DSP_II_2 VALUES ({})""".format(create_characters_array(22))

    INSERTION_DSP_III_TABLE_SQL: str = """INSERT INTO fem_DSP_III VALUES ({})""".format(create_characters_array(14))

    INSERTION_DSP_VI_TABLE_SQL: str = """INSERT INTO fem_DSP_VI VALUES ({})""".format(create_characters_array(19))

    INSERTION_DSP_V_TABLE_SQL: str = """INSERT INTO fem_DSP_V VALUES ({})""".format(create_characters_array(27))

    INSERTION_ARF_PROD_INFO_TABLE_SQL: str = (
        """INSERT INTO arf_prod_obj_information VALUES ({})""".format(create_characters_array(21))
    )
    INSERTION_ARF_VBD_PROD_INFO_TABLE_SQL: str = (
        """INSERT INTO arf_prod_obj_information VALUES ({})""".format(create_characters_array(30))
    )

    INSERTION_ARF_PROD_ECM_TABLE_SQL: str = (
        """INSERT INTO arf_prod_ecm VALUES ({}, datetime('now', '+3 hours'))""".format(
            create_characters_array(127)
        )
    )
    INSERTION_ARF_PROD_MONITORING_SCENARIOS_TABLE_SQL: str = (
        """INSERT OR IGNORE INTO arf_prod_scenarios VALUES ({})""".format(create_characters_array(23))
    )

    INSERTION_ARF_PROD_MONITORING_ECM_TABLE_SQL: str = (
        """INSERT OR IGNORE INTO arf_prod_ecm VALUES ({})""".format(create_characters_array(128))
    )

    INSERTION_ARF_VBD_PROD_ECM_TABLE_SQL: str = (
        """INSERT INTO arf_prod_ecm VALUES ({}, datetime('now', '+3 hours'))""".format(
            create_characters_array(127)
        )
    )
    INSERTION_ARF_VBD_PROD_ECM_WITH_DATE_TABLE_SQL: str = (
        """INSERT INTO arf_prod_ecm VALUES ({})""".format(
            create_characters_array(128)
        )
    )

    INSERTION_ARF_PROD_ECM_WITH_DATE_TABLE_SQL: str = (
        """INSERT INTO arf_prod_ecm VALUES ({})""".format(
            create_characters_array(128)
        )
    )

    # INSERTION_ARF_PROD_ECM_TABLE_SQL: str = (
    #     """INSERT INTO arf_prod_ecm VALUES ({}, datetime('now', '+3 hours'))""".format(
    #         create_characters_array(172)
    #     )
    # )
    INSERTION_ASPID_CONSTANTS_TABLE_SQL = (
        """INSERT INTO aspid_cons VALUES ({})""".format(create_characters_array(19))
    )

    INSERTION_ASPID_INFO_TABLE_SQL = (
        """INSERT INTO aspid_info VALUES ({})""".format(create_characters_array(3))
    )

    INSERTION_ASPID_PROD_TABLE_SQL = (
        """INSERT INTO aspid_prod VALUES ({})""".format(create_characters_array(4))
    )

    INSERTION_ASPID_FACT_DEBI_TABLE_SQL = (
        """INSERT INTO aspid_fact_debit VALUES ({})""".format(create_characters_array(4))
    )

    INSERTION_MOR_INFO_TABLE_SQL = (
        """INSERT INTO mor_info VALUES ({})""".format(create_characters_array(9))
    )

    # INSERTION_MOR_PROD_TABLE_SQL = (
    #     """INSERT INTO mor_prod VALUES ({})
    #         ON CONFLICT(id_parent, date)
    #         DO UPDATE SET
    #                 id_parent = excluded.id_parent,
    #                 date = excluded.date,
    #                 work_nature = excluded.work_nature,
    #                 end_month_status = excluded.end_month_status,
    #                 working_hours_pour_month = excluded.working_hours_pour_month,
    #                 oil_production_t_m = excluded.oil_production_t_m,
    #                 fluid_extraction_t_m = excluded.fluid_extraction_t_m,
    #                 pumping_m3_m = excluded.pumping_m3_m""".format(create_characters_array(8))
    # )

    INSERTION_MOR_PROD_TABLE_SQL = (
        """INSERT INTO mor_prod VALUES ({})""".format(create_characters_array(8))
    )

    INSERTION_MOR_NGT_INFO_TABLE_SQL = (
        """INSERT INTO mor_info VALUES ({})""".format(create_characters_array(6))
    )

    INSERTION_MOR_NGT_PROD_TABLE_SQL = (
        """INSERT OR IGNORE INTO mor_prod VALUES ({})""".format(create_characters_array(9))
    )

    INSERTION_ARF_ORIGIN_TABLE_SQL = (
        """INSERT INTO arf_origin VALUES ({})""".format(create_characters_array(54))
    )

    INSERTION_ARF_PROD_MONITORING_INFO_TABLE_SQL = (
        """INSERT INTO arf_prod_obj_information VALUES ({})""".format(create_characters_array(7))
    )
    INSERTION_NGT_ALIASES_TABLE_SQL = (
        """INSERT INTO ngt_aliases VALUES ({})""".format(create_characters_array(3))
    )


@dataclass
class DBTextSelect:
    GET_PP_CASE_TABLE_SQL: str = """SELECT
                                    case_id,
                                    name,
                                    user_id,
                                    well_link,
                                    peep_type,
                                    model_name,
                                    portfolio_flag,
                                    guid_id,
                                    sensitivity_id,
                                    last_applied_edit,
                                    fds_connection_parameter,
                                    well_document_category,
                                    well_document_id,
                                    well_document_name
                                    FROM pp_case"""
    GET_CASE_SPECIALLY_SQL: str = """SELECT
                                     merak_attr_case.link_id,
                                     pp_case.name,
                                     merak_attr_case.ua_i_kp_option
                                     FROM pp_case
                                     LEFT JOIN merak_attr_case ON pp_case.case_id = merak_attr_case.link_id"""
    GET_PP_DEPENDENCY_TABLE_SQL: str = """SELECT * FROM pp_dependency"""
    GET_PP_CONSOLIDATION_TABLE_SQL: str = """SELECT
                                             cons_id,
                                             name,
                                             peep_type
                                             FROM pp_consolidation"""
    # Прописать последовательность
    GET_PP_BATCH_TABLE_SQL: str = """SELECT batch_id, name FROM pp_batch"""
    GET_MERAK_ATTR_CASE_TABLE_SQL: str = """SELECT 
                                               archive_id,
                                               link_id,
                                               ua_a_blok,
                                               ua_b_dzo,
                                               ua_c_active,
                                               ua_d_field,
                                               ua_e_case_name,
                                               ua_f_case_code,
                                               ua_g_case_view,
                                               ua_h_case_type,
                                               ua_i_kp_option,
                                               ua_j_kp_podoption,
                                               ua_k_planfakt,
                                               ua_l_case_length,
                                               ua_m_modules_number,
                                               ua_n_bp_including,
                                               ua_o_infra_objects_including,
                                               ua_p_dop_infra_necessary,
                                               ua_q_investment_start,
                                               ua_r_investment_end,
                                               ua_s_pm_,
                                               ua_t_pm_job_title,
                                               ua_u_ps,
                                               ua_v_ps_job_title,
                                               ua_w_economist,
                                               ua_x_case_status,
                                               ua_y_approval,
                                               ua_z_budget,
                                               ua_description
                                               FROM merak_attr_case"""
    GET_DSP_I: str = """SELECT * FROM mp_DSP_I"""
    GET_DSP_II_1: str = """SELECT * FROM mp_DSP_II_1"""
    GET_DSP_II_2: str = """SELECT * FROM mp_DSP_II_2"""
    GET_DSP_III: str = """SELECT * FROM mp_DSP_III"""
    GET_DSP_VI: str = """SELECT * FROM mp_DSP_VI"""
    GET_DSP_V: str = """SELECT * FROM mp_DSP_V"""
    GET_ARF_PROD_WELL_INFO_TABLE_SQL: str = """SELECT id FROM arf_prod_obj_information 
                                          WHERE field = ?  AND type_option = ? AND group_name = ? AND well_number = ?"""
    GET_ARF_PROD_GROUP_INFO_TABLE_SQL: str = """SELECT id FROM arf_prod_obj_information  
                                           WHERE field = ?  AND type_option = ? AND group_name = ?"""
    GET_ARF_PROD_DNS_INFO_TABLE_SQL: str = """SELECT id FROM arf_prod_obj_information  
                                         WHERE field = ?  AND type_option = ? AND preparation_object = ?"""
    GET_ARF_PROD_INEFFECTIVE_OBJ_TABLE_SQL: str = """SELECT DISTINCT 
                                                arf_prod_obj_information.*, arf_prod_ecm.date_creation 
                                                FROM arf_prod_obj_information 
                                                LEFT JOIN arf_prod_ecm 
                                                ON arf_prod_obj_information.id == arf_prod_ecm.id_parent 
                                                WHERE arf_prod_obj_information.gap_period <= 12 
                                                AND arf_prod_obj_information.type_option 
                                                IN ('WELL_ECONOMIC', 'GROUP_ECONOMIC', 'PREPARATION_OBJECT_ECONOMIC')"""
    GET_ARF_ASPID_INFO_TABLE_SQL: str = """SELECT id FROM aspid_info WHERE field = ? AND well_number = ?"""
    GET_ARF_ASPID_INFO_ALL_FIELD_TABLE_SQL: str = """SELECT * FROM aspid_info
                                                         WHERE field = ?"""
    GET_ARF_ORIGIN_FIELD_TABLE_SQL: str = """SELECT * FROM arf_origin WHERE mestorozhdenie = ?"""
    GET_ARF_PROD_MONITORING_ECM_BY_ID_TABLE_SQL: str = """SELECT * FROM arf_prod_ecm 
                                                          WHERE id_parent IN (SELECT id FROM arf_prod_obj_information
                                                                              WHERE field = ?)"""
    GET_ARF_PROD_MONITORING_INFO_BY_FIELD_TABLE_SQL: str = """SELECT * FROM arf_prod_obj_information WHERE field = ?"""
    GET_ARF_PROD_ECM_BY_ID_TABLE_SQL: str = """SELECT * FROM arf_prod_ecm 
                                                          WHERE id_parent IN (SELECT id FROM arf_prod_obj_information
                                                                              WHERE field = ?)"""
    GET_ARF_PROD_INFO_BY_FIELD_TABLE_SQL: str = """SELECT * FROM arf_prod_obj_information WHERE field = ?"""
    GET_ARF_ASPID_INFO_ALL_FIELDS_AND_WELLS_TABLE_SQL: str = """SELECT field, well_number FROM aspid_info"""
    GET_ARF_ASPID_INFO_BY_FIELD_TABLE_SQL: str = """SELECT field, well_number FROM aspid_info WHERE field =?"""
    GET_ARF_ASPID_FIELDS_INFO_TABLE_SQL: str = """SELECT DISTINCT field FROM aspid_info"""
    GET_ARF_ORIGIN_FIELDS_TABLE_SQL: str = """SELECT DISTINCT mestorozhdenie FROM arf_origin"""
    GET_ARF_PROD_FIELDS_TABLE_SQL: str = """SELECT DISTINCT field FROM arf_prod_obj_information"""
    GET_ARF_ASPID_PROD_TABLE_SQL: str = """SELECT * FROM aspid_prod WHERE id_parent = ?"""
    GET_ARF_ASPID_PROD_BY_ID_TABLE_SQL: str = """SELECT * FROM aspid_prod 
                                                WHERE id_parent IN (SELECT id FROM aspid_info
                                                                    WHERE field = ?)"""
    GET_ASPID_FACT_DEBIT_TABLE_SQL: str = """SELECT * FROM aspid_fact_debit WHERE id_parent = ?"""
    GET_MOR_INFO_TABLE_SQL: str = """SELECT id FROM mor_info WHERE field = ?  AND well_number = ?"""
    GET_MOR_NGT_INFO_TABLE_SQL: str = """SELECT id FROM mor_info WHERE field = ?  AND well_number = ?"""
    GET_MOR_NGT_WELL_STRATUM_TABLE_SQL: str = """SELECT stratum FROM mor_prod WHERE id_parent = ? 
                                               AND date = (SELECT MAX(date) FROM mor_prod WHERE id_parent = ?)"""
    GET_ARF_PROD_MONITORING_INFO_TABLE_SQL: str = """SELECT id FROM arf_prod_obj_information 
                                                    WHERE field = ?  AND {} = ?"""
    GET_ARF_PROD_MONITORING_ECM_TABLE_SQL: str = """SELECT * FROM arf_prod_ecm 
                                                    WHERE id_parent IN {}"""
    GET_ALL_WELLS_MOR_NGT_INFO_TABLE_SQL: str = """SELECT DISTINCT id FROM mor_info"""
    GET_MOR_NGT_FOR_CIN_WATER_PIPE_TABLE_SQL: str = """SELECT 
                                  mor_info.well_number as "№ скважины",
                                  mor_info.field as "Месторождение",
                                  mor_info.bottom_hole_coordinates_x as "Координата забоя Х (по траектории)",
                                  mor_info.bottom_hole_coordinates_y as "Координата забоя Y (по траектории)",
                                  mor_prod.stratum as "Объекты работы",
                                  mor_info.group_name as "Куст",
                                  mor_prod.work_nature as "Характер работы",
                                  mor_prod.end_month_status as "Состояние",
                                  mor_prod.injectivity_last_month_m3_s as "Приемистость за последний месяц, м3/сут"
                           FROM mor_prod
                           LEFT JOIN mor_info ON mor_prod.id_parent = mor_info.id 
                           WHERE mor_info.id = {0} 
                           AND date = (SELECT MAX(date) FROM mor_prod WHERE id_parent = {0})"""
    GET_MOR_NGT_FIELDS_INFO_TABLE_SQL: str = """SELECT DISTINCT field FROM mor_info"""
    GET_MOR_NGT_INFO_FOR_ASPID_TABLE_SQL: str = """SELECT id,
                                                          field,
                                                          group_name,
                                                          well_number,
                                                          bottom_hole_coordinates_y,
                                                          bottom_hole_coordinates_x
                                                          FROM mor_info WHERE field = ?"""
    GET_MOR_NGT_PROD_FOR_ASPID_TABLE_SQL: str = """SELECT id_parent,
                                                          date, 
                                                          end_month_status,
                                                          work_nature,
                                                          oil_production_t_m, 
                                                          fluid_extraction_t_m, 
                                                          working_hours_pour_month, 
                                                          injectivity_last_month_m3_s,
                                                          stratum 
                                                          FROM mor_prod
                                                          WHERE id_parent IN (
                                                                SELECT id FROM mor_info 
                                                                WHERE field = ?)"""
    GET_MOR_NGT_INACTIVE_WELL_LAST_PROD_TABLE_SQL: str = """SELECT 
                                                          mor_info.id,
                                                          mor_info.well_number,
                                                          mor_info.field,
                                                          mor_prod.date,
                                                          mor_prod.oil_production_t_m, 
                                                          mor_prod.fluid_extraction_t_m, 
                                                          mor_prod.working_hours_pour_month 
                                                          FROM mor_prod
                                                          LEFT JOIN mor_info ON mor_info.id = mor_prod.id_parent
                                                          WHERE mor_prod.oil_production_t_m > 0
                                                          AND mor_info.id IN {}"""
    GET_MOR_NGT_INACTIVE_WELL_TABLE_SQL: str = """SELECT mor_info.id,
                                                         mor_info.well_number,
                                                         mor_info.group_name,
                                                         mor_info.field,
                                                         mor_info.bottom_hole_coordinates_y,
                                                         mor_info.bottom_hole_coordinates_x,
                                                         mor_prod.date as req_date,
                                                         mor_prod.end_month_status, 
                                                         mor_prod.work_nature,
                                                         mor_prod.working_hours_pour_month,
                                                         mor_prod.stratum
                                                  FROM mor_prod 
                                                  LEFT JOIN mor_info ON mor_info.id = mor_prod.id_parent
                                                  WHERE end_month_status IN (?, ?, ?, ?, ?, ?) 
                                                  AND req_date >= ? 
                                                  AND work_nature = ?"""
    GET_ALL_ARF_ORIGIN_TABLE_SQL: str = """SELECT * FROM arf_origin"""
    GET_ARF_VBD_PROD_WELL_INFO_TABLE_SQL: str = """SELECT id FROM arf_prod_obj_information 
                                          WHERE field = ?  AND type_option = ? AND group_name = ? AND well_number = ?"""
    GET_ALL_ARF_VBD_PROD_TABLE_SQL: str = """SELECT * FROM arf_prod_obj_information"""
    GET_COMMENT_GTM_ARF_VBD_PROD_TABLE_SQL: str = """SELECT comment_gtm FROM arf_prod_obj_information
                                        WHERE field = ?  AND type_option = ? AND group_name = ? AND well_number = ?"""
    GET_COMMENT_INFRO_ARF_VBD_PROD_TABLE_SQL: str = """SELECT comment_infro FROM arf_prod_obj_information
                                        WHERE field = ?  AND type_option = ? AND group_name = ? AND well_number = ?"""
    GET_PLAN_DATE_NEXT_SCENARIO_ARF_VBD_PROD_TABLE_SQL: str = """SELECT plan_date_next_scenario 
                                                                 FROM arf_prod_obj_information
                                        WHERE field = ?  AND type_option = ? AND group_name = ? AND well_number = ?"""
    GET_APPROVAL_ARF_VBD_PROD_TABLE_SQL: str = """SELECT approval FROM arf_prod_obj_information
                                        WHERE field = ?  AND type_option = ? AND group_name = ? AND well_number = ?"""
    GET_NGT_ALIASES_TABLE_SQL: str = """SELECT * FROM ngt_aliases"""
    GET_SLICE_FROM_ASPID_TABLE_SQL: str = """SELECT 
                                             aspid_info.field, 
                                             aspid_info.well_number,
                                             aspid_prod.timeindex,
                                             aspid_prod.oil_production_mor as oil_production,
                                             aspid_prod.fluid_extraction_mor as fluid_extraction
                                             FROM aspid_info
                                             LEFT JOIN aspid_prod ON aspid_info.id = aspid_prod.id_parent
                                             WHERE aspid_prod.timeindex BETWEEN ? AND ?
                                             AND (
                                                SELECT timeindex 
                                                FROM aspid_prod AS a_p 
                                                WHERE a_p.id_parent = aspid_info.id 
                                                AND DATE(timeindex) = ?) IS NOT NULL"""
    GET_SLICE_FROM_MOR_TABLE_SQL: str = """SELECT 
                                            mor_info.field, 
                                            mor_info.well_number,
                                            mor_prod.date,
                                            mor_prod.oil_production_t_m,
                                            mor_prod.fluid_extraction_t_m,
                                            mor_prod.working_hours_pour_month
                                            FROM mor_info
                                            LEFT JOIN mor_prod ON mor_info.id = mor_prod.id_parent
                                            WHERE mor_info.field = ? AND mor_info.well_number = ?
                                            AND mor_prod.date BETWEEN ? AND ?"""

    # GET_MONTHLY_WELL_INDICATOR_FROM_GFEM_RESULTS_SQL: str = """SELECT
    #                                     arf_prod_obj_information.field as 'Месторождение',
    #                                     arf_prod_obj_information.well_number as 'Скважина',
    #                                     arf_prod_obj_information.group_name as 'Куст',
    #                                     arf_prod_ecm.dobycha_nefti as 'НДН за первый месяц; тыс. т',
    #                                     arf_prod_ecm.fcf as 'FCF первый месяц:'
    #                                     FROM arf_prod_obj_information
    #                                     LEFT JOIN arf_prod_ecm ON arf_prod_obj_information.id = arf_prod_ecm.id_parent
    #                                     WHERE arf_prod_obj_information.type_option = 'WELL_ECONOMIC'
    #                                     AND arf_prod_obj_information.field = ?
    #                                     AND arf_prod_obj_information.well_number = ?
    #                                     AND arf_prod_ecm.timeindex_dataframe = ?"""

    GET_MONTHLY_WELL_INDICATOR_FROM_GFEM_RESULTS_SQL: str = """SELECT 
                                        arf_prod_obj_information.field as 'Месторождение', 
                                        arf_prod_obj_information.well_number as 'Скважина',
                                        arf_prod_obj_information.group_name as 'Куст',
                                        arf_prod_ecm.dobycha_nefti as 'НДН за первый месяц; тыс. т', 
                                        arf_prod_ecm.fcf as 'FCF первый месяц:'
                                        FROM arf_prod_obj_information
                                        LEFT JOIN arf_prod_ecm ON arf_prod_obj_information.id = arf_prod_ecm.id_parent
                                        WHERE arf_prod_obj_information.type_option = 'WELL_ECONOMIC'
                                        AND arf_prod_obj_information.field IN {} 
                                        AND arf_prod_obj_information.well_number IN {}
                                        AND arf_prod_ecm.timeindex_dataframe = ?"""

@dataclass
class DBTextUpdate:
    UPDATING_MOR_INFO_TABLE_SQL: str = """UPDATE mor_info SET (
                                    affiliated_company,
                                    stratum,
                                    license_area,
                                    group_name) = ({}) WHERE id = ?""".format(create_characters_array(4))
    UPDATING_MOR_NGT_INFO_TABLE_SQL: str = """UPDATE mor_info SET (
                                    bottom_hole_coordinates_x,
                                    bottom_hole_coordinates_y,
                                    group_name) = ({}) WHERE id = ?""".format(create_characters_array(3))
    UPDATING_ARF_VBD_PROD_INFO_TABLE_SQL: str = """UPDATE arf_prod_obj_information SET (
                                    comment_gtm,
                                    comment_infro,
                                    npv_max,
                                    gap_period,
                                    fcf_first_month,
                                    oil_production_full,
                                    fluid_extraction_full,
                                    fcf_full,
                                    oil_production_gap,
                                    fluid_extraction_gap,
                                    fcf_gap,
                                    calculation_horizon,
                                    oil_production_year,
                                    fluid_extraction_year,
                                    fcf_year,
                                    cost_v_b_d,
                                    date_of_last_calculation,
                                    plan_fact,
                                    obj_status,
                                    type_obj,
                                    plan_date_next_scenario,
                                    approval) = ({}) WHERE id = ?""".format(create_characters_array(22))
    UPDATING_ROW_ARF_ORIGIN_TABLE_SQL: str = """UPDATE arf_origin SET (
                 do,
                 mestorozhdenie,
                 licenzionnyj_uchastok,
                 zatraty_vbd,
                 _nomer__skv,
                 data_ostanovki,
                 _nomer__kusta,
                 objekt_podgotovki,
                 razrabatyvaemye_plasty,
                 sostoyanie_v_tekhrezhime,
                 kommentarij_po_nahozhdeniyu_v_nf,
                 otrabotannoe_vremya_za_mesyac,
                 gazovyj_faktor,
                 debit_zhidk_m3,
                 debit_zhidk_t,
                 debit_nefti,
                 proc_obv_mass,
                 data_zapuska_po_fondu,
                 srednee_mrp_po_mestrozhdeniyu,
                 tarif_na_elektroenergiyu_pokupka_generaciya_peredacha,
                 ure_na_ppd,
                 ure_na_podg_nefti,
                 ure_transport_zhidkosti,
                 ure_transp_nefti,
                 ure_transp_podt_vody,
                 ure_vneshnij_transport_nefti,
                 ure_sbor_i_transort_png,
                 procent_realizacii_png,
                 tekhnologicheskie_poteri_nefti,
                 shtrafy_za_szhiganie_png,
                 peremennye_raskhody_po_iskusstvennomu_vozdejstviyu_na_plastkrome_elektroenergii,
                 peremennye_raskhody_po_tekhnologicheskoj_podgotovke_neftikrome_elektroenergii,
                 peremennye_raskhody_po_transportirovke_nefti_krome_elektroenergii,
                 peremennye_raskhody_po_sboru_i_transportirovke_poputnogo_gazakrome_elektroenergii,
                 peremennye_kommercheskie_raskhody,
                 udelnye_ot_nefti_samovyvoz_transp,
                 stoimost_geofizicheskih_issledovanij,
                 stoimost_rtzh_plus_opz,
                 stoimost_tekushchego_remonta__obshchaya,
                 debit_zhidk_mer,
                 debit_nefti_mer,
                 podtovarnaya_voda,
                 zakachka,
                 udelnyj_raskhod_ee_na_mp,
                 sverhnormativnoe_szhiganie_png,
                 stoimost_obsluzhivaniya_uecn,
                 stoimost_prokata_uecn,
                 stoimost_obsluzhivaniya_nkt,
                 stoimost_obsluzhivaniya_shtang,
                 stoimost_obsluzhivaniya_stanka_minus_kachalki,
                 stoimost_obsluzhivaniya_dopoborudovaniya,
                 proc_bazovoj_dobychi_ot_predydushchego_dnya,
                 date_arf,
                 type_option) = ({})  
                 WHERE mestorozhdenie = ?  AND type_option = ? AND _nomer__kusta = ? AND _nomer__skv = ?
                 """.format(create_characters_array(54))
    UPDATING_ARF_PROD_OBJ_INFO_TABLE_SQL: str = """UPDATE arf_prod_obj_information SET ({}) = (?)
                                                   WHERE field = ?
                                                   AND well_number = ?
                                                   AND type_option = ?"""


@dataclass
class DBTextDelete:
    DELETE_VALUE_ARF_PROD_ECM_TABLE_SQL: str = """DELETE FROM arf_prod_ecm WHERE id_parent = ?"""
    DELETE_VALUE_ARF_VBD_PROD_ECM_TABLE_SQL: str = """DELETE FROM arf_prod_ecm WHERE id_parent = ?"""
    DELETE_VALUE_ASPID_TABLE_SQL: str = """DELETE FROM aspid_prod WHERE id_parent = ?"""
    DELETE_VALUE_ASPID_FACT_DEBIT_TABLE_SQL: str = """DELETE FROM aspid_fact_debit WHERE id_parent = ?"""


@dataclass
class DBConstants(DBTextCreate, DBTextInsert, DBTextSelect):
    SIP: os.path = os.path.join(os.getcwd(), 'db', 'LOCAL_UPSTREAM_SIP_2022_2024.db')
    KPRA: os.path = os.path.join(os.getcwd(), 'db', 'LOCAL_COMPLEX_PROJ_2021_IK_21.7.db')
    SIP_DSP: os.path = os.path.join(os.getcwd(), 'db', 'LOCAL_UPSTREAM_SIP_2022_2024_DSP.db')
    SIP_CONNECT: str = r"Driver={SQL Server Native Client 11.0};" \
                       r"Server=Spb99-ntc-mkdb1;" \
                       r"Database=MERAK_UPSTREAM_SIP_2022_2024;" \
                       r"UID=update_macro;" \
                       r"PWD=M#rak2010;"
    KPRA_CONNECT: str = r"Driver={SQL Server Native Client 11.0};" \
                        r"Server=Spb99-ntc-mkdb1;" \
                        r"Database=MERAK_COMPLEX_PROJ_2021_IK_21.7_COPY;" \
                        r"UID=update_macro;" \
                        r"PWD=M#rak2010;"
