from environs import Env
import logging
from playwright.sync_api import sync_playwright
import telegram


def play(page, nie, name):

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

    check_url = 'https://icp.administracionelectronica.gob.es/icpplustieb/citar?p=8&locale=es'

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=2500,
        )
        context = browser.new_context()
        page = context.new_page()
        page.goto(check_url)
        try:
            has_cita = play(page, nie, name)
            if has_cita:
                bot.send_message(
                    chat_id=chat_id,
                    text=f'Походу сита есть, бегом [записываться]({check_url})\!',
                    parse_mode='MarkdownV2',
                )
            else:
                print('Ситы нема')
        except Exception as e:
            print(e)

# The requested URL was rejected. Please consult with your administrador.

if __name__ == '__main__':
    main()