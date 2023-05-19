import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--phone_model', type=str, required=True, help='Which smartphone model the ADB connects to')
subparser = parser.add_subparsers(dest='command')

player = subparser.add_parser('player')
player.add_argument("--username", type=str, required=True)
player.add_argument("--play-as-whites", type=bool, required=False)
player.add_argument("--duration", type=int, required=False)

computer = subparser.add_parser('computer')
computer.add_argument("--diff-lvl", type=int, required=True)
computer.add_argument("--play-as-whites", type=bool, required=False)

args = parser.parse_args()
print(args)
