# Color Manager <img src="resources/icon.svg" width="50"/>

[Roadmap](#roadmap) | [Features](#features) | [Use](#use) | [Requests](#requests) | [Contribute](#contribute)

Color Manager is a program for recoloring and manipulating existing icon packs, wallpapers and themes. The program is designed for [NovaOS](https://github.com/NicklasVraa/NovaOS) and is currently in **early development**. The first release will be late August 2023. In the meantime, this repository will act as a preview.

![gui](resources/gui.png)

**Instanty recolor artwork such as wallpapers.**
| Operation | Result |
| :---------: | ------ |
| Original | ![1](resources/original.png) |
| Monochrome: (0.6, 0.54, 0.5) | ![2](resources/mono.png) |
| Multichrome: dracula.json | ![3](resources/multi.png) |

To decrease the perceived noise after multichromatic recoloring, simply increase the number of colors in the palette, e.g. populate it with slight variations of the existing colors.

**GUI Demo**:
![demo](resources/demo.gif)


**Note**: If you publish anything that was generated using this program, make sure to credit the original creator and this repository.


## Roadmap <a name="roadmap"></a>
- [x] Basic framework for manipulating icon packs.
- [x] Grayscale, monochromatic and multichromatic recoloring functions.
- [x] Command-line interface.
- [x] Graphical user interface based on the GTK framework.
- [x] Python pip package.
- [x] Full support for pngs and jpgs.
- [ ] Basic framework for manipulating GTK, Cinnamon and Metacity themes.
- [ ] Intelligent color inversion function.
- [ ] Function for adding basic geometry to the backgrounds of icons.
- [ ] GNU/Linux binary.


## Features <a name="features"></a>
Currently, two types of recoloring operations are supported:
| Type        | Result | Speed            | Supports |
| ----------- | ------ | ---------------- | -------- |
| Monochrome  | A monochromatic variant, colored by appropriate shades of the provided base color. | ~5000 svgs/sec | svg, png, jpg |
| Multichrome | A multichromatic variant, where all colors are replaced by their nearest perceived equivalent that adheres to the provided color palette. | ~100 svgs/sec | svg, png, jpg |

Speeds were recorded with an Intel i7-4770K CPU. Any asset can serve as the base for any color palette or base color.


## Using the Program<a name="use"></a>
Either import `utils` into your own script and call the recoloring functions, e.g.:
```python
from color_manager import utils
```
```python
src     = "packs/test_pack"
name    = "my_pack"
dest    = "~/Downloads"
hsl     = (0.5, 0.5, 0.5) # = rc.norm_hsl(180, 50, 50)
palette = "palettes/dracula.json"

utils.recolor(src, dest, name, hsl) # hsl or palette.
```

Or launch the GUI by running `python3 color_manager/gui.py` in a terminal from the project's root directory. The GUI will adopt your active theme. Dependencies: `colormath`, `tqdm` and `pillow`. For the GUI, `pygobject` (GTK bindings) must also be installed.


## Requests <a name="requests"></a>
Until the release of Color Manager, I will be taking requests for icon packs and recolorings. Simply submit a feature request here on the repository containing the following:
- The name of an open-source icon pack that will serve as the base look.
- For a monochromatic variant, a single hexadecimal value representing a color.
- For particular color palettes, a list of hexadecimal values or the name of a popular palette.

Please star the repository or consider donating, and I will upload your requested variant. Also consider showing the creators of the original artworks some love.


## Contribute <a name="contribute"></a>
If you are experienced with packaging projects such as this for easy distribution, please contact me.

---
**Legal Notice**: This repository, including any and all of its forks and derivatives, may NOT be used in the development or training of any machine learning model of any kind, without the explicit permission of the owner of the original repository.
