import pygame as pg

from pysgui.widgets import Window


class WindowsManager:
    """
    Manages multiple windows within an application.
    Windows are drawn in order of their z-index, with higher z-index windows drawn on top of lower z-index windows.
    """

    def __init__(self, screen: pg.Surface):
        self._screen = screen
        self._windows: list[tuple[int, Window]] = []

    def add(self, window: Window, z_index: int = -1):
        """
        Add a window to the application.
        :param window: Window instance to be added
        :param z_index: The z-index of the window. Higher values are drawn on top of lower values. (Not implemented yet)
        """
        if window.fullscreen:
            window.rect = self._screen.get_rect()

        if z_index < 0:
            z_index = self.top_z + 1

        self._windows.append((z_index, window))

        self._sort_windows()

    def bring_to_front(self, window: Window):
        """
        Bring a window to the front of the z-order.
        :param window: Window instance to be brought to the front
        """
        if window not in [w for z, w in self._windows]:
            raise ValueError("Window not found in the application.")

        max_z = self.top_z
        for i, (z, w) in enumerate(self._windows):
            if w == window:
                self._windows[i] = (max_z + 1, w)
                break

        self._sort_windows()

    def draw(self):
        """
        Draw all windows to the screen.
        """
        top_fs_index = 0
        for i, (z, window) in enumerate(reversed(self._windows)):
            if window.fullscreen and window.visible:
                top_fs_index = len(self._windows) - 1 - i
                break

        for z, window in self._windows[top_fs_index:]:
            window.draw(self._screen)

    def handle_event(self, event: pg.Event) -> bool:
        """
        Handle an event for all windows.
        :param event: Pygame event to be handled
        :return: True if the event was handled by any window, False otherwise
        """
        if event.type == pg.VIDEORESIZE:
            for z, window in self._windows:
                if window.fullscreen:
                    window.rect = self._screen.get_rect()

        for z, window in reversed(self._windows):
            if window.handle_event(event):
                return True
        return False

    def remove(self, window: Window):
        """
        Remove a window from the application.
        :param window: Window instance to be removed
        """
        self._windows = [(z, w) for (z, w) in self._windows if w != window]

    @property
    def screen(self):
        return self._screen

    def top_window(self, only_visible: bool = True) -> Window | None:
        """
        Get the topmost window.
        :param only_visible: If True, only consider visible windows.
        :return: The topmost window or None if there are no windows.
        """
        for z, window in reversed(self._windows):
            if window.visible or not only_visible:
                return window
        return None

    @property
    def top_z(self):
        return self._windows[-1][0] if self._windows else 0

    def update(self, dt: float):
        """
        Update all windows.
        :param dt: Delta time since last update, in seconds.
        :return:
        """
        pass

    @property
    def windows(self):
        return self._windows

    def _sort_windows(self):
        """
        Sort windows by their z-index, then by their order of addition.
        :return:
        """
        self._windows.sort(key=lambda item: item[0])
