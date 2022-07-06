from alfred.pipelines.exceptions import PipelineException


def test_pipeline_exception():
    assert issubclass(PipelineException, Exception) is True
