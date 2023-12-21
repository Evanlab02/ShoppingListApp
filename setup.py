"""Contains setup instructions for the project."""

from setuptools import find_packages, setup  # type: ignore


def parse_requirements(filename: str) -> list[str]:
    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()
    lines.pop(0)
    return [line.strip() for line in lines if line.strip()]


setup(
    name="ShoppingListApp-BE",
    version="0.13.0",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    include_package_data=True,
)
