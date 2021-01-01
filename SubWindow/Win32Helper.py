import win32gui


class WindowList:
    def __init__(self):
        self.titles = []
        self.descriptors = []

    def at(self, value):
        if isinstance(value, str):
            value = self._get_index(value)
        return self.titles[value], self.descriptors[value]

    def get_window_rect(self, title):
        self._update()
        title, hwnd = self.at(title)
        x, y, w, h = win32gui.GetWindowRect(hwnd)
        return (x, y), (w, h)

    def _update(self):
        self._clear()
        win32gui.EnumWindows(self._enum_window_clb, [])

    def _clear(self):
        self.titles.clear()
        self.descriptors.clear()

    def _add_window(self, title, descriptor):
        self.titles.append(title)
        self.descriptors.append(descriptor)

    def _get_index(self, title):
        if title in self.titles:
            return self.titles.index(title)

    def _enum_window_clb(self, hwnd, *args):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowVisible(hwnd) and title:
            self._add_window(title, hwnd)
            # print(f"Window: {title}")
            # print(f"\tLocation: ({x}, {y})")
            # print(f"\t    Size: ({w}, {h})")
