"""Contains the setup configuration for the project."""

from setuptools import find_packages, setup  # type: ignore

version = open("version.txt").read().strip()


def read_requirements() -> list[str]:
    """Read the requirements from the requirements.txt file."""
    lines = []
    with open("requirements.txt") as req:
        lines = req.readlines()
        lines.pop(0)
    return [line.strip() for line in lines]


include_files = [
    "shoppingapp",
    "shoppingapp/*",
    "shoppingapp/**/*",
    "authentication",
    "authentication/*",
    "authentication/**/*",
    "stores",
    "stores/*",
    "stores/**/*",
]

exclude_files = [
    "**/tests/*",
    "tests/*",
]

setup(
    name="shoppingapp-be",
    version=version,
    install_requires=read_requirements(),
    packages=find_packages(
        where=".",
        include=include_files,
        exclude=exclude_files,
    ),
    entry_points={
        "console_scripts": [
            "shoppingapp = shoppingapp.config.asgi:main",
            "shoppingapp-int = shoppingapp.config.int_config:main",
        ]
    },
    include_package_data=True,
)
