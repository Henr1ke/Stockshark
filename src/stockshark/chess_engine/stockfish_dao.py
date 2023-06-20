import threading
import subprocess
from queue import Queue, Empty
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

        self._sf_output = Queue()

        self._line_reader = threading.Thread(target=StockFishDao._thread_read_contents,
                                             args=(self._stockfish, self._sf_output,),
                                             daemon=True)
        self._line_reader.start()

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
        try:
            line = self._sf_output.get_nowait()
            # line = self._sf_output.get(timeout=0.1)
            return line
        except Empty:
            return None

    def _read_response(self) -> Optional[str]:
        lines = []
        line = self._read_line()
        while line is not None:
            lines.append(line)
            line = self._read_line()
        return "\n".join(lines)

    @staticmethod
    def _thread_read_contents(sf_process: subprocess.Popen, sf_output: Queue) -> None:
        while True:
            if not sf_process.stdout:
                raise BrokenPipeError()
            if sf_process.poll() is not None:
                raise ConnectionError("The Stockfish process has crashed")
            line = sf_process.stdout.readline().strip()
            sf_output.put(line)

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
