#!/usr/bin/env python3

import os
from redminelib import Redmine
import sys
import subprocess
import re

MESSAGE_REGEX = "(RM[#-]?)([0-9]{4,7})"
BRANCHNAME_REGEX = "(RM[#-]?)([0-9]{4,7})-"
REDMINE_URL = os.getenv("REDMINE_URL")
REDMINE_TOKEN = os.getenv("REDMINE_TOKEN")


def git_addr_trim(addr):
    after_trim = addr.replace("http://", "")
    after_trim = after_trim.replace("https://", "")
    after_trim = after_trim.replace("git@", "")
    after_trim = after_trim.replace("ssh://", "")
    return after_trim


def git_addr_repo(addr, commit_hash):
    trim = git_addr_trim(addr)
    if re.findall("(\.git)", trim):
        REPO_URL_SCHEMA = os.getenv("REPO_URL_SCHEMA", "http")
        git_addr = trim.split(":", 1)
        url_syntax = "{}://{}/{}/commit/{}".format(
            REPO_URL_SCHEMA, git_addr[0], git_addr[1].replace(".git",""), commit_hash
        )
    else:
        aws_region = os.getenv("AWS_REGION", "eu-west-1")
        repo_name = trim.split("/", 5)[3]
        url_syntax = "https://console.aws.amazon.com/codesuite/codecommit/repositories/{}/commit/{}?region={}".format(
            repo_name, commit_hash, aws_region
        )
    return url_syntax


def current_branch_name():
    return (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .decode(sys.stdout.encoding)
        .strip()
    )


def current_commithash():
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD"])
        .decode(sys.stdout.encoding)
        .strip()
    )


def current_origin():
    return (
        subprocess.check_output(["git", "remote", "get-url", "origin"])
        .decode(sys.stdout.encoding)
        .strip()
    )


def get_redmine_issue(branch_name):
    match = re.findall(BRANCHNAME_REGEX, str(branch_name))
    if match and match[0]:
        return match[0]
    return


def valid_commit_message(message):
    if not re.match(MESSAGE_REGEX, str(message)):
        # ToDo - code to check branch is not created yet
        # name = current_branch_name()
        # issue_number = get_redmine_issue(name)
        print("ERROR: Missing RedMine Issue in commmit message.")
        print("Hint: MR#12345  bla bla bla your Commit message.")
        return False
    return True


def update_redmine_task(message):
    match = re.search(MESSAGE_REGEX, message)
    issue_id = match.group(2)
    try:
        redmine = Redmine(REDMINE_URL, key=REDMINE_TOKEN)
        issue = redmine.issue.get(issue_id)
        print("RM issue updated: {}".format(issue))
    except:
        print(
            "Issue with connection to Redmine. Did you export REDMINE_TOKEN & REDMINE_URL envs?"
        )
        sys.exit(1)
    git_addr_to_repo = git_addr_repo(str(current_origin()), str(current_commithash()))
    note = "*Branch*: __{}__ | {}\n __{}__".format(
        str(current_branch_name()), git_addr_to_repo, message
    )
    redmine.issue.update(issue_id, notes=note)
    return


def main():
    """Main function."""
    message_file = sys.argv[1]

    try:
        txt_file = open(message_file, "r")
        commit_message = txt_file.read()
    finally:
        txt_file.close()

    if valid_commit_message(commit_message):
        update_redmine_task(commit_message)
        sys.exit(0)
    else:
        sys.exit(" ERROR - invalid commit message ")


if __name__ == "__main__":
    main()
