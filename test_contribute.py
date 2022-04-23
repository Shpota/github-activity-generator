import unittest
import contribute
from subprocess import check_output


class TestContribute(unittest.TestCase):

    def test_arguments(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(args.no_weekends)
        self.assertEqual(args.max_commits, 10)
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_contributions_per_day(self):
        args = contribute.arguments(['-nw'])
        self.assertTrue(1 <= contribute.contributions_per_day(args) <= 20)

    def test_commits(self):
        contribute.NUM = 11   # limiting the number only for unittesting
        contribute.main(['-nw',
                         '--user_name=sampleusername',
                         '--user_email=your-username@users.noreply.github.com',
                         '-mc=12',
                         '-fr=82',
                         '-db=10',
                         '-da=15'])
        self.assertTrue(1 <= int(check_output(
            ['git',
             'rev-list',
             '--count',
             'HEAD']
        ).decode('utf-8')) <= 20*(10 + 15))
