from script import husa, snemovna, hybernia
from func import all_func

logger = all_func.logger_init("MAIN")

logger.info('Downloading_data-START')
Hybernia = hybernia.get_value()
Husa = husa.get_value()
Snemovna = snemovna.get_value()
rest_dict = {'Hybernia': Hybernia,
             'Husa': Husa,
             'Snemovna': Snemovna}
logger.info("Downloading_data-END")

logger.info("Export_to_file-START")
all_func.file_export(rest_dict)
logger.info("Export_to_file-END")