# pysgui  
**Pygame Simple GUI** – An easy to use yet powerful GUI framework for [pygame](https://www.pygame.org/).  

---

## 🎯 Goal  

`pysgui` aims to provide a **simple and intuitive API** to build graphical user interfaces in pygame applications.  
Whether you are prototyping a game menu, designing a HUD, or creating a complete editor inside pygame, `pysgui` gives you the tools to:  

- Create and switch **scenes** (fullscreen windows).  
- Use built-in **popup windows** for menus, dialogs, or overlays.  
- Organize widgets with **flexible layouts**.  
- Style everything with a **powerful theming system** (similar to stylesheets). Several default themes are given. 
- Keep a **main canvas** for your game, while layering UI windows above.  

---

## ✨ Features  

- 🖼 **Windows & Scenes**  
  - Fullscreen windows for menus or game states.  
  - Popup windows with captions, shadows, borders.  
  - Scene switching via the `WindowManager`.
  - If you want a **main canvas for your game**, you can directly draw onto a window’s surface.  
    For deeper customizations, simply inherit from the `Window` class.  

- 🎨 **Theming & Styles**  
  - Style every widget (color, borders, shadows, fonts…).  
  - Central **ThemeStore** for consistent design.  
  - Easy to create custom styles and override defaults.  

- 📐 **Layouts**  
  - Fixed layout for absolute positioning.  
  - Horizontal/Vertical layouts.  
  - Future support for grid and flexible layouts with constraints.  

- 🧩 **Widgets**  
  - Buttons, captions, containers, and more to come.  
  - All widgets are **stylable** via stylesheets.  
  - Consistent API: constraints, rects, and events.  

- 🎮 **Pygame Friendly**  
  - Integrates seamlessly with the pygame event loop.  
  - No external dependencies beyond pygame.  

---

## 🚀 Quick Example  

```python
import pygame as pg
import pysgui as gui

pg.init()
app = gui.Application(size=(800, 600), title="My Game")

# A fullscreen window (scene)
menu = gui.Window(fullscreen=True, rect=app.screen.get_rect())
app.add_window(menu)

# A popup window
popup = gui.PopupWindow(pg.Rect(200, 150, 400, 300), title="Settings")
menu.add_widget(popup)

# A button inside the popup
button = gui.Button("Click me!")
popup.add_widget(button)

app.run()
```

## 📂 Roadmap

- [x] Application & Window management
- [x] Stylesheet and theming system
- [x] Fixed layout
- [ ] Basic Widgets (labels, buttons)
- [ ] Popup Windows with captions, 
- [ ] Horizontal & Vertical layouts
- [ ] Advanced built-in widgets (sliders, text inputs, checkboxes, …)
- [ ] Avanced windows and container (with scrollbars)
- [ ] Add more default themes (complete light theme, add dark theme)
- [ ] Constraint-based layout system

## 🛠 Contributing

This project is still at its beginning and not opened to contribution yet.

