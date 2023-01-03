from setuptools import setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="flake8-unused-globals",
    version="0.1.0",
    python_requires=">=3.10,<3.11",
    include_package_data=True,
    install_requires=install_requires,
    py_modules=["flake8_unused_globals"],
    entry_points={"flake8.extension": "UUG001 = flake8_unused_globals:Plugin"},
)
