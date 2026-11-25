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
    ADD_SHIFT = BasePage.by_text("Añadir turno")
    EMPLOYEE = BasePage.by_id("shift-edit-employee")
    DAY = BasePage.by_id("shift-edit-day")
    START = BasePage.by_id("shift-edit-start")
    END = BasePage.by_id("shift-edit-end")
    SAVE = BasePage.by_id("shift-edit-save")
    DELETE = BasePage.by_id("shift-edit-delete")
    EMPLOYEE_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceIdMatches(".*shift-edit-employee-opt.*").text("{SHIFT_EMPLOYEE}")')
    DIALOG = (AppiumBy.XPATH, '//*[contains(@resource-id,"cdk-dialog-")]')
    PICKER_PANEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-time-picker__panel.*")')
    DATE_PANEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-date-picker__panel.*")')
    PICKER_BACKDROP = (AppiumBy.XPATH, '(//*[contains(@resource-id,"cdk-overlay-backdrop")])[last()]')
    DAY_CELL = 'new UiSelector().resourceIdMatches(".*tam-date-picker__day-{}$")'
    SHIFT = '(//*[contains(@resource-id,"span-cal__employee") and contains(@text,"{}")]/..//*[contains(@resource-id,"button-chip") and contains(@text,"{}:{}–")] | //*[contains(@resource-id,"button-person") and contains(@content-desc,"{} · {}:{}")])'
    ANY_SHIFT = '(//*[contains(@resource-id,"span-cal__employee") and contains(@text,"{}")]/..//*[contains(@resource-id,"button-chip")] | //*[contains(@resource-id,"button-person") and contains(@content-desc,"{} ·")])'
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

    def _shifts(self, time):
        return self.driver.find_elements(AppiumBy.XPATH, self.SHIFT.format(SHIFT_EMPLOYEE, time[0], time[1], SHIFT_EMPLOYEE, time[0], time[1]))

    def _all_shifts(self):
        return self.driver.find_elements(AppiumBy.XPATH, self.ANY_SHIFT.format(SHIFT_EMPLOYEE, SHIFT_EMPLOYEE))

    def _first_shift(self, time):
        return WebDriverWait(self.driver, 20).until(lambda d: self._shifts(time))[0]

    def _delete_shift(self, shift):
        shift.click()
        self.confirm_delete(self.DELETE, self.EMPLOYEE)

    def _clear_shifts(self):
        shifts = self._all_shifts()
        while shifts:
            count = len(shifts)
            self._delete_shift(shifts[0])
            WebDriverWait(self.driver, 20).until(lambda d: len(self._all_shifts()) < count)
            shifts = self._all_shifts()

    def _close_overlays(self):
        for _ in range(4):
            if not self.exists(self.DIALOG, timeout=1):
                return
            self.driver.back()

    def _open_panel(self, button, panel):
        self.click(button)
        if not self.exists(panel, timeout=5):
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
                raise Exception(f"No se pudo elegir {text} en la columna {column + 1}: {result}")
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

    def _pick_time(self, button, time):
        self._open_panel(button, self.PICKER_PANEL)
        self._pick_cell(0, time[0])
        if not self.exists(self.PICKER_PANEL, timeout=1):
            self._open_panel(button, self.PICKER_PANEL)
        self._pick_cell(1, time[1])
        self._close_panel(self.PICKER_PANEL)

    def access_schedules(self):
        self._close_overlays()
        self.open_menu("Horarios")
        self.wait_clickable(self.ADD_SHIFT)

    def create_shift(self):
        self._clear_shifts()
        self.click(self.ADD_SHIFT)
        self.click(self.EMPLOYEE)
        self.click(self.EMPLOYEE_OPTION)
        self._pick_day()
        self._pick_time(self.START, START_TIME)
        self._pick_time(self.END, END_TIME)
        self.click_and_wait_gone(self.SAVE, self.EMPLOYEE)

    def check_shift_created(self):
        self._first_shift(START_TIME)

    def modify_shift(self):
        self._first_shift(START_TIME).click()
        self._pick_time(self.START, NEW_START_TIME)
        self.click_and_wait_gone(self.SAVE, self.EMPLOYEE)

    def check_shift_modified(self):
        self._first_shift(NEW_START_TIME)
        WebDriverWait(self.driver, 20).until(lambda d: not self._shifts(START_TIME))

    def delete_shift(self):
        self._delete_shift(self._first_shift(NEW_START_TIME))

    def check_shift_deleted(self):
        WebDriverWait(self.driver, 20).until(lambda d: not self._shifts(NEW_START_TIME))