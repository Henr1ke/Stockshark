from adb.sim_adb.connector_ADB import ConnectorADB
from adb.sim_adb.constants import *


# TODO open_path, vs_friend, vs_bot return ?
class MenuNavigator:
    def __init__(self):
        self.connector = ConnectorADB()

    def open_app(self, app_path="com.chess/.home.HomeActivity"):
        self.connector.device.shell('am start -n ' + app_path)

    def vs_friend(self, name: str, white: bool = None, time_control: int = 10):
        assert time_control in [1, 3, 5, 10, 30], "O tempo de jogo tem de ser 1, 3, 5, 10 ou 30 minutos"
        con = self.connector

        def choose_time():
            con.tap_screen(*TIMEBOX)  # time box
            if time_control == 1:
                con.tap_screen(*TIME1)
            elif time_control == 3:
                con.tap_screen(*TIME3)
            elif time_control == 5:
                con.tap_screen(*TIME5)
            elif time_control == 10:
                con.tap_screen(*TIME10)
            elif time_control == 30:
                con.tap_screen(*TIME30)

        con.tap_screen(*PLAY1)  # play
        con.tap_screen(*VS_FRIEND)  # vs friend
        con.tap_screen(*SEARCH_BOX)  # search box
        con.input_text(name)  # write friend name
        con.tap_screen(*FRIEND)  # friend
        choose_time()  # choose time control
        if white is not None:
            con.tap_screen(*WHITE_PLAYER) if white else con.tap_screen(*BLACK_PLAYER)  # choose color
        con.tap_screen(*PLAY2)  # play

    def vs_bot(self, diff_lvl: int = 1, white: bool = None):
        con = self.connector

        # TODO Os bots vão mudar no final de maio, refazer isto depois
        def choose_bot():
            if diff_lvl == 1:
                con.tap_screen(*BOT1)
            elif diff_lvl == 2:
                con.tap_screen(*BOT2)
            elif diff_lvl == 3:
                con.tap_screen(*BOT3)
            elif diff_lvl == 4:
                con.tap_screen(*BOT4)
            elif diff_lvl == 5:
                con.tap_screen(*BOT5)
            con.tap_screen(*CONFIRM_BOT)  # confirm choosing

        con.tap_screen(*PLAY1)  # play
        con.tap_screen(*VS_BOT)  # vs computer
        choose_bot()  # choose enemy bot and
        if white is not None:
            con.tap_screen(*WHITE_BOT) if white else con.tap_screen(*BLACK_BOT)  # choose color
        con.tap_screen(*PLAY3)


if __name__ == "__main__":
    mn = MenuNavigator()
    # mn.vs_friend("AOlliveira01", white=True, time_control=5)
    # mn.open_app()
    # TODO Isto nao vai dar para ser chamado assim por causa do delay para abrir a app
    mn.vs_bot(3, white=False)
    # mn.vs_friend("AOlliveira01")
