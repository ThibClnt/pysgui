import pygame as pg
from typing import final

from .windows_manager import WindowsManager
from pysgui.util import SingletonMeta
from pysgui.styling import ThemeStore
from pysgui.widgets import Window


@final
class Application(metaclass=SingletonMeta):
    """
    Main class for the application.
    The application is responsible for running the main loop, handling events and updating the windows.
    This class can not be inherited. In order to add custom behavior, inherit the Window class instead.
    Only one instance of this class should be created.
    """
    __instance = None

    def __init__(self, title: str = "Application", size: tuple[int, int] = (800, 600), fps: int = 60, flags: int = 0, no_root : bool = False):
        """
        Create a new application instance.
        :param title: Title of the application window
        :param size: Size of the application window (width, height)
        :param fps: Maximum framerate of the application
        :param flags: Flags for the application window. Use pygame display flags.
        """

        pg.init()
        ThemeStore.load_default_themes()

        self._title = title
        self._size = size
        self.fps = fps
        self._flags = flags

        self._screen = pg.display.set_mode(size, flags)
        pg.display.set_caption(title)

        self._clock = pg.time.Clock()

        self._windows_manager: WindowsManager = WindowsManager(self._screen)

        if not no_root:
            self._windows_manager.add(Window(fullscreen=True), z_index=0)

        self.running = False

    def add_window(self, window: Window, z_index: int = -1) -> Window:
        """
        Add a window to the application.
        :param window: Window instance to be added
        :param z_index: The z-index of the window. Higher values are drawn on top of lower values. (Not implemented yet)
        :return: The id of the added window.
        """
        self._windows_manager.add(window, z_index)
        return window

    def quit(self):
        """
        Quit the application.
        :return:
        """
        self.running = False
        pg.quit()

    def run(self):
        """
        Launch the main loop of the application.
        Stop the loop by calling Application.quit().
        :return:
        """
        self.running = True

        while self.running:
            dt = self._clock.tick(self.fps) / 1000.0

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quit()
                    return
                self._windows_manager.handle_event(event)

            self._windows_manager.update(dt)
            self._windows_manager.draw()
            pg.display.flip()

    @property
    def screen(self) -> pg.Surface:
        return self._screen

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        pg.display.set_caption(value)

    @property
    def windows_manager(self):
        return self._windows_manager
