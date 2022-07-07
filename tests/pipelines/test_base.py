import uuid
from datetime import datetime
from unittest.mock import Mock, call, patch

import pytest
from freezegun import freeze_time

from alfred.pipelines.base import Pipeline, PipelineStep


class DummyStep(PipelineStep):
    def run(self):
        pass


@freeze_time("2022-07-06 15:50:00")
def test_pipeline_init():
    session = Mock()
    pipeline = Pipeline(session=session)

    assert type(pipeline.uuid) is uuid.UUID
    assert pipeline.started_at == datetime(2022, 7, 6, 15, 50, 0)
    assert pipeline.steps == []


@freeze_time("2022-07-06 15:50:00")
@patch("alfred.pipelines.base.logger.info")
def test_pipeline_run_without_exception(mock_log):
    session = Mock()

    step = DummyStep
    pipeline = Pipeline(session=session)
    pipeline.steps = [step]
    pipeline.run()

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


def test_pipeline_step_run_with_exception():
    session = Mock()

    step = PipelineStep
    pipeline = Pipeline(session=session)
    pipeline.steps = [step]
    with pytest.raises(NotImplementedError):
        pipeline.run()
