# Desc: The GUI for color_manager
# Auth: Nicklas Vraa

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from PIL import Image
import os, ngtk, utils

def recolor(src_path, dest_path, name, replacement, progress_bar, status):
    """Recursively copies and converts a source folder into a destination, given a either a color or a palette."""

    is_mono, new_colors = utils.get_input_colors(replacement)
    dest_path = utils.copy_pack(src_path, dest_path, name)
    svg_paths = utils.get_paths(dest_path, [".svg"])
    img_paths = utils.get_paths(dest_path, [".png", ".jpg", ".jpeg"])

    n = len(svg_paths); i = 0
    for path in svg_paths:
        with open(path, 'r') as file:
            svg = file.read()

        colors = utils.get_svg_colors(svg)

        if is_mono: svg = utils.monochrome_svg(svg, colors, new_colors)
        else: svg = utils.multichrome_svg(svg, colors, new_colors)

        with open(path, 'w') as file:
            file.write(svg)

        i = i + 1
        progress_bar.set_fraction(i/n)
        while Gtk.events_pending():
            Gtk.main_iteration()

    status.set_text("SVGs completed! Continuing...")

    n = len(img_paths); i = 0
    for path in img_paths:
        img = Image.open(path)

        if is_mono: img = utils.monochrome_img(img, new_colors)
        else: img = utils.multichrome_img(img, new_colors)

        img.save(path)

        i = i + 1
        progress_bar.set_fraction(i/n)
        while Gtk.events_pending():
            Gtk.main_iteration()

    status.set_text("Finished!")

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

        mono  = ngtk.Page(self.pages, "Monochromatic", padding)
        mono.add(ngtk.Label("Choose a hue, saturation and lightness offset that will serve as the base for your monochromatic icon pack variant."))
        self.color_picker = ngtk.HSLColorPicker()
        mono.add(self.color_picker)

        multi = ngtk.Page(self.pages, "Multichromatic", padding)
        multi.add(ngtk.Label("Load a palette file containing a list of colors."))
        self.palette = None
        palette_desc = ngtk.Label("No palette chosen.")
        palette_btn = Gtk.FileChooserButton(title="Choose palette file")
        palette_btn.connect("file-set", self.on_custom_palette_set, palette_desc)
        multi.add(palette_btn)
        multi.add(ngtk.Label("Or load one of the premade color palettes."))
        self.palette_picker = ngtk.ComboBoxFolder("palettes")
        multi.add(self.palette_picker)
        self.palette_picker.connect("changed", self.on_palette_set, palette_desc)
        multi.add(palette_desc)

        about = ngtk.Page(self.pages, "About", padding)
        about.add(ngtk.Label("Color Manager is a program for recoloring existing svg-based icon packs as well as themes. The program is designed for <a href='https://github.com/NicklasVraa/NovaOS'>NovaOS</a>.\n\nCheck for updates on the project's <a href='https://github.com/NicklasVraa/Color-manager'>repository</a>."))

        shared = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=padding)
        shared.set_border_width(padding)
        content.add(shared)
        self.files = ngtk.Files(padding)
        shared.pack_start(self.files, True, True, 1)
        self.progress_bar = Gtk.ProgressBar()
        shared.add(self.progress_bar)
        gen_area = Gtk.Box(spacing=padding)
        gen_btn = Gtk.Button(label="Generate")
        gen_btn.connect("clicked", self.on_generate)
        gen_area.add(gen_btn)
        self.status = ngtk.Label("")
        gen_area.add(self.status)
        shared.add(gen_area)

    def on_custom_palette_set(self, btn, palette_desc):
        self.palette = utils.load_palette_file(btn.get_filename())
        palette_desc.set_text(self.palette["name"] + ": " + self.palette["desc"])

    def on_palette_set(self, palette_picker, palette_desc):
        self.palette = utils.load_palette_file(palette_picker.choice)
        palette_desc.set_text(self.palette["name"] + ": " + self.palette["desc"])

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
            if self.color_picker.color is None:
                self.status.set_text("Choose a base color")
                return
            else:
                btn.set_sensitive(False)
                self.status.set_text("Generating " + self.files.name + " variant from " + os.path.basename(self.files.source) + "...")

                recolor(self.files.source, self.files.destination, self.files.name, self.color_picker.color, self.progress_bar, self.status)

        elif current_page == 1:
            if self.palette is None:
                self.status.set_text("Choose a color palette file")
                return
            else:
                btn.set_sensitive(False)
                self.status.set_text("Generating " + self.files.name + " variant from " + os.path.basename(self.files.source) + " and " + os.path.basename(self.palette["name"]) + "...")

                recolor(self.files.source, self.files.destination, self.files.name, self.palette, self.progress_bar, self.status)

        btn.set_sensitive(True)

win = Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
