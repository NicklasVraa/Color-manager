from setuptools import setup, find_packages

setup(
    setup_requires=['wheel'],
    name="color_manager_nv",
    version="0.1.0",
    author="Nicklas Vraa",
    author_email="nicklasvraa@proton.me",
    description="A package for recoloring icon and wallpaper packs and desktop themes",
    url="https://github.com/nicklasvraa/color-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages(include=["color_manager", "color_manager.*"]),
    include_package_data=True,
    package_data={
        "color_manager": ["palettes/*.json"],
    },
    exclude=["tests", "packs"],
    install_requires=[
        "colormath",
        "tqdm",
        "pillow"
    ],
)
