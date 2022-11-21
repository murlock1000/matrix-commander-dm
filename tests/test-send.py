#!/usr/bin/python3

r"""send.py.
This program uses the matrix-commander actions to send DM messages to a user.
It first creates a DM room if one does not exist.
"""

# isort: skip_file
# isort: off
import argparse
import asyncio
from datetime import datetime
import sys
import os

# importing matrix_commander module
try:
    # if installed via pip
    import matrix_commander  # nopep8 # isort: skip
    from matrix_commander import (
        main,
    )  # nopep8 # isort: skip
except:
    # if not installed via pip. if installed via 'git clone' or file download
    # appending a local path to sys.path
    sys.path.append("./matrix_commander")
    sys.path.append("../matrix_commander")
    # print(f"Expanded path is: {sys.path}")
    import matrix_commander  # nopep8 # isort: skip
    from matrix_commander import (
        main,
    )  # nopep8 # isort: skip

parser = argparse.ArgumentParser()

parser.add_argument("-u", required=True)

args, unknown = parser.parse_known_args()
users = [args.u]

for idx, arg in enumerate(sys.argv):
    if arg =="-u":
        sys.argv = sys.argv[:idx] + sys.argv[idx+2:]
        break

# set up some test arguments
#print(f"Running test program: {sys.argv[0]}")
#print(f"Current working directory is: {os.getcwd()}")
#print(f"Path is: {sys.path}")
#print(f"Arguments that are passed on to matrix-commander are: {sys.argv[1:]}")
sys.argv[0] = "matrix-commander"
cached_args = sys.argv[:]
sys.argv = sys.argv[:1]
#sys.argv.extend(["--debug"])

# Github Action Workflow differs from local test as Github Action env
# pipes a "" into the input of the program.
def execute_commander():
    #print(f"Testing with these arguments: {sys.argv}")
    try:
        ret = matrix_commander.main()
        if ret == 0:
            print("matrix_commander finished successfully.")
        else:
            print(
                f"matrix_commander failed with {ret} error{'' if ret == 1 else 's'}."
            )
    except Exception as e:
        print(f"Exception happened: {e}")
        ret = 99
    return ret

if ret:=execute_commander() !=0:
    exit(ret)

event_loop = asyncio.new_event_loop()
res_room = ""
async def main(users):
    
    client = matrix_commander.gs.client
    credentials = matrix_commander.gs.credentials
    
    rooms = await matrix_commander.determine_dm_rooms(users, client, credentials)
    if len(rooms) == 0:
        d = vars(matrix_commander.gs.pa)
        d["room_dm_create"] = users
        res_room = await matrix_commander.action_room_dm_create(client, credentials)
        res_rooms = [res_room]
    else:
        res_rooms = rooms

    # Close connections
    await matrix_commander.gs.client.close()
    return res_rooms

res_rooms = event_loop.run_until_complete(main(users))
room = res_rooms[-1]
event_loop.close()

sys.argv = cached_args
sys.argv.extend(["-r", room])

print(f"Arguments that are passed on to matrix-commander are: {sys.argv[:]}")
if ret:=execute_commander() !=0:
    exit(ret)

#os.remove(TESTFILE)
exit(ret)
