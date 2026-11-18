
from datetime import datetime, timedelta
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from features.pages.base_page import BasePage
from features.config.test_config import SHIFT_EMPLOYEE, WEBVIEW_CONTEXT

DAY_OFFSET = 1
START_TIME = ("04", "00")
END_TIME = ("22", "30")
NEW_START_TIME = ("14", "30")


class SchedulesPage(BasePage):
    MENU = BasePage.by_text("Horarios")
    ADD_SHIFT = BasePage.by_text("Añadir turno")
    EMPLOYEE = BasePage.by_id("shift-edit-employee")
    DAY = BasePage.by_id("shift-edit-day")
    START = BasePage.by_id("shift-edit-start")
    END = BasePage.by_id("shift-edit-end")
    SAVE = BasePage.by_id("shift-edit-save")
    DELETE = BasePage.by_id("shift-edit-delete")
    CONFIRM_DELETE = BasePage.by_id("confirm-modal-accept")
    EMPLOYEE_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceIdMatches(".*shift-edit-employee-opt.*").text("{SHIFT_EMPLOYEE}")')
    DIALOG = (AppiumBy.XPATH, '//*[contains(@resource-id,"cdk-dialog-")]')
    PICKER_PANEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-time-picker__panel.*")')
    DATE_PANEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-date-picker__panel.*")')
    PICKER_BACKDROP = (AppiumBy.XPATH, '(//*[contains(@resource-id,"cdk-overlay-backdrop")])[last()]')
    DAY_CELL = 'new UiSelector().resourceIdMatches(".*tam-date-picker__day-{}$")'
    SHIFT_CELL = (AppiumBy.XPATH, '//*[contains(@resource-id,"div-cal__cell-{}-button-person") and contains(@content-desc,"{}")]')

    PICK_JS = """
        const panels = document.querySelectorAll('.tam-time-picker__panel');
        const panel = panels[panels.length - 1];
        if (!panel) return 'sin panel';
        const col = panel.querySelectorAll('.tam-time-picker__column')[arguments[0]];
        if (!col) return 'sin columna';
        const cell = [...col.querySelectorAll('.tam-time-picker__cell')].find(c => c.textContent.trim() === arguments[1]);
        if (!cell) return 'sin celda';
        cell.scrollIntoView({block: 'center'});
        cell.click();
        return 'ok';
    """

    PANEL_HTML_JS = """
        const p = document.querySelectorAll('.tam-time-picker__panel');
        return p.length ? p[p.length - 1].outerHTML.slice(0, 1500) : 'sin panel';
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.shift_day = None

    def _calendar_shift(self):
        return self.driver.find_elements(self.SHIFT_CELL[0], self.SHIFT_CELL[1].format(self.shift_day, SHIFT_EMPLOYEE))

    def _close_overlays(self):
        for _ in range(4):
            if not self.exists(self.DIALOG, timeout=1):
                return
            self.driver.back()

    def _debug_dump(self, name):
        self.driver.save_screenshot(f"{name}.png")
        with open(f"{name}.xml", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

    def _open_panel(self, button, panel):
        self.click(button)
        if not self.exists(panel, timeout=5):
            self._debug_dump("debug_picker")
            raise Exception(f"El selector no se abre al pulsar {button[1]}")

    def _close_panel(self, panel):
        try:
            self.wait_invisibility(panel, 3)
        except TimeoutException:
            backdrops = self.driver.find_elements(*self.PICKER_BACKDROP)
            if backdrops:
                backdrops[0].click()
            if self.exists(panel, timeout=2):
                self.driver.back()

    def _pick_cell(self, column, text):
        self.driver.switch_to.context(WEBVIEW_CONTEXT)
        try:
            result = self.driver.execute_script(self.PICK_JS, column, text)
            if result != "ok":
                html = self.driver.execute_script(self.PANEL_HTML_JS)
                raise Exception(f"No se pudo elegir {text} en la columna {column + 1}: {result}\n{html}")
        finally:
            self.driver.switch_to.context("NATIVE_APP")

    def _pick_day(self):
        today = datetime.now().date()
        target = today + timedelta(days=DAY_OFFSET)
        self.shift_day = target.day
        first = today.replace(day=1)
        number = first.weekday() + (target - first).days + 1
        if not 1 <= number <= 42:
            raise Exception(f"El día {target} queda fuera del calendario mostrado")
        self._open_panel(self.DAY, self.DATE_PANEL)
        self.click((AppiumBy.ANDROID_UIAUTOMATOR, self.DAY_CELL.format(number)))
        self._close_panel(self.DATE_PANEL)
        el = self.wait_visibility(self.DAY)
        print(f"Día {target} -> campo: text={el.text!r} desc={el.get_attribute('content-desc')!r}")

    def _pick_time(self, button, time):
        self._open_panel(button, self.PICKER_PANEL)
        self._pick_cell(0, time[0])
        if not self.exists(self.PICKER_PANEL, timeout=1):
            self._open_panel(button, self.PICKER_PANEL)
        self._pick_cell(1, time[1])
        self._close_panel(self.PICKER_PANEL)
        el = self.wait_visibility(button)
        print(f"Hora {':'.join(time)} -> botón: text={el.text!r} desc={el.get_attribute('content-desc')!r}")

    def _save(self):
        self.click(self.SAVE)
        self.wait_invisibility(self.EMPLOYEE)

    def access_schedules(self):
        self._close_overlays()
        self.scroll_text("Horarios")
        self.click(self.MENU)
        self.wait_clickable(self.ADD_SHIFT)

    def create_shift(self):
        self.click(self.ADD_SHIFT)
        self.click(self.EMPLOYEE)
        self.click(self.EMPLOYEE_OPTION)
        self._pick_day()
        self._pick_time(self.START, START_TIME)
        self._pick_time(self.END, END_TIME)
        self._save()

    def check_shift_created(self):
        WebDriverWait(self.driver, 15).until(lambda d: self._calendar_shift())
        print(f"Turno creado correctamente: aparece a las {START_TIME[0]}:{START_TIME[1]}")

    def modify_shift(self):
        shift = WebDriverWait(self.driver, 15).until(lambda d: self._calendar_shift())
        shift[0].click()
        self._pick_time(self.START, NEW_START_TIME)
        self._save()

    def check_shift_modified(self):
        shift = WebDriverWait(self.driver, 15).until(lambda d: self._calendar_shift())
        shift[0].click()
        start = self.wait_visibility(self.START)
        value = start.text or start.get_attribute("content-desc") or ""
        expected = f"{NEW_START_TIME[0]}:{NEW_START_TIME[1]}"
        if expected not in value:
            raise Exception(f"Hora de inicio esperada {expected}, encontrada: {value!r}")
        print(f"Turno modificado correctamente: el inicio es {value!r}")
        self.driver.back()

    def delete_shift(self):
        shift = WebDriverWait(self.driver, 15).until(lambda d: self._calendar_shift())
        shift[0].click()
        self.wait_clickable(self.DELETE)
        self.click(self.DELETE)
        self.wait_clickable(self.CONFIRM_DELETE)
        self.click(self.CONFIRM_DELETE)
        self.wait_invisibility(self.EMPLOYEE)

    def check_shift_deleted(self):
        WebDriverWait(self.driver, 15).until(lambda d: not self._calendar_shift())
        print(f"Turno eliminado correctamente: ya no aparece a las {NEW_START_TIME[0]}:{NEW_START_TIME[1]}")
