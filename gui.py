import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os, subprocess

class ColorManagerGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Color Manager")

        # Window setup.
        self.set_default_size(300, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Top container setup.
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(container)
        pages = Gtk.Notebook()
        container.add(pages)

        # Monochromatic page.
        mono_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        pages.append_page(mono_page, Gtk.Label(label="Monochromatic", hexpand=True))
        mono_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        mono_container.set_border_width(10)
        mono_page.add(mono_container)
        label = Gtk.Label(label="Choose a single color that will serve as the base color for your monochromatic icon pack variant.")
        label.set_alignment(0,0)
        label.set_line_wrap(True)
        mono_container.add(label)

        mono_color = Gtk.ColorButton()
        mono_container.add(mono_color)

        # Multichromatic page.
        multi_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        pages.append_page(multi_page, Gtk.Label(label="Multichromatic", hexpand=True))

        multi_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        multi_container.set_border_width(10)
        multi_page.add(multi_container)
        label = Gtk.Label(label="Choose a palette file containing a list of colors. Only these will occur in the new pack.")
        label.set_alignment(0,0)
        label.set_line_wrap(True)
        multi_container.add(label)

        palette_button = Gtk.FileChooserButton()
        palette_button.set_title("Choose palette file")
        multi_container.add(palette_button)

        # About page.
        about_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        pages.append_page(about_page, Gtk.Label(label="About", hexpand=True))
        about_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        about_container.set_border_width(10)
        about_page.add(about_container)
        label = Gtk.Label()
        label.set_markup("Color Manager is a program for recoloring existing svg-based icon packs as well as themes. The program is designed for <a href='https://github.com/NicklasVraa/NovaOS'>NovaOS</a>.\n\nCheck for updates on the project's <a href='https://github.com/NicklasVraa/Color-manager'>repository</a>.")
        label.set_alignment(0,0)
        label.set_line_wrap(True)
        about_container.add(label)

        # Shared container setup.
        shared = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        shared.set_border_width(10)
        container.add(shared)

        # Input-output area.
        io_area = Gtk.Box(spacing=10)
        io_area.set_homogeneous(True)

        dest_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="Name your pack:")
        label.set_alignment(0,0)
        dest_area.add(label)
        dest_entry = Gtk.Entry()
        dest_area.add(dest_entry)
        io_area.add(dest_area)

        src_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="Choose source pack:")
        label.set_alignment(0,0)
        src_area.add(label)
        src_button = Gtk.FileChooserButton()
        src_button.set_title("Choose source pack")
        src_area.add(src_button)
        io_area.add(src_area)
        shared.add(io_area)

        # Progress bar.
        progress_bar = Gtk.ProgressBar()
        shared.add(progress_bar)

        gen_area = Gtk.Box(spacing=10)
        button = Gtk.Button(label="Generate")
        gen_area.add(button)
        status = Gtk.Label(label="Status:")
        status.set_alignment(0,0)
        status.set_line_wrap(True)
        gen_area.add(status)
        shared.add(gen_area)

win = ColorManagerGUI()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
