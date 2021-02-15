import unittest
import contribute
from subprocess import check_output
import os

class TestContribute(unittest.TestCase):


    def test_arguments(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits,10)
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)
    
    def test_contributions_per_day(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_commits(self):
        contribute.main(['-nw','--user_name=sampleusername','--user_email=your-username@users.noreply.github.com'])
        self.assertTrue(1 <= int(check_output(['git', 'rev-list', '--count', 'HEAD']).decode('utf-8')) <=20*contribute.NUM_OF_DAYS)
        #git rev-list --count HEAD

        