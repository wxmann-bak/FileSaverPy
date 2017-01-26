import unittest

from saverpy import pipeline


class PipelineTests(unittest.TestCase):

    def setUp(self):
        func1 = lambda x: [x + n for n in range(1, 6)]
        func2 = lambda xs: [x for x in xs if x % 2 == 0]
        func3 = lambda xs: [x for x in xs if x > 0]
        func4 = lambda xs: [x / 2 for x in xs]

        self.four_step_pl = pipeline.Pipeline(func1, func2, func3, func4)

    def test_should_execute_pipeline(self):
        result = self.four_step_pl(10)
        self.assertEqual(result, [6, 7])

    def test_should_execute_empty_pipeline(self):
        pl = pipeline.Pipeline()
        self.assertEqual(pl(10), 10)

    def test_should_execute_pipeline_multiple_times(self):
        result1 = self.four_step_pl(10)
        result2 = self.four_step_pl(20)
        self.assertEqual(result1, [6, 7])
        self.assertEqual(result2, [11, 12])
