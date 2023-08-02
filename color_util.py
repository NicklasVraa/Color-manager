# Desc: A program for recoloring existing svg-based icon packs as well as
#       themes. Designed for NovaOS.
#
# Auth: Nicklas Vraa

from typing import List, Set
from tqdm import tqdm
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from gi.repository import Gtk
import os, re, shutil, subprocess, json

# Color space conversion -------------------------------------------------------

def hex_to_rgb(hex:str):
    """Convert hexadecimal color to RGB base 16."""
    hex = hex.lstrip('#')
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return r, g, b

def rgb_to_hsl(rgb):
    """Convert RGB to HSL color-space."""
    r, g, b = rgb
    r /= 255.0; g /= 255.0; b /= 255.0
    max_val = max(r, g, b); min_val = min(r, g, b)
    h = s = l = (max_val + min_val) / 2.0

    if max_val == min_val:
        h = s = 0
    else:
        d = max_val - min_val
        s = d / (2.0 - max_val - min_val)

        if max_val == r:
            h = (g - b) / d + (6.0 if g < b else 0.0)
        elif max_val == g:
            h = (b - r) / d + 2.0
        else:
            h = (r - g) / d + 4.0
        h /= 6.0

    return h, s, l

def hue_to_rgb(p, q, t):
    """Convert Hue to RGB values. Used only by hsl_to_rgb."""
    if t < 0: t += 1
    if t > 1: t -= 1
    if t < 1 / 6: return p + (q - p) * 6 * t
    if t < 1 / 2: return q
    if t < 2 / 3: return p + (q - p) * (2 / 3 - t) * 6

    return p

def hsl_to_rgb(hsl):
    """Convert HSL to RGB color-space."""
    h, s, l = hsl

    if s == 0:
        r = g = b = l
    else:
        if l < 0.5: q = l * (1 + s)
        else: q = l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

    r = int(round(r * 255))
    g = int(round(g * 255))
    b = int(round(b * 255))
    return r, g, b

def rgb_to_hex(rgb):
    """Convert RGB base 16 to hexadecimal."""
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hex_to_hsl(hex):
    """Convert hexadecimal color to HSL color-space."""
    return rgb_to_hsl(hex_to_rgb(hex))

def hex_color_to_grayscale(hex:str) -> str:
    """Convert a hexadecimal color to a hexadecimal grayscale equivalent."""
    hex = hex.lstrip('#')
    r,g,b = int(hex[0:2],16), int(hex[2:4],16), int(hex[4:6],16)
    gs = int(0.21*r + 0.72*g + 0.07*b)
    hex_gs = '#' + format(gs, '02x')*3

    return hex_gs

# Input/Output -----------------------------------------------------------------

def load_palette(path:str):
    """Load a json file defining a color palette object."""
    with open(path, 'r') as file:
        palette = json.load(file)
    return palette

def expand_path(path:str) -> str:
    """Turns given path into absolute and supports bash notation."""
    return os.path.abspath(os.path.expanduser(path))

def get_paths(folder:str, ext:str) -> List[str]:
    """Return path of every file with the given extension within a folder
    and its subfolders, excluding symbolic links."""
    paths = []

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)

        if os.path.islink(item_path): # Link.
            continue

        if os.path.isfile(item_path): # File.
            if item.lower().endswith(ext):
                paths.append(item_path)

        elif os.path.isdir(item_path): # Folder.
            subfolder_svg_paths = get_paths(item_path, ext)
            paths.extend(subfolder_svg_paths)

    return paths

def copy_file_structure(src_path:str, dest_path:str):
    """Copies a directory tree, but changes symbolic links to point
    to files within the destination folder instead of the source.
    Assumes that no link points to files outside the source folder."""

    shutil.rmtree(dest_path, ignore_errors=True)
    shutil.copytree(src_path, dest_path, symlinks=True)

    for root, _, files in os.walk(dest_path):
        for file in files:
            file_path = os.path.join(root, file)

            if os.path.islink(file_path):
                link_target = os.readlink(file_path)

                if not os.path.isabs(link_target):
                    continue

                # Make link relative and update.
                link_base = os.path.dirname(file_path)
                relative_target = os.path.relpath(link_target, link_base)
                os.remove(file_path)

                # Replace root source folder with root destination folder.
                relative_target = relative_target.replace(src_path, dest_path, 1)
                os.symlink(relative_target, file_path)

def rename_pack(path:str, name:str):
    """If an index.theme file exists within the given folder, apply
    appropiate naming."""
    path = os.path.join(path, name)
    index_path = os.path.join(path, "index.theme")

    if os.path.exists(index_path):
        with open(index_path, 'r') as file:
            content = file.read()
            contents = re.sub(r"Name=.*", "Name=" + name, content, count=1)

        with open(index_path, 'w') as file:
            file.write(contents)

# Documentation functions ------------------------------------------------------

def generate_entry(base:str, name:str) -> str:
    """Return a string for copy-pasting into the project readme."""
    return '| ' + name.capitalize() + ' | <img src="previews/' + base + '/' + name + '/colors.png" width="50"/>  <img src="previews/' + base + '/' + name + '/firefox.png" width="50"/> <img src="previews/' + base + '/' + name + '/vscode.png" width="50"/> <img src="previews/' + base + '/' + name + '/account.png" width="50"/>  <img src="previews/' + base + '/' + name + '/video.png" width="50"/> <img src="previews/' + base + '/' + name + '/git.png" width="50"/> | Finished |'

def generate_previews(src_path:str, dest_path:str, name:str, width:int = 300) -> None:
    """Generate png previews of an icon_pack. Convert all svgs in a folder to pngs in another, using the external program called ImageMagick."""
    in_path = os.path.join(expand_path(src_path), "preview")
    out_path = os.path.join(expand_path(dest_path), name)

    try:
        subprocess.run(['inkscape', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise RuntimeError("Inkscape is not installed.")

    os.makedirs(out_path, exist_ok=True)
    svgs = [file for file in os.listdir(in_path) if file.endswith('.svg')]

    for svg in svgs:
        svg_path = os.path.join(in_path, svg)
        png = os.path.splitext(svg)[0] + '.png'
        png_path = os.path.join(out_path, png)
        command = ['inkscape', svg_path, '-o', png_path, '-w', str(width)]
        subprocess.run(command)

# Utility ----------------------------------------------------------------------

def clamp(value:float, a:float, b:float) -> float:
    """Clamp an input value between a and b."""
    return max(a, min(value, b))

def normalize_hsl(h:int, s:int, l:int):
    """Converts from conventional HSL format to normalized."""
    return h/360, s/100, 2*(l/100)-1

def get_fill_colors(svg:str) -> Set[str]:
    """Return a list of all unique fill colors within a given string
    representing an svg-file."""
    colors = set()
    matches = re.findall(r"#[A-Fa-f0-9]{6}", svg)

    for match in matches:
        colors.add(match)

    return colors

def delta_e(color1:str, color2:str) -> float:
    """Returns the distance between two colors in the CIELAB color-space."""
    r1,g1,b1 = hex_to_rgb(color1)
    r2,g2,b2 = hex_to_rgb(color2)
    color1 = sRGBColor(r1,g1,b1)
    color2 = sRGBColor(r2,g2,b2)
    color1 = convert_color(color1, LabColor)
    color2 = convert_color(color2, LabColor)

    return delta_e_cie2000(color1, color2)

def closest_color_match(color:str, palette:List[str]) -> str:
    """Compare the similarity of colors in the CIELAB colorspace. Return the
    closest match, i.e. the palette entry with the smallest euclidian distance
    to the given color."""
    closest_color = None
    min_distance = float('inf')

    for entry in palette:
        distance = delta_e(color, entry)

        if distance < min_distance:
            min_distance = distance
            closest_color = entry

    return closest_color

# Monochrome -------------------------------------------------------------------

def to_grayscale(svg:str, colors:Set[str]) -> str:
    """Replace every instance of colors within the given list with their
    grayscale equivalent in the given string representing an svg-file."""
    gray_svg = svg
    graytones = set()

    for color in colors:
        graytone = hex_color_to_grayscale(color)
        graytones.add(graytone)
        gray_svg = re.sub(color, graytone, gray_svg)

    return gray_svg, graytones

def monochrome_icon(svg:str, colors:Set[str], hsl) -> str:
    """Replace every instance of color within the given list with their
    monochrome equivalent in the given string representing an svg-file,
    determined by the given hue, saturation and lightness offset."""
    h, s, l_offset = hsl
    l_offset = (l_offset - 0.5) * 2 # Remapping.

    monochrome_svg = svg
    monochromes = set()

    for color in colors:
        graytone = hex_color_to_grayscale(color)
        _, _, l = rgb_to_hsl(hex_to_rgb(graytone))
        l = clamp(l + l_offset, -1, 1)
        monochrome = rgb_to_hex(hsl_to_rgb((h, s, l)))
        monochromes.add(monochrome)
        monochrome_svg = re.sub(color, monochrome, monochrome_svg)

    return monochrome_svg, monochromes

def monochrome_pack(src_path:str, dest_path:str, name:str, hsl, progress_bar = None) -> None:
    """Recursively copies and converts a source folder of svg icons into
    a monochrome set at a destination, given a hue, saturation and lightness
    offset."""
    h, s, l_offset = hsl

    src_path = expand_path(src_path)
    dest_path = os.path.join(expand_path(dest_path), name)

    copy_file_structure(src_path, dest_path)
    rename_pack(dest_path, name)
    paths = get_paths(dest_path, ".svg")

    n = len(paths); i = 0
    for path in tqdm(paths, desc="Processing SVGs", unit=" file"):
        with open(path, 'r') as file:
            svg = file.read()
        colors = get_fill_colors(svg)

        if s == 0:
            svg, _ = to_grayscale(svg, colors) # Faster.
        else:
            svg, _ = monochrome_icon(svg, colors, (h, s, l_offset))

        with open(path, 'w') as file:
            file.write(svg)

        i = i+1
        progress_bar.set_fraction(i/n)
        while Gtk.events_pending():
            Gtk.main_iteration()

# Multichrome ------------------------------------------------------------------

def multichrome_icon(svg:str, colors:Set[str], new_colors:List[str]) -> str:
    """Replace colors in a given svg with the closest match within a given
    color palette."""
    multichrome_svg = svg

    for color in colors:
        new_color = closest_color_match(color, new_colors)
        multichrome_svg = re.sub(color, new_color, multichrome_svg)

    return multichrome_svg

def multichrome_pack(src_path:str, dest_path:str, name:str, palette, progress_bar = None) -> None:
    """Recursively copies and converts a source folder of svg icons into
    a multichrome set at a destination, given a color palette file."""
    src_path = expand_path(src_path)
    dest_path = os.path.join(expand_path(dest_path), name)

    copy_file_structure(src_path, dest_path)
    rename_pack(dest_path, name)
    paths = get_paths(dest_path, ".svg")

    if type(palette) is str: # If path is given instead of list of colors.
        new_colors = load_palette(palette)["colors"]
    else:
        new_colors = palette["colors"]

    n = len(paths); i = 0
    for path in tqdm(paths, desc="Processing SVGs", unit=" file"):
        with open(path, 'r') as file:
            svg = file.read()
        colors = get_fill_colors(svg)

        svg = multichrome_icon(svg, colors, new_colors)

        with open(path, 'w') as file:
            file.write(svg)

        i = i+1
        progress_bar.set_fraction(i/n)
        while Gtk.events_pending():
            Gtk.main_iteration()
