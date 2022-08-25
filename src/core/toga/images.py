import pathlib


class Image:
    """
    A representation of graphical content.

    :param path: Path to the image. Allowed values can be local file
        (relative or absolute path) or URL (HTTP or HTTPS). Relative paths
        will be interpreted relative to the application module directory.
    """
    def __init__(self, path):
        if isinstance(path, pathlib.Path):
            self.path = path
        elif path.startswith('http://') or path.startswith('https://'):
            self.path = path
        else:
            self.path = pathlib.Path(path)

        # Resource is late bound.
        self._impl = None

    def bind(self, factory):
        """
        Bind the Image to a factory.

        Creates the underlying platform implemenation of the Image. Raises
        FileNotFoundError if the path is a non-existent local file.

        :param factory: The platform factory to bind to.
        :returns: The platform implementation
        """
        if self._impl is None:
            if isinstance(self.path, pathlib.Path):
                full_path = factory.paths.app / self.path
                if not full_path.exists():
                    raise FileNotFoundError(
                        'Image file {full_path!r} does not exist'.format(
                            full_path=full_path
                        )
                    )
                self._impl = factory.Image(interface=self, path=full_path)
            else:
                self._impl = factory.Image(interface=self, url=self.path)

        return self._impl
