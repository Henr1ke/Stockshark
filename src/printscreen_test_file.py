from chess.adb.dao_adb import DaoADB

if __name__ == '__main__':
    dao = DaoADB()
    dao.connect()
    dao.screenshot()
    pass
