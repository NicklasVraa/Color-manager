# Documentation functions ------------------------------------------------------
import subprocess
from os.path import join, abspath, expanduser, splitext
from os import listdir, makedirs

def generate_entry(base:str, name:str) -> str:
    """Return a string for copy-pasting into the project readme."""

    return '| ' + name.capitalize() + ' | <img src="previews/' + base + '/' + name + '/colors.png" width="50"/>  <img src="previews/' + base + '/' + name + '/firefox.png" width="50"/> <img src="previews/' + base + '/' + name + '/vscode.png" width="50"/> <img src="previews/' + base + '/' + name + '/account.png" width="50"/>  <img src="previews/' + base + '/' + name + '/video.png" width="50"/> <img src="previews/' + base + '/' + name + '/git.png" width="50"/> | Finished |'

def generate_previews(src_path:str, dest_path:str, width:int = 300) -> None:
    """Generate png previews of an icon_pack. Convert all svgs in a folder to pngs in another, using the external program called ImageMagick."""

    in_path = abspath(expanduser(src_path))
    out_path = abspath(expanduser(dest_path))

    try:
        subprocess.run(['inkscape', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise RuntimeError("Inkscape is not installed.")

    makedirs(out_path, exist_ok=True)
    svgs = [file for file in listdir(in_path) if file.endswith('.svg')]

    for svg in svgs:
        svg_path = join(in_path, svg)
        png = splitext(svg)[0] + '.png'
        png_path = join(out_path, png)
        command = ['inkscape', svg_path, '-o', png_path, '-w', str(width)]
        subprocess.run(command)
