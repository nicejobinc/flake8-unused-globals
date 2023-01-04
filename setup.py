from setuptools import setup

with open("__VERSION__") as f:
    version = f.read().strip()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read().strip()

setup(
    name="flake8-unused-globals",
    version=version,
    python_requires=">=3.10,<3.11",
    include_package_data=True,
    install_requires=install_requires,
    py_modules=["flake8_unused_globals"],
    entry_points={"flake8.extension": "UUG001 = flake8_unused_globals:Plugin"},
    long_description=long_description,
)
