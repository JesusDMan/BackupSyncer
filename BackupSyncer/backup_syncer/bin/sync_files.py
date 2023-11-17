from backup_syncer.modules.syncer import Syncer


def main():
    syncer = Syncer(r"D:\ProgramFiles\sync_conf\src_dst_setup.txt")
    syncer.use_setup()
    syncer.print_sync()
    syncer.make_changes_in_sync_actions()
    syncer.perform_sync()
    input("Sync was successful! Press enter to exit")


if __name__ == "__main__":
    main()
