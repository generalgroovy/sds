from types import SimpleNamespace

import pytest

from coop_navigation_sds import smoke


@pytest.mark.parametrize("outcome", ["unsatisfied", "semi_satisfied", "unknown", None])
def test_smoke_rejects_incomplete_task_outcomes(monkeypatch, outcome):
    result = SimpleNamespace(extra={"conversation_outcome": outcome})
    monkeypatch.setattr(smoke, "conversation_worker", lambda *_: (result, {"run_dir": "results/failed-run"}))
    with pytest.raises(RuntimeError, match="results/failed-run"):
        smoke.run_smoke()


def test_smoke_preserves_satisfied_result_and_paths(monkeypatch):
    result = SimpleNamespace(extra={"conversation_outcome": "satisfied"})
    paths = {"run_dir": "results/passed-run"}
    monkeypatch.setattr(smoke, "conversation_worker", lambda *_: (result, paths))
    assert smoke.run_smoke() == (result, paths)


def test_direct_smoke_cli_returns_failure_without_traceback(monkeypatch, capsys):
    def fail(_):
        raise RuntimeError("Expected satisfied outcome; inspect results/failed-run")
    monkeypatch.setattr(smoke, "run_smoke", fail)
    assert smoke.main([]) == 1
    assert "results/failed-run" in capsys.readouterr().err
