from setuptools import setup, find_packages

setup(
    name="BackupSyncer",
    version="2.1",
    packages=find_packages(exclude=["tests*"]),
    description="A files syncer for easy local backups!",
    long_description=open("README.md").read(),
    install_requires=[
        "shutils",
        "langdetect",
    ],
    url="https://github.com/JesusDMan/JesusDMan",
    author="JesusDMan",
    entry_points={"console_scripts": ["sync = BackupSyncer.bin.sync_files:main"]},
)
