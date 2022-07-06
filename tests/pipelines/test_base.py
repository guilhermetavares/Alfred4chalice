import uuid
from datetime import datetime
from unittest.mock import call, patch

import pytest
from freezegun import freeze_time

from alfred.pipelines.base import Pipeline, PipelineStep
from tests.db import Session

from .test_exceptions import PipelineException


class DummyStep(PipelineStep):
    def run(self):
        pass


@freeze_time("2022-07-06 15:50:00")
def test_pipeline_init():
    pipeline = Pipeline()

    assert type(pipeline.uuid) is uuid.UUID
    assert pipeline.started_at == datetime(2022, 7, 6, 15, 50, 0)
    assert pipeline.steps == []


@freeze_time("2022-07-06 15:50:00")
@patch("alfred.pipelines.base.logger.info")
def test_pipeline_run_without_exception(mock_log):
    session = Session()

    step = DummyStep
    pipeline = Pipeline()
    pipeline.steps = [step]
    pipeline.run(session=session)

    calls = [
        call(
            {
                "pipeline_id": str(pipeline.uuid),
                "pipeline": pipeline.__class__.__name__,
                "pipeline_step": None,
                "extra": {
                    "uuid": str(pipeline.uuid),
                    "started_at": str(datetime.now()),
                    "steps": str([DummyStep]),
                    "session": str(pipeline.session),
                },
            }
        ),
        call(
            {
                "pipeline_id": str(pipeline.uuid),
                "pipeline": pipeline.__class__.__name__,
                "pipeline_step": "DummyStep",
                "extra": {
                    "uuid": str(pipeline.uuid),
                    "started_at": str(datetime.now()),
                    "steps": str([DummyStep]),
                    "session": str(pipeline.session),
                },
            }
        ),
    ]

    mock_log.assert_has_calls(calls)


def test_pipeline_run_with_exception():
    class DummyStep(PipelineStep):
        def run(self):
            raise PipelineException

    session = Session()

    step = DummyStep
    pipeline = Pipeline()
    pipeline.steps = [step]
    with pytest.raises(PipelineException):
        pipeline.run(session=session)


def test_pipeline_step_run_with_exception():
    session = Session()

    step = PipelineStep
    pipeline = Pipeline()
    pipeline.steps = [step]
    with pytest.raises(NotImplementedError):
        pipeline.run(session=session)
