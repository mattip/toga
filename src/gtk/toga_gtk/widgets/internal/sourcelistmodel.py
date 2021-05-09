from toga_gtk.libs import Gio


class SourceListModel(Gio.ListStore):
    """
    The rows inherit from .internal.rows.ScrollableRow which inherits from Gtk.ListBoxRow, 
    they are kept inside a Gio.ListStore.
    toga.sources.ListSource is converted to Gtk.ListBoxRow in self.change_source.
    """
    def __init__(self, row_class, icon_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_class = row_class
        self.icon_factory = icon_factory
        self._parent_list = None
        self._on_select = None

    def _bind_function(self, item):
        return item

    def bind_to_list(self, parent_list):
        self._parent_list = parent_list
        parent_list.bind_model(self, self._bind_function)

    def set_on_select(self, on_select: callable):
        self._on_select = on_select
        self._on_select_handler = self._parent_list.connect("row-selected", self._on_row_selected)

    def destroy(self, *args, **kwargs):
        self._parent_list.dsconnect(self._on_select_handler)
        super().destroy(*args, **kwargs)

    def change_source(self, source: 'ListSource'):
        # Gtk.ListBox.bind_model() requires a function to convert the objects in the store
        # to presentation objects. But the objects in the store are already what we want.
        # Thus the identity function.
        # ListStore only accepts GObjects so we can't put toga.sources.Row in it.
        super().remove_all()
        for row in source:
            self.append(
                self.row_class(row, self.icon_factory))

    def insert(self, index: int, item: 'Row'):
        new_item = self.row_class(item, self.icon_factory)
        super().insert(index, new_item)

    def change(self, item: 'Row'):
        new_item = self.row_class(item, self)
        index = self._find(item)
        super().insert(index, new_item)

    def remove(self, item: 'Row', index: int):
        if index is None:
            index = self._find(item)
        super().remove(index)

    def scroll_to_row(self, index: int):
        row = self[index]
        row.scroll_to_center()

    def get_selection(self):
        row = self._parent_list.get_selected_row()
        if row is None:
            return row
        else:
            return row.interface

    def _on_row_selected(self, widget: 'GObject', item: 'ListBoxRow'):
        if item is not None and self._on_select is not None:
            self._on_select(item.interface)

    def _find(self, item: 'Row') -> int:
        found, index = self.store.find_with_equal_func(
            item,
            lambda a, b: a == b.interface
        )

        if not found:
            return -1
        else:
            return index

