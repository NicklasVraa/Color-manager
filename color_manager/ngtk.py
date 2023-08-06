# Desc: A collection of customized GTK widgets for easier GUI creation.
# Auth: Nicklas Vraa

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os

class Page(Gtk.Box):
    """A page widget for the Gtk.Notebook class."""
    def __init__(self, notebook, header, spacing=10):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
        self.set_border_width(spacing)
        notebook.append_page(self, Gtk.Label(label=header, hexpand=True))

class Label(Gtk.Label):
    """A label with sensible defaults settings."""
    def __init__(self, text, y=0):
        super().__init__()
        self.set_markup(text)
        self.set_alignment(0,y)
        self.set_line_wrap(True)

class Files(Gtk.Box):
    """A compound widget for handling picking a source folder, a destination folder and a name for the file about to be created."""
    def __init__(self, spacing=10):
        super().__init__()
        self.source = None; self.destination = None; self.name = None

        grid = Gtk.Grid()
        grid.set_column_spacing(spacing)
        grid.set_row_spacing(spacing)
        self.add(grid)

        grid.attach(Label("Source:", 0.5), 0, 0, 1, 1)
        src_btn = Gtk.FileChooserButton(title="Choose source", action=Gtk.FileChooserAction.SELECT_FOLDER, hexpand=True)
        grid.attach(src_btn, 1, 0, 1, 1)
        src_btn.connect("file-set", self.on_source_set)

        grid.attach(Label("Destination:", 0.5), 0, 1, 1, 1)
        dest_btn = Gtk.FileChooserButton(title="Choose destination", action=Gtk.FileChooserAction.SELECT_FOLDER, hexpand=True)
        grid.attach(dest_btn, 1, 1, 1, 1)
        dest_btn.connect("file-set", self.on_destination_set)

        grid.attach(Label("Name:", 0.5), 0, 2, 1, 1)
        name_entry = Gtk.Entry()
        grid.attach(name_entry, 1, 2, 1, 1)
        name_entry.connect("changed", self.on_name_set)

    def on_source_set(self, btn):
        self.source = btn.get_filename()

    def on_destination_set(self, btn):
        self.destination = btn.get_filename()

    def on_name_set(self, entry):
        name = entry.get_text().strip()
        if name != "": self.name = name

class HSLColorPicker(Gtk.Box):
    """An interactive color picker widget with sliders for hue, saturation and lightness."""
    def __init__(self):
        super().__init__()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        self.add(grid)

        hsv = Gtk.HSV()
        hsv.set_color(0.5, 0.5, 0.5)
        self.color = hsv.get_color()
        grid.attach(hsv, 0, 0, 3, 3)

        grid.attach(Label("H", 0.8), 4, 0, 1, 1)
        h = Gtk.HScale.new_with_range(0, 360, 1)
        h.set_value(180); h.set_hexpand(True)
        grid.attach(h, 5, 0, 1, 1)

        grid.attach(Label("S", 0.8), 4, 1, 1, 1)
        s = Gtk.HScale.new_with_range(0, 100, 1)
        s.set_value(50); s.set_hexpand(True)
        grid.attach(s, 5, 1, 1, 1)

        grid.attach(Label("L", 0.8), 4, 2, 1, 1)
        v = Gtk.HScale.new_with_range(0, 100, 1)
        v.set_value(50); v.set_hexpand(True)
        grid.attach(v, 5, 2, 1, 1)

        h.connect("value-changed", self.on_hue_set, hsv)
        s.connect("value-changed", self.on_sat_set, hsv)
        v.connect("value-changed", self.on_val_set, hsv)
        hsv.connect("changed", self.on_hsv_set, h, s, v)

    def on_hsv_set(self, hsv, h, s, v):
        self.color = hsv.get_color()
        h.set_value(self.color.h * 360)
        s.set_value(self.color.s * 100)
        v.set_value(self.color.v * 100)

    def on_hue_set(self, h, hsv):
        hsv.set_color(h.get_value() / 360, self.color.s, self.color.v)

    def on_sat_set(self, s, hsv):
        hsv.set_color(self.color.h, s.get_value() / 100, self.color.v)

    def on_val_set(self, v, hsv):
        hsv.set_color(self.color.h, self.color.s, v.get_value() / 100)

class ComboBoxFolder(Gtk.ComboBoxText):
    """Create a Gtk.ComboBoxText from the files within a given folder."""
    def __init__(self, path):
        super().__init__(hexpand=True)
        self.choice = None

        files = os.listdir(path)
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                self.append_text(file)

        self.connect("changed", self.on_combobox_changed, path)

    def on_combobox_changed(self, combobox, path):
        self.choice = os.path.join(path, combobox.get_active_text())
