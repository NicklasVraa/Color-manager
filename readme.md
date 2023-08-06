# Color Manager <img src="res/icon.svg" width="50"/>

[Roadmap](#roadmap) | [Features](#features) | [Use](#use) | [Requests](#requests) | [Contribute](#contribute)

Color Manager is a program for recoloring existing svg-based icon packs as well as themes. The program is designed for [NovaOS](https://github.com/NicklasVraa/NovaOS) and is currently in **early development**. The first release will be late August 2023. In the meantime, this repository will act as a preview.

![GUI](res/gui.png)

![Demo](res/demo.gif)

**Note**: If you publish an icon- or theme pack variant that was generated using this program, make sure to credit the original creator and this repository.


## Roadmap <a name="roadmap"></a>
- [x] Basic framework for manipulating icon packs.
- [x] Grayscale, monochromatic and multichromatic recoloring functions.
- [x] Command-line interface.
- [x] Graphical user interface based on the GTK framework.
- [ ] Basic framework for manipulating GTK, Cinnamon and Metacity themes.
- [ ] Intelligent color inversion function.
- [ ] Function for adding basic geometry to the backgrounds of icons.
- [ ] Python pip package.
- [ ] GNU/Linux binary.


## Features <a name="features"></a>
Currently, two types of recoloring operations are supported:
| Type        | Result | Speed            |
| ----------- | ------ | ---------------- |
| Monochrome  | A monochromatic variant, colored by appropriate shades of the provided base color. | ~5000 icons/sec |
| Multichrome | A multichromatic variant, where all colors are replaced by their nearest perceived equivalent that adheres to the provided color palette. | ~70 icons/sec |

Speeds were recorded with an Intel i7-4770K CPU. Any svg-based icon pack can serve as the base for any color palette or base color. For the best result when doing monochromatic recoloring, a pack where all icons have the same average saturation and lightness is recommended.


## Using the Program<a name="use"></a>
Either import `recolor` into your own script and call the recoloring functions, e.g.:
```python
from color_manager import recolor as rc
```
```python
src     = "packs/papirus-mini_mono"
name    = "my_mono_pack"
dest    = "~/Downloads"
hsl     = (0.5, 0.5, 0.5) # = rc.normalize_hsl(180, 50, 50)

rc.monochrome_pack(src, dest, name, hsl)
```
```python
src     = "packs/papirus-mini_multi"
name    = "my_multi_pack"
dest    = "~/Downloads"
palette = "palettes/dracula.json"

rc.multichrome_pack(src, dest, name, palette)
```

Or launch the GUI by running `python3 color_manager/gui.py` in a terminal from the project's root directory. The GUI will adopt your active theme. Dependencies: `colormath` and `tqdm`. For the GUI, `pygobject` (GTK bindings) must also be installed.


## Requests <a name="requests"></a>
Until the release of Color Manager, I will be taking requests for icon packs and recolorings. Simply submit a feature request here on the repository containing the following:
- The name of an open-source icon pack that will serve as the base look.
- For a monochromatic variant, a single hexadecimal value representing a color.
- For particular color palettes, a list of hexadecimal values or the name of a popular palette.

Please star the repository or consider donating, and I will upload your requested variant. Also consider showing the creators of the original icon packs some love.

Preview and download already fullfilled requests here:
<details>
<summary><b>Papirus-Mini Mono- and Multichromatic Variants</b></summary>
The original papirus set is massive (>100MB), so this version has been simplified, e.g. icons no longer have multiple versions for slightly different icon sizes. As a result, it only takes up ~10MB when zipped.

| Name  | Examples | Status |
| ----- | -------- | -------|
| Original | <img src="res/previews/papirus/original/colors.png" width="50"/>  <img src="res/previews/papirus/original/firefox.png" width="50"/> <img src="res/previews/papirus/original/vscode.png" width="50"/> <img src="res/previews/papirus/original/account.png" width="50"/>  <img src="res/previews/papirus/original/video.png" width="50"/> <img src="res/previews/papirus/original/git.png" width="50"/> | [Source](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme) |
| Nord | <img src="res/previews/papirus/nord/colors.png" width="50"/>  <img src="res/previews/papirus/nord/firefox.png" width="50"/> <img src="res/previews/papirus/nord/vscode.png" width="50"/> <img src="res/previews/papirus/nord/account.png" width="50"/>  <img src="res/previews/papirus/nord/video.png" width="50"/> <img src="res/previews/papirus/nord/git.png" width="50"/> | Finished |
| Dracula | <img src="res/previews/papirus/dracula/colors.png" width="50"/>  <img src="res/previews/papirus/dracula/firefox.png" width="50"/> <img src="res/previews/papirus/dracula/vscode.png" width="50"/> <img src="res/previews/papirus/dracula/account.png" width="50"/>  <img src="res/previews/papirus/dracula/video.png" width="50"/> <img src="res/previews/papirus/dracula/git.png" width="50"/> | Released |
| Catppuccin | <img src="res/previews/papirus/catppuccin/colors.png" width="50"/>  <img src="res/previews/papirus/catppuccin/firefox.png" width="50"/> <img src="res/previews/papirus/catppuccin/vscode.png" width="50"/> <img src="res/previews/papirus/catppuccin/account.png" width="50"/>  <img src="res/previews/papirus/catppuccin/video.png" width="50"/> <img src="res/previews/papirus/catppuccin/git.png" width="50"/> | Released |

| Name  | Examples | Status |
| ----- | -------- | -------|
| Galactic | <img src="res/previews/papirus/galactic/colors.png" width="50"/>  <img src="res/previews/papirus/galactic/firefox.png" width="50"/> <img src="res/previews/papirus/galactic/vscode.png" width="50"/> <img src="res/previews/papirus/galactic/account.png" width="50"/>  <img src="res/previews/papirus/galactic/video.png" width="50"/> <img src="res/previews/papirus/galactic/git.png" width="50"/> | Released |
| Strawberry | <img src="res/previews/papirus/strawberry/colors.png" width="50"/>  <img src="res/previews/papirus/strawberry/firefox.png" width="50"/> <img src="res/previews/papirus/strawberry/vscode.png" width="50"/> <img src="res/previews/papirus/strawberry/account.png" width="50"/>  <img src="res/previews/papirus/strawberry/video.png" width="50"/> <img src="res/previews/papirus/strawberry/git.png" width="50"/> | Released |
| Amazon | <img src="res/previews/papirus/amazon/colors.png" width="50"/>  <img src="res/previews/papirus/amazon/firefox.png" width="50"/> <img src="res/previews/papirus/amazon/vscode.png" width="50"/> <img src="res/previews/papirus/amazon/account.png" width="50"/>  <img src="res/previews/papirus/amazon/video.png" width="50"/> <img src="res/previews/papirus/amazon/git.png" width="50"/> | Finished |
| Pacific | <img src="res/previews/papirus/pacific/colors.png" width="50"/>  <img src="res/previews/papirus/pacific/firefox.png" width="50"/> <img src="res/previews/papirus/pacific/vscode.png" width="50"/> <img src="res/previews/papirus/pacific/account.png" width="50"/>  <img src="res/previews/papirus/pacific/video.png" width="50"/> <img src="res/previews/papirus/pacific/git.png" width="50"/> | Finished |
| Cobalt | <img src="res/previews/papirus/cobalt/colors.png" width="50"/>  <img src="res/previews/papirus/cobalt/firefox.png" width="50"/> <img src="res/previews/papirus/cobalt/vscode.png" width="50"/> <img src="res/previews/papirus/cobalt/account.png" width="50"/>  <img src="res/previews/papirus/cobalt/video.png" width="50"/> <img src="res/previews/papirus/cobalt/git.png" width="50"/> | Finished |
| Bumblebee | <img src="res/previews/papirus/bumblebee/colors.png" width="50"/>  <img src="res/previews/papirus/bumblebee/firefox.png" width="50"/> <img src="res/previews/papirus/bumblebee/vscode.png" width="50"/> <img src="res/previews/papirus/bumblebee/account.png" width="50"/>  <img src="res/previews/papirus/bumblebee/video.png" width="50"/> <img src="res/previews/papirus/bumblebee/git.png" width="50"/> | Released |
| Goldenrod | <img src="res/previews/papirus/goldenrod/colors.png" width="50"/>  <img src="res/previews/papirus/goldenrod/firefox.png" width="50"/> <img src="res/previews/papirus/goldenrod/vscode.png" width="50"/> <img src="res/previews/papirus/goldenrod/account.png" width="50"/>  <img src="res/previews/papirus/goldenrod/video.png" width="50"/> <img src="res/previews/papirus/goldenrod/git.png" width="50"/> | Released |
</details>


## Contribute <a name="contribute"></a>
If you are experienced with packaging projects such as this for easy distribution, please contact me.

---
**Legal Notice**: This repository, including any and all of its forks and derivatives, may NOT be used in the development or training of any machine learning model of any kind, without the explicit permission of the owner of the original repository.
