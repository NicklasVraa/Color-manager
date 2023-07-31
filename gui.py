import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import os
import color_manager as cm

TITLE = "Color Manager"
PAD = 10
DIMS = (300, 200)

class Window(Gtk.Window):
    def __init__(self):
        super().__init__(title=TITLE)
        self.set_default_size(DIMS[0], DIMS[1])
        self.set_position(Gtk.WindowPosition.CENTER)
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(content)
        self.pages = Gtk.Notebook()
        content.pack_start(self.pages, True, True, 0)

        mono  = Page(self.pages, "Monochromatic")
        mono.add(Label("Choose a single color that will serve as the base color for your monochromatic icon pack or theme variant."))

        self.color = None
        color_btn = Gtk.ColorButton()
        color_btn.connect("color-set", self.on_color_chosen)
        mono.add(color_btn)

        multi = Page(self.pages, "Multichromatic")
        multi.add(Label("Choose a palette file containing a list of colors. Only these will occur in the new icon pack or theme."))

        self.palette = None
        palette_btn = Gtk.FileChooserButton(title="Choose palette file")
        palette_btn.connect("file-set", self.on_palette_chosen)
        multi.add(palette_btn)

        about = Page(self.pages, "About")
        about.add(Label("Color Manager is a program for recoloring existing svg-based icon packs as well as themes. The program is designed for <a href='https://github.com/NicklasVraa/NovaOS'>NovaOS</a>.\n\nCheck for updates on the project's <a href='https://github.com/NicklasVraa/Color-manager'>repository</a>."))

        # Shared widget.
        shared = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=PAD)
        shared.set_border_width(PAD)
        content.add(shared)
        io_area = Gtk.Box(spacing=PAD, homogeneous=True)
        shared.add(io_area)
        self.source = None
        src_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=PAD)
        src_area.add(Label("Choose source pack:"))
        src_btn = Gtk.FileChooserButton(title="Choose source pack", action=Gtk.FileChooserAction.SELECT_FOLDER)
        src_btn.connect("file-set", self.on_source_chosen)
        src_area.add(src_btn)
        io_area.add(src_area)
        self.name = None
        name_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=PAD)
        name_area.add(Label("Name your pack:"))
        self.dest_entry = Gtk.Entry()
        name_area.add(self.dest_entry)
        io_area.add(name_area)
        progress_bar = Gtk.ProgressBar()
        shared.add(progress_bar)
        gen_area = Gtk.Box(spacing=PAD)
        gen_btn = Gtk.Button(label="Generate")
        gen_btn.connect("clicked", self.on_generate)
        gen_area.add(gen_btn)
        self.status = Label("Status:")
        gen_area.add(self.status)
        shared.add(gen_area)

    def on_color_chosen(self, btn):
        rgba = btn.get_rgba()
        r = int(rgba.red * 255)
        g = int(rgba.green * 255)
        b = int(rgba.blue * 255)
        self.color = "#{:02x}{:02x}{:02x}".format(r,g,b)

    def on_palette_chosen(self, btn):
        self.palette = btn.get_filename()

    def on_source_chosen(self, btn):
        self.source = btn.get_filename()

    def on_generate(self, btn):
        if self.source is None:
            self.status.set_text("Choose a source folder first")
            return

        self.name = self.dest_entry.get_text().strip()
        if self.name == "":
            self.status.set_text("Enter a name first")
            return

        current_page = self.pages.get_current_page()
        if current_page == 0:
            if self.color is None:
                self.status.set_text("Choose a base color")
                return
            else:
                self.status.set_text("Status: Generating " + self.name + " variant from " + os.path.basename(self.source) + " and " + self.color)

                h,s,l = cm.hex_to_hsl(self.color)
                h,s,l = cm.normalize_hsl(h,s,l)
                cm.monotone_pack(self.source, self.name, h, s, l)

        elif current_page == 1:
            if self.palette is None:
                self.status.set_text("Choose a color palette file")
                return
            else:
                self.status.set_text("Status: Generating " + self.name + " variant from " + os.path.basename(self.source) + " and " + os.path.basename(self.palette))

                #cm.recolor_pack(self.source, self.name, self.palette)

class Page(Gtk.Box):
    def __init__(self, notebook, header):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=PAD)
        self.set_border_width(PAD)
        notebook.append_page(self, Gtk.Label(label=header, hexpand=True))

class Label(Gtk.Label):
    def __init__(self, text):
        super().__init__()
        self.set_markup(text)
        self.set_alignment(0,0)
        self.set_line_wrap(True)

win = Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
