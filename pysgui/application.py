import pygame as pg
from typing import final

from .window import Window


@final
class Application:
    """
    Main class for the application.
    The application is responsible for running the main loop, handling events and updating the windows.
    This class can not be inherited. In order to add custom behavior, inherit the Window class instead.
    Only one instance of this class should be created.
    """

    def __init__(self, title: str = "Application", size: tuple[int, int] = (800, 600), fps: int = 60, flags: int = 0):
        """
        Create a new application instance.
        :param title: Title of the application window
        :param size: Size of the application window (width, height)
        :param fps: Maximum framerate of the application
        :param flags: Flags for the application window. Use pygame display flags.
        """
        pg.init()

        self._title = title
        self._size = size
        self.fps = fps
        self._flags = flags

        self._screen = pg.display.set_mode(size, flags)
        pg.display.set_caption(title)

        self._clock = pg.time.Clock()

        self._windows: list[Window] = []

        self.running = False

    def add_window(self, window: Window):
        """
        Add a window to the application.
        :param window: Window instance to be added
        :return:
        """
        self._windows.append(window)

        if window.fullscreen or window.rect.size == (0, 0):
            window.resize(self._screen.get_rect())

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

                if event.type == pg.VIDEORESIZE:
                    self._size = event.size
                    self._screen = pg.display.set_mode(self._size, self._flags)
                    for window in self._windows:
                        if window.fullscreen:
                            window.resize(self._screen.get_rect())

            for window in self._windows:
                window.handle_events(events)
                window.update(dt)

            self._screen.fill((0, 0, 0))
            for window in self._windows:
                if window.visible:
                    window.draw(self._screen)

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
