import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harmony-device",
    version="0.0.8",
    author="Caleb Hester",
    author_email="naclcaleb@gmail.com",
    description="Harmony - A standard protocol for controlling IoT devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naclcaleb/Harmony",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
