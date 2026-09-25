from appium.webdriver.common.appiumby import AppiumBy
from datetime import datetime
from features.pages.base_page import BasePage
from features.utils.tickets_store import load_ticket
import time
import re


class TicketsHistoryPage(BasePage):
    HISTORIAL_TICKETS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Tickets")')

    def __init__(self, driver):
        super().__init__(driver)

    def open_tickets_history(self):
        self.click(self.HISTORIAL_TICKETS)
        time.sleep(2)
        self.driver.swipe(360, 300, 360, 1000, 800)
        time.sleep(3)

    def verify_tickets_history(self):
        saved_ticket = load_ticket()

        if saved_ticket:
            print(f"Ticket guardado: {saved_ticket!r}")
            print(f"Fecha buscada: {saved_ticket['date']!r}")
            print(f"Importe buscado: {saved_ticket['amount']!r}")
            return self.find_ticket(saved_ticket["date"], saved_ticket["amount"])

        latest_date = self.get_latest_tickets_date(timeout=120)

        return latest_date is not None

    def get_latest_tickets_date(self, timeout=120):
        end_time = time.time() + timeout
        latest_date = None

        while time.time() < end_time:
            try:
                source = self.driver.page_source

                for match_es in re.findall(r'\d{2}/\d{2}/\d{4}', source):
                    try:
                        dt = datetime.strptime(match_es, "%d/%m/%Y")

                        if not latest_date or dt > latest_date:
                            latest_date = dt

                    except Exception:
                        pass

                for match_en in re.findall(r'[A-Za-z]{3} \d{1,2}, \d{4}', source):
                    try:
                        dt = datetime.strptime(match_en, "%b %d, %Y")

                        if not latest_date or dt > latest_date:
                            latest_date = dt

                    except Exception:
                        pass

            except Exception:
                pass

            if latest_date:
                return latest_date.strftime("%d/%m/%Y")

            time.sleep(2)

        return None

    def find_ticket(self, expected_date, expected_amount):
        try:
            date_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{expected_date}")'
            )

            amount_locator = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{expected_amount}").instance(0)'
            )

            print(f"Buscando fecha: {expected_date!r}")
            print(f"Buscando importe: {expected_amount!r}")

            date_element = self.esperar_visible(date_locator, timeout=5)

            print(f"Fecha encontrada: {date_element.text!r}")

            amount_element = self.esperar_visible(amount_locator, timeout=5)

            print(f"Importe encontrado: {amount_element.text!r}")

            print("Ticket encontrado correctamente")

            return True

        except Exception as e:
            print(f"No se encontró el ticket: {e}")
            return False
