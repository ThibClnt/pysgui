from .style import Style


class Theme:

    def __init__(self, name: str, styles: dict[str, Style] = None, variables: dict = None, root_stylename: str = None):
        self.__name: str = name
        self.__styles: dict[str, Style] = styles or {}
        self.__variables: dict = variables or {}
        self.__root_stylename = root_stylename

    def get(self, name: str, default: Style | None = None) -> Style:
        """
        Get a style by name.
        :param name: Name of the style
        :param default: Default value to return if the style is not found
        :return: Style object
        """
        return self.__styles.get(name, default or self.__styles.get(self.__root_stylename))

    def get_variable(self, name: str, default=None):
        """
        Get a variable by name.
        :param name: Name of the variable
        :param default: Default value to return if the variable is not found
        :return: Variable value
        """
        return self.__variables.get(name, default)

    @property
    def name(self) -> str:
        return self.__name

    def set_style(self, name: str, style: Style) -> None:
        """
        Set a style by name.
        :param name: Name of the style
        :param style: Style object
        """
        self.styles[name] = style

    def set_variable(self, name: str, value) -> None:
        """
        Set a variable by name.
        :param name: Name of the variable
        :param value: Variable value
        """
        self.variables[name] = value

    @property
    def styles(self):
        return self.__styles

    @property
    def style_names(self):
        return list(self.__styles.keys())

    @property
    def variables(self):
        return self.__variables

    @property
    def variable_names(self):
        return list(self.__variables.keys())
