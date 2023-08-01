# Desc: The GUI for color_manager
# Auth: Nicklas Vraa

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from os.path import basename
from ngtk import Page, Label, Files, HSLColorPicker
from color_manager import monochrome_pack, multichrome_pack

class Window(Gtk.Window):
    def __init__(self):
        super().__init__(title="Color Manager")
        self.set_default_size(400, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        padding = 10
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(content)
        self.pages = Gtk.Notebook()
        content.pack_start(self.pages, True, True, 0)

        mono  = Page(self.pages, "Monochromatic", padding)
        mono.add(Label("Choose a hue, saturation and lightness offset that will serve as the base for your monochromatic icon pack or theme variant."))

        self.color_picker = HSLColorPicker(padding)
        mono.add(self.color_picker)

        multi = Page(self.pages, "Multichromatic", padding)
        multi.add(Label("Choose a palette file containing a list of colors. Only these will occur in the new icon pack or theme."))

        self.palette = None
        palette_btn = Gtk.FileChooserButton(title="Choose palette file")
        palette_btn.connect("file-set", self.on_palette_chosen)
        multi.add(palette_btn)

        about = Page(self.pages, "About", padding)
        about.add(Label("Color Manager is a program for recoloring existing svg-based icon packs as well as themes. The program is designed for <a href='https://github.com/NicklasVraa/NovaOS'>NovaOS</a>.\n\nCheck for updates on the project's <a href='https://github.com/NicklasVraa/Color-manager'>repository</a>."))

        # Shared widget.
        shared = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=padding)
        shared.set_border_width(padding)
        content.add(shared)
        self.files = Files(padding)
        shared.pack_start(self.files, True, True, 1)
        progress_bar = Gtk.ProgressBar()
        shared.add(progress_bar)
        gen_area = Gtk.Box(spacing=padding)
        gen_btn = Gtk.Button(label="Generate")
        gen_btn.connect("clicked", self.on_generate)
        gen_area.add(gen_btn)
        self.status = Label("")
        gen_area.add(self.status)
        shared.add(gen_area)

    def on_color_set(self, color_picker):
        self.color = color_picker.get_color()
        print(self.color)

    def on_palette_chosen(self, btn):
        self.palette = btn.get_filename()

    def on_generate(self, btn):
        if self.files.source is None:
            self.status.set_text("Choose a source folder first")
            return

        if self.files.destination is None:
            self.status.set_text("Choose a destination folder first")
            return

        if self.files.name is None:
            self.status.set_text("Enter a name first")
            return

        current_page = self.pages.get_current_page()
        if current_page == 0:
            if self.color is None:
                self.status.set_text("Choose a base color")
                return
            else:
                self.status.set_text("Generating " + self.files.name + " variant from " + basename(self.files.source) + " and " + self.color)

                #monochrome_pack(self.source, self.destination, self.name, self.color)

        elif current_page == 1:
            if self.palette is None:
                self.status.set_text("Choose a color palette file")
                return
            else:
                self.status.set_text("Generating " + self.files.name + " variant from " + basename(self.files.source) + " and " + basename(self.palette))

                #multichrome_pack(self.source, self.destination, self.name, self.palette)

win = Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
