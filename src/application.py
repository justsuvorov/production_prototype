from pathlib import Path

from edifice import App

from Program.AROMonitoring.aro_monitoring import AroMonitoring
from Program.GUI.data_model import DataModelMonitoring
from Program.GUI.my_app import MonitoringApp

DATA_PATH = Path(__file__).resolve().parent.parent / 'data'


def main(path: str):
    filtered = {'Company': 'All', 'Field': 'All'}
    monitoring_module = AroMonitoring(file_path=path, filter=filtered)
    app = MonitoringApp(data_model=DataModelMonitoring(monitoring_module=monitoring_module),
                        result_path=path)

    App(app).start()


if __name__ == '__main__':
    main(DATA_PATH)
