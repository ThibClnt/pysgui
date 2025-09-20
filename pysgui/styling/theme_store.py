import json

from .style import Style
from .theme import Theme


class ThemeStore:
    __store: dict[str, Theme] = {}
    __current: Theme

    @staticmethod
    def add(theme: Theme) -> Theme:
        """
        Add a new theme.
        :param theme: Theme object to add
        :return: The new theme object
        """
        ThemeStore.__store[theme.name] = theme
        return theme

    @staticmethod
    def current() -> Theme:
        """
        Get the current theme.
        :return: The current theme
        """
        return ThemeStore.__current

    @staticmethod
    def get_current_name() -> str:
        """
        Get the name of the current theme.
        :return: Name of the current theme
        """
        return ThemeStore.__current.name

    @staticmethod
    def get(name: str, default: Theme = None) -> Theme:
        """
        Get a theme by name. If no name is provided, return the current theme.
        :param name: Name of the theme
        :param default: Default value to return if the theme is not found
        :return: Theme object
        :raises KeyError: If the theme is not found and no default value is provided
        """
        if default is None and name not in ThemeStore.__store:
            raise KeyError(f"Theme '{name}' not found.")

        return ThemeStore.__store.get(name, default)

    @staticmethod
    def get_theme_names() -> list[str]:
        """
        Get the names of all available themes.
        :return: List of theme names
        """
        return list(ThemeStore.__store.keys())

    @staticmethod
    def load_default_themes() -> None:
        """
        Load the default themes.
        """
        default_theme = ThemeStore.load_theme("assets/themes/light.json")
        ThemeStore.__current = ThemeStore.get(default_theme.name)

    @staticmethod
    def load_theme(path: str) -> Theme:
        """
        Load a theme from a file.
        :param path: Path to the theme file
        :return: The loaded theme
        """

        def resolve_variable(value):
            """Resolve if the value is a variable."""
            if isinstance(value, str) and value.startswith("$"):
                var_name = value[1:]
                if var_name not in variables:
                    raise ValueError(f"Variable '{var_name}' not found in theme variables.")
                return variables[var_name]
            return value

        with open(path) as file:
            data = json.load(file)

        try:
            theme_name = data["name"]
            root_name = data.get("root", None)
            variables: dict = data.get("variables", dict())

            json_styles = data["styles"]
        except (KeyError, TypeError) as e:
            raise TypeError("Invalid theme file. A theme must have a name and one or several styles.") from e

        if root_name is not None and root_name not in json_styles:
            raise ValueError(f"Root style '{root_name}' not found in theme styles.")

        cache: dict[str, Style] = {}

        def resolve_style(name: str) -> Style:
            """Resolve a style by name, using cache to avoid re-computation."""
            if name in cache:
                return cache[name]

            resolved_style = {key: resolve_variable(value) for key, value in json_styles[name].items()}

            if '>' in name:
                parent_name = '>'.join(name.split('>')[:-1])
            elif name != root_name:
                parent_name = root_name
            else:
                parent_name = None

            if parent_name:
                if parent_name not in json_styles and parent_name not in cache:
                    raise ValueError(f"Parent style '{parent_name}' not found for style '{name}'.")
                parent_style = resolve_style(parent_name)
                merged = {**parent_style.__dict__, **resolved_style}
            else:
                merged = resolved_style

            style = Style(**merged)
            cache[name] = style
            return style

        styles = {name: resolve_style(name) for name in json_styles.keys()}

        return ThemeStore.add(Theme(theme_name, styles, variables, root_name))

    @staticmethod
    def remove(name: str) -> None:
        """
        Remove a theme.
        :param name: Name of the theme to remove
        :raises KeyError: If the theme is not found
        """
        del ThemeStore.__store[name]

    @staticmethod
    def use(name: str) -> None:
        """
        Set the current theme by name.
        :param name: Name of the theme to set as current
        :raises KeyError: If the theme is not found
        """
        ThemeStore.__current = ThemeStore.get(name)
