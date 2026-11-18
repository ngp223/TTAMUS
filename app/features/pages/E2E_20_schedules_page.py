from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from features.pages.base_page import BasePage
from features.config.test_config import SHIFT_EMPLOYEE


class SchedulesPage(BasePage):
    MENU = BasePage.by_text("Horarios")
    ADD_SHIFT = BasePage.by_text("Añadir turno")
    EMPLOYEE = BasePage.by_id("shift-edit-employee")
    START = BasePage.by_id("shift-edit-start")
    END = BasePage.by_id("shift-edit-end")
    SAVE = BasePage.by_id("shift-edit-save")
    DELETE = BasePage.by_id("shift-edit-delete")
    CONFIRM_DELETE = BasePage.by_id("confirm-modal-accept")
    EMPLOYEE_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceIdMatches(".*shift-edit-employee-opt.*").text("{SHIFT_EMPLOYEE}")')
    PICKER_PANEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-time-picker__panel.*")')
    PICKER_BACKDROP = (AppiumBy.XPATH, '(//*[contains(@resource-id,"cdk-overlay-backdrop")])[last()]')
    CHIPS = f'//*[contains(@resource-id,"tam-shift-calendar")]//*[@text="{SHIFT_EMPLOYEE[0]}"]'
    HOUR_CELL = 'new UiSelector().resourceIdMatches(".*column-1.*tam-time-picker__cell.*").text("{}")'
    HOUR_LIST = 'new UiSelector().resourceIdMatches(".*column-1.*tam-time-picker__list.*")'
    START_HOUR, END_HOUR, NEW_END_HOUR = "16", "22", "23"

    def __init__(self, driver):
        super().__init__(driver)
        self.count_before = 0
        self.positions_before = set()
        self.shift_pos = None

    def _chips(self):
        return self.driver.find_elements(AppiumBy.XPATH, self.CHIPS)

    def _pick_time(self, button, hour):
        self.click(button)
        cell = (AppiumBy.ANDROID_UIAUTOMATOR, self.HOUR_CELL.format(hour))
        if not self.exists(cell, timeout=2):
            try:
                self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable({self.HOUR_LIST}).scrollIntoView({self.HOUR_CELL.format(hour)})')
            except Exception:
                pass
        self.click(cell)
        if self.exists(self.PICKER_PANEL, timeout=1):
            self.click(self.PICKER_BACKDROP)

    def _open_shift(self):
        x, y = self.shift_pos
        chip = min(self._chips(), key=lambda c: (abs(c.rect["x"] - x), abs(c.rect["y"] - y)))
        self.shift_pos = (chip.rect["x"], chip.rect["y"])
        chip.click()

    def _save(self):
        self.click(self.SAVE)
        self.wait_invisibility(self.EMPLOYEE)

    def access_schedules(self):
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
        self._pick_time(self.START, self.START_HOUR)
        self._pick_time(self.END, self.END_HOUR)
        self._save()

    def check_shift_created(self):
        WebDriverWait(self.driver, 15).until(lambda d: len(self._chips()) == self.count_before + 1)
        new = [c for c in self._chips() if (c.rect["x"], c.rect["y"]) not in self.positions_before]
        if not new:
            raise Exception("No se ha podido identificar el turno creado en el calendario")
        self.shift_pos = (new[0].rect["x"], new[0].rect["y"])

    def modify_shift(self):
        self._open_shift()
        self._pick_time(self.END, self.NEW_END_HOUR)
        self._save()

    def check_shift_modified(self):
        self._open_shift()
        end = self.wait_visibility(self.END)
        value = end.text or end.get_attribute("content-desc") or ""
        if self.NEW_END_HOUR not in value:
            raise Exception(f"Hora de fin esperada {self.NEW_END_HOUR}, encontrada: {value!r}")

    def delete_shift(self):
        self.click(self.DELETE)
        self.click(self.CONFIRM_DELETE)

    def check_shift_deleted(self):
        WebDriverWait(self.driver, 15).until(lambda d: len(self._chips()) == self.count_before)