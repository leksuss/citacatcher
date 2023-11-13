from environs import Env
import logging
from playwright.sync_api import sync_playwright
import telegram
import time


DELAY_BETWEEN_REQUESTS = 600  # 10 minutes
MAX_COUNT_EXCEPTIONS = 3

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        self.tg_bot.send_message(
            chat_id=self.chat_id,
            text=self.format(record),
        )


def is_cita_available(page, nie, name):

    page.get_by_role('combobox', name='Selecciona Oficina:').select_option('14')
    page.get_by_role('combobox', name='TRÁMITES POLICÍA NACIONAL').select_option('4036')
    page.get_by_role('button', name='Aceptar').click()
    page.get_by_role('button', name='Entrar').click()
    page.get_by_label('D.N.I.Campo obligatorio \n\t\t\tN.I.E.Campo obligatorio \n\t\t\tPASAPORTECampo obligatorio \n\t\t\tPasaporte / Documento de identidadCampo obligatorio \n\t\t\tNº COLEGIADOCampo obligatorio').click()
    page.get_by_label('D.N.I.Campo obligatorio \n\t\t\tN.I.E.Campo obligatorio \n\t\t\tPASAPORTECampo obligatorio \n\t\t\tPasaporte / Documento de identidadCampo obligatorio \n\t\t\tNº COLEGIADOCampo obligatorio').fill(nie)
    page.get_by_label('Nombre y apellidosCampo obligatorio').click()
    page.get_by_label('Nombre y apellidosCampo obligatorio').fill(name)
    page.get_by_role('button', name='Aceptar').click()
    page.get_by_role('button', name='Solicitar Cita').click()
    if not page.get_by_text('En este momento no hay citas disponibles').count():
        return True
    return False


def main():
    env = Env()
    env.read_env()

    nie = env('NIE')
    name = env('NAME')

    tg_token = env('TG_TOKEN')
    chat_id = env('TG_CHAT_ID')
    bot = telegram.Bot(token=tg_token)


    formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')

    tg_log_handler = TelegramLogsHandler(bot, chat_id)
    tg_log_handler.setFormatter(formatter)
    tg_log_handler.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)

    logger.addHandler(tg_log_handler)
    logger.addHandler(stdout_handler)

    logger.debug('Bot started')

    check_url = 'https://icp.administracionelectronica.gob.es/icpplustieb/citar?p=8&locale=es'

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=2500,
        )
        context = browser.new_context()
        page = context.new_page()

        count_exceptions = 0
        while True:
            if count_exceptions >= MAX_COUNT_EXCEPTIONS:
                break
            try:
                page.goto(check_url)
                if is_cita_available(page, nie, name):
                    logger.info(f'Cita found, go make an appointment')
                    timestamp = time.strftime('%Y/%m/%d_%H_%M_%S', time.localtime())
                    page.screenshot(path=f'screenshot_{timestamp}.png')
                else:
                    logging.debug('Сит нема :(')
                time.sleep(DELAY_BETWEEN_REQUESTS)
            except Exception as e:
                logger.exception(e)
                count_exceptions += 1

# The requested URL was rejected. Please consult with your administrador.

if __name__ == '__main__':
    main()