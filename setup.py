from setuptools import setup, find_packages


def read_requirements(path="requirements.txt"):
    """Read requirements file and return a list."""
    with open(path, "r", encoding="utf8") as file:
        return [line.strip() for line in file.readlines() if not line.startswith("#")]


setup(
    name="ghs",
    version="1.0.0",
    description="GitHub scripts",
    author="AmLight Team",
    author_email="no-reply@amlight.net",
    keywords="GitHub scripts",
    url="http://github.com/amlight/gh_scripts",
    packages=find_packages(exclude=["tests"]),
    license="MIT",
    install_requires=read_requirements(),
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    entry_points={"console_scripts": "ghs=ghs.bin.cli:main"},
    zip_safe=False,
)
