import win32gui


class WindowList:
    def __init__(self):
        self.titles = []
        self.descriptors = []

    def get_window_rect(self, hwnd):
        x, y, w, h = win32gui.GetWindowRect(hwnd)
        return (x, y), (w, h)

    def update(self):
        self.clear()
        win32gui.EnumWindows(self.enum_window_clb, [])

    def clear(self):
        self.titles.clear()
        self.descriptors.clear()

    def add_window(self, title, descriptor):
        self.titles.append(title)
        self.descriptors.append(descriptor)

    def at(self, index: int):
        return self.titles[index], self.descriptors[index]

    def get_index(self, title):
        if title in self.titles:
            return self.titles.index(title)

    def enum_window_clb(self, hwnd, *args):
        (x, y), (w, h) = self.get_window_rect(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowVisible(hwnd) and (w - x, h - y) != (0, 0) and title:
            self.add_window(title, hwnd)
            # print(f"Window: {title}")
            # print(f"\tLocation: ({x}, {y})")
            # print(f"\t    Size: ({w}, {h})")
