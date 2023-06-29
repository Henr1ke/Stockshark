from queue import Queue, Empty
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from typing import Optional, List

from stockshark.util.move import Move


class StockfishDao:
    def __init__(self, path: str = "../../stockfish/stockfish-windows-2022-x86-64-modern.exe") -> None:

        self._path = path
        self._stockfish = Popen(
            self._path,
            universal_newlines=True,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
        )

        self._sf_output = Queue()

        def thread_read_contents(sf_process: Popen, sf_output: Queue) -> None:
            while True:
                if not sf_process.stdout:
                    raise BrokenPipeError()
                if sf_process.poll() is not None:
                    raise ConnectionError("The Stockfish process has crashed")
                line = sf_process.stdout.readline().strip("\n")
                sf_output.put(line)

        self._line_reader = Thread(target=thread_read_contents,
                                   args=(self._stockfish, self._sf_output,),
                                   daemon=True)
        self._line_reader.start()
        self._read_line()  # Clear Queue

        self._is_closing = False

        self._is_ready()
        self._send_command("uci")
        response = self._read_response(5, "uciok")
        if "uciok" not in response:
            raise ChildProcessError('No "uciok" message recieved from stockfish')

    def _send_command(self, command: str) -> None:
        if not self._stockfish.stdin:
            raise BrokenPipeError()
        if self._stockfish.poll() is None and not self._is_closing:
            self._stockfish.stdin.write(f"{command}\n")
            self._stockfish.stdin.flush()
            if command == "quit":
                self._is_closing = True

    def _read_line(self, timeout: float = 0.1) -> Optional[str]:
        try:
            line = self._sf_output.get(timeout=timeout)
            return line
        except Empty:
            return None

    def _get_response_lines(self, timeout: float = 0.1, end_str: Optional[str] = None) -> List[str]:
        lines = []

        line = self._read_line(timeout)
        if line is None:
            return lines

        while line is not None:
            lines.append(line)

            if end_str is not None and end_str in line:
                break

            line = self._read_line(timeout)

        return lines

    def _read_response(self, timeout: float = 0.1, end_str: Optional[str] = None) -> Optional[str]:
        lines = self._get_response_lines(timeout, end_str)
        return "\n".join(lines)

    def _is_ready(self) -> bool:
        self._send_command("isready")
        response = self._read_response(5, "readyok")
        return response is not None and "readyok" in response

    def new_game(self, fen: Optional[str] = None) -> bool:
        if fen is not None:
            self._send_command(f"position fen {fen}")
        else:
            self._send_command("ucinewgame")
        return self._is_ready()

    def close(self) -> None:
        self._send_command("quit")

    def is_process_running(self) -> bool:
        return self._stockfish.poll() is None

    def get_fen(self) -> Optional[str]:
        self._send_command("d")
        response = self._read_response()
        if response is None:
            return None
        search_word = "Fen: "
        start_idx = response.find(search_word) + len(search_word)
        end_idx = response.find("\n", start_idx)
        return response[start_idx:end_idx]

    def get_board_repr(self) -> Optional[str]:
        self._send_command("d")
        response = self._read_response()
        if response is None:
            return None
        search_word = "Fen: "
        idx = response.find(search_word)
        return response[:idx].strip("\n")

    def make_moves(self, fen_string: str, moves: List[str]):
        self._send_command(f"position fen {fen_string} moves {' '.join(moves)}")

    def make_move(self, fen_string: str, move: str):
        self.make_moves(fen_string, [move])

    def get_available_moves(self) -> List[str]:
        self._send_command("go perft 1")
        response_lines = self._get_response_lines(end_str="Nodes searched: ")
        if len(response_lines) == 0:
            return []

        moves = []
        for i in range(len(response_lines) - 2):
            line = response_lines[i]
            colon_idx = line.find(":")
            moves.append(line[:colon_idx].strip())

        return moves

    def __del__(self) -> None:
        if self._stockfish.poll() is None and not self._is_closing:
            self._send_command("quit")
            while self._stockfish.poll() is None:
                pass


if __name__ == '__main__':
    sf_dao = StockfishDao()
    success = sf_dao.new_game()
    f = sf_dao.get_fen()
    board_repr = sf_dao.get_board_repr()
    print(f)
    print(board_repr)

    available_moves = sf_dao.get_available_moves()
    for move in available_moves:
        print(move)
