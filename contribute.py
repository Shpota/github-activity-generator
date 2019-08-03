#!/usr/bin/env python
import argparse
import os
from datetime import datetime
from datetime import timedelta
from random import randint
from subprocess import Popen


def main():
    args = arguments()
    current_datetime = datetime.now()
    directory = 'repository-' + current_datetime.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]

    os.mkdir(directory)
    perform(['git', 'init'], directory)
    start_date = current_datetime.replace(hour=20, minute=0) - timedelta(366)
    for day in (start_date + timedelta(n) for n in range(366)):
        if randint(0, 100) < args.frequency:
            for commit_time in (day + timedelta(minutes=m) for m in range(contributions_per_day(args))):
                contribute(commit_time, directory)

    if repository is not None:
        perform(['git', 'remote', 'add', 'origin', repository], directory)
        perform(['git', 'push', '-u', 'origin', 'master'], directory)

    print('\nRepository generation \x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date, directory):
    with open(os.path.join(directory, 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    perform(['git', 'add', '.'], directory)
    perform(['git', 'commit', '-m', '"%s"' % message(date), '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')], directory)


def perform(commands, context_dir):
    Popen(commands, cwd=context_dir).wait()


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    max_c = args.max_commits
    if max_c > 20:
        max_c = 20
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mc', '--max_commits', type=int, default=10, required=False,
                        help="""Defines the maximum amount of commits a day the script can make.
                        Accepts a number from 1 to 20. If N is specified the script commits
                        from 1 to N times a day. The exact number of commits is defined randomly 
                        for each day. The default value is 10.""")
    parser.add_argument('-fr', '--frequency', type=int, default=80, required=False,
                        help="""Percentage of days when the script performs commits. If N is specified,
                        the script will commit N%% of days in a year. The default value is 80.""")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link on an empty non-initialized remote git repository. If specified, 
                        the script pushes the changes to the repository. The link is accepted in SSH  
                        or HTTPS format. For example: git@github.com:user/repo.git or 
                        https://github.com/user/repo.git""")
    return parser.parse_args()


if __name__ == "__main__":
    main()
