from BackupSyncer.file_syncer import setup_file_shit
from BackupSyncer.file_syncer.syncer import Syncer


def main():
    syncer = Syncer(r"D:\ProgramFiles\sync_conf\src_dst_setup.txt")
    syncer.use_setup()
    syncer.print_sync()
    syncer.make_change_in_action()
    syncer.finale_sync()
    input("Sync was successful! Press enter to exit")
