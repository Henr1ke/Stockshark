import threading
import subprocess
import time
from typing import List, Optional


class StockFishDao:
    def __init__(self, path: str = "../../stockfish/stockfish-windows-2022-x86-64-modern.exe") -> None:

        self._path = path
        self._stockfish = subprocess.Popen(
            self._path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self._new_lines = []
        self._new_lines_lock = threading.Lock()

        self._line_reader = threading.Thread(target=StockFishDao._thread_read_contents,
                                             args=(self._stockfish, self._new_lines, self._new_lines_lock,),
                                             daemon=True)
        self._line_reader.start()
        with self._new_lines_lock:
            self._new_lines.clear()

        self._is_closing = False

        self._send_command("uci")
        response = self._read_response()
        print(response)

    def _send_command(self, command: str) -> None:
        if not self._stockfish.stdin:
            raise BrokenPipeError()
        if self._stockfish.poll() is None and not self._is_closing:
            self._stockfish.stdin.write(f"{command}\n")
            self._stockfish.stdin.flush()
            if command == "quit":
                self._is_closing = True
            time.sleep(0.1)

    def _read_line(self) -> Optional[str]:
        with self._new_lines_lock:
            if len(self._new_lines) > 0:
                return self._new_lines.pop(0)

    def _read_response(self) -> Optional[str]:
        with self._new_lines_lock:
            if len(self._new_lines) > 0:
                return "".join(self._new_lines)

    @staticmethod
    def _thread_read_contents(sf_process: subprocess.Popen, new_lines: List[str],
                              new_lines_lock: threading.Lock) -> None:
        while True:
            if not sf_process.stdout:
                raise BrokenPipeError()
            if sf_process.poll() is not None:
                raise ConnectionError("The Stockfish process has crashed")
            line = sf_process.stdout.readline().strip()
            with new_lines_lock:
                new_lines.append(line)

    def close(self):
        self._send_command("quit")

    def is_process_running(self):
        return self._stockfish.poll() is None

    def __del__(self) -> None:
        if self._stockfish.poll() is None and not self._is_closing:
            self._send_command("quit")
            while self._stockfish.poll() is None:
                pass


if __name__ == '__main__':
    sf_dao = StockFishDao()
