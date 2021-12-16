#!/usr/bin/env python3

import os
import re
import subprocess
import sys

MESSAGE_REGEX = "(RM[#-]?)([0-9]{4,7})"
BRANCHNAME_REGEX = "(RM[#-]?)([0-9]{4,7})-"
REDMINE_URL = os.getenv("REDMINE_URL")
REDMINE_TOKEN = os.getenv("REDMINE_TOKEN")


def current_branch_name():
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode(sys.stdout.encoding).strip()


def get_redmine_issue(branch_name):
    match = re.findall(BRANCHNAME_REGEX, str(branch_name))
    if match and match[0]:
        return match[0]
    return


def valid_commit_message(message):
    if not re.match(MESSAGE_REGEX, str(message)):
        if not re.match(BRANCHNAME_REGEX, str(current_branch_name())):
            return False
    return True


def main():
    message_file = sys.argv[1:]
    if not message_file:
        message_file = ".git/COMMIT_EDITMSG"

    try:
        txt_file = open(message_file, "r")
        commit_message = txt_file.read()
    finally:
        txt_file.close()

    if not valid_commit_message(commit_message):
        print(" ERROR: Missing RedMine Issue in commmit message.")
        print("   Hint: MR#12345  bla bla bla your Commit message.")
        sys.exit(1)


if __name__ == "__main__":
    main()
