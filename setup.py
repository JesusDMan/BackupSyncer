from setuptools import setup, find_packages

setup(
    name="backup_syncer",
    version="2.5",
    packages=find_packages(exclude=["tests*"]),
    description="A files syncer for easy local backups!",
    long_description=open("README.md").read(),
    install_requires=[
        "shutils",
        "langdetect",
    ],
    url="https://github.com/JesusDMan/JesusDMan",
    author="JesusDMan",
    entry_points={"console_scripts": ["bsync = backup_syncer.bin.sync_files:main"]},
)
