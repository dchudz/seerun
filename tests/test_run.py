import logging
from showvalues.run import run


def test_baz(caplog):
    logging.warn('hi')
    for record in caplog.records:
        assert record.levelname != 'CRITICAL'
    print(caplog.text)
    assert 'hi' in caplog.text


def test_run_logs_exceptions(caplog):
    run('{}["a"]', [], {})
    assert 'KeyError' in caplog.text


def test_run_logs_system_exit_1(caplog):
    run('raise SystemExit(1)', [], {})
    assert 'SystemExit' in caplog.text

def test_run_no_log_system_exit_0(caplog):
    run('raise SystemExit(0)', [], {})
    assert 'SystemExit' not in caplog.text
