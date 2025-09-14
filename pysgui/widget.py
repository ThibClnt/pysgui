import pygame as pg


class Widget:

    def draw(self, surface):
        pass

    def handle_event(self, event: pg.Event) -> bool:
        return False
