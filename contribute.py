#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen
import sys
import shutil  # Added to handle directory cleanup


def main(def_args=sys.argv[1:]):
    # Parse and validate command-line arguments
    args = arguments(def_args)

    # Change: Parse and validate explicit start and end dates.
    # Reason: Fix the issue where the script could not handle exact date ranges.
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        sys.exit("Invalid date format. Use YYYY-MM-DD for --start_date and --end_date.")

    # Change: Ensure start_date <= end_date
    # Reason: To prevent incorrect ranges and improve input validation.
    if start_date > end_date:
        sys.exit("Start date must be earlier than or equal to the end date.")

    # Display date range for confirmation
    print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
    print(f"End Date: {end_date.strftime('%Y-%m-%d')}")
    proceed = input("Proceed with these dates? (yes/no): ").strip().lower()
    if proceed != 'yes':
        print("Operation canceled.")
        sys.exit(0)

    # Generate repository directory name
    directory = 'repository-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email

    # Change: Handle dynamic directory names based on the repository name
    # Reason: To ensure the script doesn’t overwrite directories.
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]

    # Change: Cleanup and reinitialize directories automatically
    # Reason: To avoid manual intervention and improve user experience.
    if os.path.exists(directory):
        print(f"Directory {directory} already exists. Cleaning it up...")
        shutil.rmtree(directory)
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    # Set git user configuration if provided
    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])
    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    # Commit generation loop
    current_date = start_date
    no_weekends = args.no_weekends
    frequency = args.frequency

    # Change: Ensure the loop operates strictly within start_date and end_date
    # Reason: To fix the issue where the script continued beyond the specified range.
    while current_date <= end_date:
        if (not no_weekends or current_date.weekday() < 5) and randint(0, 100) < frequency:
            for commit_time in (current_date + timedelta(minutes=m) for m in range(contributions_per_day(args))):
                contribute(commit_time)
        current_date += timedelta(days=1)

    # Push changes to remote repository if specified
    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' +
          '\x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    # Generate commit messages with specified dates
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    # Added error handling to catch command execution errors
    try:
        Popen(commands).wait()
    except Exception as e:
        sys.exit(f"Error running command {' '.join(commands)}: {e}")


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    max_c = args.max_commits
    if max_c > 20:
        max_c = 20
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--start_date', type=str, required=True,
                        help="""The start date for commits in YYYY-MM-DD format.
                        For example: 2019-10-01.""")
    parser.add_argument('-ed', '--end_date', type=str, required=True,
                        help="""The end date for commits in YYYY-MM-DD format.
                        For example: 2020-11-30.""")
    parser.add_argument('-nw', '--no_weekends',
                        required=False, action='store_true', default=False,
                        help="""Do not commit on weekends.""")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        required=False, help="""Defines the maximum number of
                        commits a day the script can make. Accepts a number
                        from 1 to 20. The default value is 10.""")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        required=False, help="""Percentage of days when the
                        script performs commits. Default is 80.""")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link to the remote repository.
                        Example: git@github.com:user/repo.git""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.""")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
