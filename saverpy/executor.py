from saverpy.pipeline import Pipeline


class SavePipeline(Pipeline):
    def __init__(self, converter, filter, saver, reporter):
        super(SavePipeline, self).__init__(converter, filter, saver, reporter)