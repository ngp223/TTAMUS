class MobileUtils:

    def __init__(self, driver):
        self.driver = driver

    def swipe_up(self, element=None):
        if element:
            location = element.location
            size = element.size
            start_x = location["x"] + size["width"] / 2
            start_y = location["y"] + size["height"] / 2
            end_x = start_x
            end_y = start_y - 500
            self.driver.swipe(start_x, start_y, end_x, end_y, 800)
        else:
            size = self.driver.get_window_size()
            start_x = size["width"] / 2
            start_y = size["height"] * 0.8
            end_x = start_x
            end_y = size["height"] * 0.3
            self.driver.swipe(start_x, start_y, end_x, end_y, 800)

    def swipe_down(self):
        size = self.driver.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.3
        end_x = start_x
        end_y = size["height"] * 0.8
        self.driver.swipe(start_x, start_y, end_x, end_y, 800)
