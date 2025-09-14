import pygame as pg

from .widget import Widget


class Window:
    """
    A window is a container for widgets. It can be fullscreen or a fixed size.
    Inherit from this class to create custom windows.
    """

    def __init__(self, fullscreen: bool = True, rect: pg.Rect = None, visible: bool = True):
        """
        Initialize the window.
        :param fullscreen: If True, the window will take the full size of the application window.
        :param rect: The rectangle defining the position and size of the window. Ignored if fullscreen is True.
        :param visible: If False, the window will not be drawn or receive events.
        """
        self._rect: pg.Rect = rect if rect else pg.Rect(0, 0, 0, 0)
        self._fullscreen = fullscreen
        self.visible = visible
        self.widgets: list[Widget] = []

        self._background_color = (0, 0, 0, 0)
        self._surface = pg.Surface(self.rect.size, pg.SRCALPHA)

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)

    def draw(self, surface: pg.Surface):
        if not self.visible:
            return

        self.draw_window(surface)

        for widget in reversed(self.widgets):
            widget.draw(surface)

    def draw_window(self, surface: pg.Surface):
        self._surface.fill(self._background_color)
        surface.blit(self._surface, self.rect.topleft)

    @property
    def fullscreen(self):
        return self._fullscreen

    def handle_event(self, event: pg.Event) -> bool:
        if not self.visible:
            return False

        for widget in reversed(self.widgets):
            if widget.handle_event(event):
                return True
        return False

    def move(self, pos: tuple[int, int]):
        self._rect.update(pos, self._rect.size)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: pg.Rect):
        self._rect = value
        self._build_surfaces()

    def resize(self, size: tuple[int, int]):
        self._rect.update(self._rect.topleft, size)
        self._build_surfaces()

    def update(self, dt: float):
        pass

    def _build_surfaces(self):
        self._surface = pg.Surface(self.rect.size, pg.SRCALPHA)


class PopupWindow(Window):
    """
    A popup window is a window that is displayed on top of other windows.
    It is usually used for dialogs, menus, etc.
    """

    def __init__(self, rect: pg.Rect, title: str = "", show_caption: bool | None = None, visible: bool = True):
        """
        Initialize the popup window.
        :param rect: The rectangle defining the position and size of the window.
        :param visible: If False, the window will not be drawn or receive events.
        """
        super().__init__(fullscreen=False, rect=rect, visible=visible)

        self.title = title
        self._show_caption = show_caption if show_caption is not None else bool(title)

        self._border_color = (255, 255, 255)
        self._border_width = 1
        self._background_color = (0, 0, 0, 255)
        self._corner_radius = 15
        self._shadow_color = (0, 0, 0, 100)
        self._shadow_offset = (10, 10)
        self._caption_background_color = (200, 200, 200, 255)
        self._caption_text_color = (0, 0, 0, 255)
        self._caption_text_size = 25
        self._caption_font_file = None
        self._caption_font = pg.font.Font(self._caption_font_file, self._caption_text_size)
        self._caption_text_space_needed = self._caption_font.size(self.title)
        self._caption_height = 30

        self._shadow_surf: pg.Surface
        self._build_surfaces()

    def draw_window(self, surface: pg.Surface):
        surface.blit(self._shadow_surf, (self.rect.x + self._shadow_offset[0], self.rect.y + self._shadow_offset[1]))
        surface.blit(self._surface, self.rect.topleft)

    def _build_surfaces(self):
        # Shadow surface
        shadow_width = self.rect.width + abs(self._shadow_offset[0])
        shadow_height = self.rect.height + abs(self._shadow_offset[1])
        self._shadow_surf = pg.Surface((shadow_width, shadow_height), pg.SRCALPHA)
        pg.draw.rect(self._shadow_surf, self._shadow_color,
                     (0, 0, self.rect.width, self.rect.height),
                     border_radius=self._corner_radius)

        # Main surface
        # Caption
        if self._show_caption:
            text_x = self._corner_radius + 5
            text_y = (self._caption_height - self._caption_text_space_needed[1]) // 2 + self._border_width

            pg.draw.rect(self._surface, self._caption_background_color, (0, 0, self.rect.width, self._caption_height),
                         border_top_left_radius=self._corner_radius, border_top_right_radius=self._corner_radius)
            self._surface.blit(self._caption_font.render(self.title, True, self._caption_text_color), (text_x, text_y))

        # Content and border
        content_y_offset = self._caption_height if self._show_caption else 0
        content_height = self.rect.height - content_y_offset
        pg.draw.rect(self._surface, self._background_color, (0, content_y_offset, self.rect.width, content_height),
                     border_top_left_radius=0 if self._show_caption else self._corner_radius,
                     border_top_right_radius=0 if self._show_caption else self._corner_radius,
                     border_bottom_left_radius=self._corner_radius,
                     border_bottom_right_radius=self._corner_radius)
        pg.draw.rect(self._surface, self._border_color, (0, 0, *self.rect.size), self._border_width,
                     border_radius=self._corner_radius)
