#!/usr/bin/env python
import argparse
import os
from datetime import datetime
from datetime import timedelta
from random import randint
from subprocess import Popen
import sys


def main(def_args=sys.argv[1:]):
    """
    Main function to parse arguments, create a new Git repository, and generate commits
    based on specified options. The function configures the repository, handles custom
    user settings, and iterates over a date range to add commits on selected days.
    """

    
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')

    # Use repository name as directory name if provided
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]

    # Validate date range inputs
    no_weekends = args.no_weekends
    frequency = args.frequency
    days_before = args.days_before
    if days_before < 0:
        sys.exit('days_before must not be negative')
    days_after = args.days_after
    if days_after < 0:
        sys.exit('days_after must not be negative')

    # Create and initialize the repository directory
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    # Set Git user configuration if specified
    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    # Define the starting date for commits
    start_date = curr_date.replace(hour=20, minute=0) - timedelta(days_before)

    # Loop through each day in the specified date range
    for day in (start_date + timedelta(n) for n
                in range(days_before + days_after)):
        # Check frequency and weekend setting to decide if commits should be made on a given day            
        if (not no_weekends or day.weekday() < 5) \
                and randint(0, 100) < frequency:
            for commit_time in (day + timedelta(minutes=m)
                                for m in range(contributions_per_day(args))):
                contribute(commit_time)

    # Add remote repository and push commits if a repository URL is provided
    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' +
          '\x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    """
    Creates a commit at a specific date and time by appending to README.md,
    staging the change, and setting the commit date.
    """

    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    """
    Execute a shell command and wait for it to complete. 
    This function wraps subprocess.Popen to run Git commands synchronously.
    """
    
    Popen(commands).wait()


def message(date):
    """
    Formats a standardized commit message with a timestamp.
    """
    
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    """
    Determines the number of commits to make on a single day, within the range set
    by `max_commits` (capped at 1-20).
    """
    
    max_c = args.max_commits
    if max_c > 20:
        max_c = 20
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments(argsval):
    """
    Parses command-line arguments to configure the script, including commit frequency,
    max commits per day, repository URL, commit range, and whether to skip weekends.
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends',
                        required=False, action='store_true', default=False,
                        help="""do not commit on weekends""")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        required=False, help="""Defines the maximum amount of
                        commits a day the script can make. Accepts a number
                        from 1 to 20. If N is specified the script commits
                        from 1 to N times a day. The exact number of commits
                        is defined randomly for each day. The default value
                        is 10.""")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        required=False, help="""Percentage of days when the
                        script performs commits. If N is specified, the script
                        will commit N%% of days in a year. The default value
                        is 80.""")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link on an empty non-initialized remote git
                        repository. If specified, the script pushes the changes
                        to the repository. The link is accepted in SSH or HTTPS
                        format. For example: git@github.com:user/repo.git or
                        https://github.com/user/repo.git""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-db', '--days_before', type=int, default=365,
                        required=False, help="""Specifies the number of days
                        before the current date when the script will start
                        adding commits. For example: if it is set to 30 the
                        first commit date will be the current date minus 30
                        days.""")
    parser.add_argument('-da', '--days_after', type=int, default=0,
                        required=False, help="""Specifies the number of days
                        after the current date until which the script will be
                        adding commits. For example: if it is set to 30 the
                        last commit will be on a future date which is the
                        current date plus 30 days.""")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
