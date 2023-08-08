# Desc: A program for recoloring icon packs, themes and wallpapers. For NovaOS.
# Auth: Nicklas Vraa

from typing import List, Set, Tuple, Dict
from tqdm import tqdm
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from PIL import Image
import os, re, shutil, json

# Color conversion -------------------------------------------------------------

def hex_to_rgb(hex:str) -> Tuple[int,int,int]:
    hex = hex.lstrip('#')
    return int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)

def hex_to_hsl(hex:str) -> Tuple[float,float,float]:
    return rgb_to_hsl(hex_to_rgb(hex))

def hex_to_gray(hex:str) -> str:
    r, g, b = hex_to_rgb(hex)
    return '#' + format(int(0.21*r + 0.72*g + 0.07*b), '02x')*3

def rgb_to_hex(rgb:Tuple[int,int,int]) -> str:
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def rgb_to_hsl(rgb:Tuple[int,int,int]) -> Tuple[float,float,float]:
    r, g, b = rgb
    r /= 255.0; g /= 255.0; b /= 255.0
    max_val = max(r, g, b); min_val = min(r, g, b)
    h = s = l = (max_val + min_val) / 2.0

    if max_val == min_val:
        h = s = 0
    else:
        d = max_val - min_val
        s = d / (2.0 - max_val - min_val)

        if max_val == r: h = (g - b) / d + (6.0 if g < b else 0.0)
        elif max_val == g: h = (b - r) / d + 2.0
        else: h = (r - g) / d + 4.0
        h /= 6.0

    return h, s, l

def rgb_to_gray(rgb:Tuple[int,int,int]) -> Tuple[int,int,int]:
    r, g, b = rgb
    weighed_avg = int(0.21*r + 0.72*g + 0.07*b)
    return weighed_avg, weighed_avg, weighed_avg

def hsl_to_rgb(hsl:Tuple[float,float,float]) -> Tuple[int,int,int]:
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

    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))

def hue_to_rgb(p:float, q:float, t:float) -> float:
    if t < 0: t += 1
    if t > 1: t -= 1
    if t < 1 / 6: return p + (q - p) * 6 * t
    if t < 1 / 2: return q
    if t < 2 / 3: return p + (q - p) * (2 / 3 - t) * 6
    return p

def norm_hsl(h:int, s:int, l:int) -> Tuple[float,float,float]:
    return h/360, s/100, l/100

# Color comparision ------------------------------------------------------------

def load_palette_file(path:str) -> Dict:
    with open(path, 'r') as file:
        palette = json.load(file)
    return palette

def get_input_colors(resource) -> List[str]:
    """Returns an HSL tuple, or a list of colors, depending on the input, as well as a boolean indicating either."""

    if isinstance(resource, tuple) and len(resource) == 3:
        return True, resource

    elif type(resource) is str:
        return False, load_palette_file(resource)["colors"]

    else:
        return False, resource["colors"]

def get_svg_colors(svg:str) -> Set[str]:
    """Return a list of all unique colors within a given string
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
    color1 = convert_color(sRGBColor(r1,g1,b1), LabColor)
    color2 = convert_color(sRGBColor(r2,g2,b2), LabColor)

    return delta_e_cie2000(color1, color2)

def closest_match(color:str, palette:List[str]) -> str:
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

# Pack management --------------------------------------------------------------

def expand_path(path:str) -> str:
    return os.path.abspath(os.path.expanduser(path))

def get_paths(folder: str, exts: List[str]) -> List[str]:
    """Return paths of every file with the given extensions within a folder
    and its subfolders, excluding symbolic links."""

    paths = []

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)

        if os.path.islink(item_path): # Link.
            continue

        if os.path.isfile(item_path): # File.
            for ext in exts:
                if item.lower().endswith(ext):
                    paths.append(item_path)

        elif os.path.isdir(item_path): # Folder.
            subfolder_paths = get_paths(item_path, exts)
            paths.extend(subfolder_paths)

    return paths

def copy_file_structure(src_path:str, dest_path:str) -> None:
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

def rename_pack(path:str, name:str) -> None:
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

def copy_pack(src_path:str, dest_path:str, name:str) -> str:
    """Copy pack and return the resulting copy's directory path."""

    src_path = expand_path(src_path)
    dest_path = os.path.join(expand_path(dest_path), name)

    copy_file_structure(src_path, dest_path)
    rename_pack(dest_path, name)

    return dest_path

# Recolor ----------------------------------------------------------------------

def monochrome_svg(svg:str, colors:Set[str], hsl:Tuple[float,float,float]) -> str:
    """Replace every instance of color within the given list with their
    monochrome equivalent in the given string representing an svg-file,
    determined by the given hue, saturation and lightness offset."""

    h, s, l_offset = hsl

    if s == 0:
        for color in colors:
            graytone = hex_to_gray(color)
            svg = re.sub(color, graytone, svg)
    else:
        l_offset = (l_offset - 0.5) * 2 # Remapping.

        for color in colors:
            graytone = hex_to_gray(color)
            r, g, b = hex_to_rgb(graytone)
            l = (0.21*r + 0.72*g + 0.07*b)/255
            l = max(-1, min(l+l_offset, 1))
            monochrome = rgb_to_hex(hsl_to_rgb((h, s, l)))
            svg = re.sub(color, monochrome, svg)

    return svg

def multichrome_svg(svg:str, colors:Set[str], new_colors:List[str]) -> str:
    """Replace colors in a given svg with the closest match within a given
    color palette."""

    for color in colors:
        new_color = closest_match(color, new_colors)
        svg = re.sub(color, new_color, svg)

    return svg

def monochrome_img(img:Image, hsl:Tuple[float,float,float]) -> Image:
    """Replace every instance of color within the given list with their
    monochrome equivalent in the given image, determined by the given hue, saturation and lightness offset."""

    h, s, l_offset = hsl

    if s == 0:
        if img.mode == "RGBA":
            img = img.convert("LA")
        else:
            img = img.convert("L")
    else:
        width, height = img.size
        l_offset = (l_offset - 0.5) * 2 # Remapping.

        for x in range(width):
            for y in range(height):
                if img.mode == "RGBA":
                    r, g, b, a = img.getpixel((x, y))
                else:
                    r, g, b = img.getpixel((x, y))

                l = (0.21*r + 0.72*g + 0.07*b)/255
                l = max(-1, min(l+l_offset, 1))
                new_color = hsl_to_rgb((h, s, l))

                if img.mode == "RGBA":
                    img.putpixel((x,y), new_color + (a,))
                else:
                    img.putpixel((x,y), new_color)

    return img

def multichrome_img(img:str, new_colors:List[str]) -> Image:
    """Replace colors in a given image with the closest match within a given
    color palette."""

    width, height = img.size

    for x in range(width):
        for y in range(height):
            if img.mode == "RGBA":
                r, g, b, a = img.getpixel((x, y))
            else:
                r, g, b = img.getpixel((x, y))

            color = rgb_to_hex((r,g,b))
            new_color = hex_to_rgb(closest_match(color, new_colors))

            if img.mode == "RGBA":
                img.putpixel((x,y), new_color + (a,))
            else:
                img.putpixel((x,y), new_color)

    return img

def recolor(src_path:str, dest_path:str, name:str, replacement) -> None:
    """Recursively copies and converts a source folder into a destination, given a either a color or a palette."""

    is_mono, new_colors = get_input_colors(replacement)
    dest_path = copy_pack(src_path, dest_path, name)
    svg_paths = get_paths(dest_path, [".svg"])
    img_paths = get_paths(dest_path, [".png", ".jpg", ".jpeg"])

    for path in tqdm(svg_paths, desc="Processing svgs", unit="file"):
        with open(path, 'r') as file:
            svg = file.read()

        colors = get_svg_colors(svg)

        if is_mono: svg = monochrome_svg(svg, colors, new_colors)
        else: svg = multichrome_svg(svg, colors, new_colors)

        with open(path, 'w') as file:
            file.write(svg)

    for path in tqdm(img_paths, desc="Processing imgs", unit="file"):
        img = Image.open(path)

        if is_mono: img = monochrome_img(img, new_colors)
        # else: multichrome_img(img, new_colors) # too slow.

        img.save(path)
