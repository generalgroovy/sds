import subprocess
import sys
from types import SimpleNamespace

import pytest

from coop_navigation_sds.__main__ import main


def test_help_does_not_import_the_experiment_runtime():
    code = """
import sys
from coop_navigation_sds.__main__ import main
try:
    main(['--help'])
except SystemExit as error:
    assert error.code == 0
assert 'coop_navigation_sds.app' not in sys.modules
assert 'torch' not in sys.modules
"""
    result = subprocess.run([sys.executable, '-c', code], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert '--smoke' in result.stdout


def test_output_option_is_not_silently_ignored(capsys):
    with pytest.raises(SystemExit) as error:
        main(['--results-dir', 'example'])
    assert error.value.code == 2
    assert 'applies to --smoke' in capsys.readouterr().err


def test_smoke_failure_is_actionable(monkeypatch, capsys):
    def fail(_):
        raise PermissionError('Choose a writable results folder.')
    monkeypatch.setitem(sys.modules, 'coop_navigation_sds.smoke', SimpleNamespace(run_smoke=fail))
    assert main(['--smoke']) == 1
    assert 'Smoke check failed: Choose a writable results folder.' in capsys.readouterr().err


def test_smoke_reports_outcome_and_requested_folder(monkeypatch, capsys):
    calls = []
    def run(folder):
        calls.append(folder)
        return SimpleNamespace(extra={'conversation_outcome': 'success'}), {'run_dir': 'demo/run'}
    monkeypatch.setitem(sys.modules, 'coop_navigation_sds.smoke', SimpleNamespace(run_smoke=run))
    assert main(['--smoke', '--results-dir', 'demo']) == 0
    assert calls == ['demo']
    assert 'Smoke result: success' in capsys.readouterr().out
