from .utils import LoggedObject, not_required, not_required_on


@not_required
class Container:
    def __init__(self, content=None):
        self.baseline_dpi = 96
        self.dpi = 96

        # Prime the underlying storage before using setter
        self._content = None
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content:
            self._content.container = None

        self._content = value
        if value:
            value.container = self

    @property
    def width(self):
        return self.content.get_size()[0]

    @property
    def height(self):
        return self.content.get_size()[1]

    def refreshed(self):
        if self.content:
            self.content.refresh()


class Window(LoggedObject):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self.interface = interface
        self.container = Container()

        self.set_title(title)
        self.set_position(position)
        self.set_size(size)

    def create_toolbar(self):
        self._action("create toolbar")

    # Some platforms inherit this method from a base class.
    @not_required_on("android", "winforms")
    def clear_content(self):
        try:
            widget = self._get_value("content")
            widget.container = self.container
        except AttributeError:
            pass
        self._action("clear content")

    # Some platforms inherit this method from a base class.
    @not_required_on("android", "winforms")
    def set_content(self, widget):
        self.container.content = widget
        self._action("set content", widget=widget)
        self._set_value("content", widget)

    def get_title(self):
        return self._get_value("title")

    def set_title(self, title):
        self._set_value("title", title)

    def get_position(self):
        return self._get_value("position")

    def set_position(self, position):
        self._set_value("position", position)

    def get_size(self):
        return self._get_value("size", (640, 480))

    def set_size(self, size):
        self._set_value("size", size)

    def set_app(self, app):
        self._set_value("app", app)

    def show(self):
        self._action("show")
        self._set_value("visible", True)

    def hide(self):
        self._action("hide")
        self._set_value("visible", False)

    def get_visible(self):
        return self._get_value("visible")

    def close(self):
        self._action("close")

    @not_required_on("mobile")
    def set_full_screen(self, is_full_screen):
        self._set_value("is_full_screen", is_full_screen)

    @not_required
    def toga_on_close(self):
        self._action("handle Window on_close")
