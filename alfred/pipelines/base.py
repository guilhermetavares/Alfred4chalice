import json
import logging
import uuid
from datetime import datetime

logger = logging.getLogger("base")


class PipeLog:
    def log(self, hierarchy):
        extra = {}
        pipeline = self
        if hasattr(self, "pipeline"):
            pipeline = self.pipeline

        for key, value in vars(pipeline).items():
            try:
                extra[key] = json.dump(value)
            except TypeError:
                extra[key] = str(value)

        pipeline_step = None
        if pipeline.__class__.__name__ != self.__class__.__name__:
            pipeline_step = self.__class__.__name__

        logger.info(
            {
                "pipeline_id": str(pipeline.uuid),
                "pipeline": pipeline.__class__.__name__,
                "pipeline_step": pipeline_step,
                "extra": extra,
            }
        )


class PipelineStep(PipeLog):
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self):
        raise NotImplementedError


class Pipeline(PipeLog):
    steps = []

    def __init__(self):
        self.uuid = uuid.uuid4()
        self.started_at = datetime.utcnow()

    def run(self, session):
        self.session = session
        self.log(hierarchy="pipeline")

        for step_class in self.steps:
            step = step_class(pipeline=self)
            try:
                step.run()
                step.log(hierarchy="pipeline_step")
            except (NotImplementedError) as err:
                self.session.rollback()
                raise err
