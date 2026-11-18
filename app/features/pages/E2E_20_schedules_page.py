from datetime import datetime, timedelta
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from features.pages.base_page import BasePage
from features.config.test_config import SHIFT_EMPLOYEE, WEBVIEW_CONTEXT

DAY_OFFSET = 1
START_TIME = ("04", "00")
END_TIME = ("23", "30")
NEW_START_TIME = ("14",)


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
    CHIPS = f'//*[contains(@resource-id,"tam-shift-calendar")]//*[@text="{SHIFT_EMPLOYEE[0]}"]'
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
        self.count_before = 0
        self.positions_before = set()
        self.shift_pos = None

    def _chips(self):
        return self.driver.find_elements(AppiumBy.XPATH, self.CHIPS)

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
        for column, text in enumerate(time):
            self._pick_cell(column, text)
        self._close_panel(self.PICKER_PANEL)
        el = self.wait_visibility(button)
        print(f"Hora {':'.join(time)} -> botón: text={el.text!r} desc={el.get_attribute('content-desc')!r}")

    def _find_new_shift(self):
        WebDriverWait(self.driver, 15).until(lambda d: len(self._chips()) == self.count_before + 1)
        new = [c for c in self._chips() if (c.rect["x"], c.rect["y"]) not in self.positions_before]
        if not new:
            raise Exception("No se ha podido identificar el turno en el calendario")
        self.shift_pos = (new[0].rect["x"], new[0].rect["y"])

    def _open_shift(self):
        x, y = self.shift_pos
        min(self._chips(), key=lambda c: (abs(c.rect["x"] - x), abs(c.rect["y"] - y))).click()

    def _save(self):
        self.click(self.SAVE)
        self.wait_invisibility(self.EMPLOYEE)

    def access_schedules(self):
        self._close_overlays()
        self.scroll_text("Horarios")
        self.click(self.MENU)
        self.wait_clickable(self.ADD_SHIFT)

    def create_shift(self):
        chips = self._chips()
        self.count_before = len(chips)
        self.positions_before = {(c.rect["x"], c.rect["y"]) for c in chips}
        self.click(self.ADD_SHIFT)
        self.click(self.EMPLOYEE)
        self.click(self.EMPLOYEE_OPTION)
        self._pick_day()
        self._pick_time(self.START, START_TIME)
        self._pick_time(self.END, END_TIME)
        self._save()

    def check_shift_created(self):
        self._find_new_shift()

    def modify_shift(self):
        self._open_shift()
        self._pick_time(self.START, NEW_START_TIME)
        self._save()
        self._find_new_shift()

    def check_shift_modified(self):
        self._open_shift()
        start = self.wait_visibility(self.START)
        value = start.text or start.get_attribute("content-desc") or ""
        if NEW_START_TIME[0] not in value:
            raise Exception(f"Hora de inicio esperada {NEW_START_TIME[0]}, encontrada: {value!r}")

    def delete_shift(self):
        self.click(self.DELETE)
        self.click(self.CONFIRM_DELETE)

    def check_shift_deleted(self):
        WebDriverWait(self.driver, 15).until(lambda d: len(self._chips()) == self.count_before)