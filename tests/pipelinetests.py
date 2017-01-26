import unittest

from saverpy import pipeline


class PipelineTests(unittest.TestCase):

    def test_should_execute_pipeline(self):
        func1 = lambda x: [x + n for n in range(1, 6)]
        func2 = lambda xs: [x for x in xs if x % 2 == 0]
        func3 = lambda xs: [x for x in xs if x > 0]
        func4 = lambda xs: [x / 2 for x in xs]

        pl = pipeline.Pipeline(func1, func2, func3, func4)
        result = pl(10)
        self.assertEqual(result, [6, 7])
