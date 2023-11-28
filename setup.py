from setuptools import setup, find_packages

setup(
    name="backup_syncer",
    version="2.5",
    packages=find_packages(exclude=["tests*"]),
    description="A local backups creator and syncer, for easy backup handling!",
    long_description=open("README.md").read(),
    install_requires=["shutils", "langdetect", "tqdm"],
    url="https://github.com/JesusDMan/BackupSyncer",
    author="JesusDMan",
    entry_points={"console_scripts": ["bsync = backup_syncer.bin.sync_files:main"]},
)
