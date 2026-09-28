# CoopNavigationSDS

A research framework for evaluating cooperative speech dialogue systems. Two
agents negotiate a public-transport route: the caller reveals travel constraints,
and the dialogue system proposes and revises grounded routes. The framework
records each language, speech, understanding and decision phase, then calculates
metrics from the saved evidence.

Compare models and speech conditions with declared experiment jobs and paired
text controls. A plausible conversation alone does not establish task success:
routes and constraints are checked against the generated transport network.

## Start here

Use a supported Windows or Linux environment with Python 3.14 and the project
requirements installed. Provider-specific environments and model downloads are
separate from the deterministic pipeline check. Follow the platform-specific
[setup instructions](RESEARCH_GUIDE.md#10-setup) for a new checkout.

From the repository root:

```bash
python -m coop_navigation_sds --help
python -m coop_navigation_sds --smoke
```

`--help` does not load the experiment runtime. The smoke run uses deterministic
agents and file-backed speech fixtures, without model downloads or audio
playback. It writes a result directory and checks that the expected task outcome
is satisfied. It does not measure full-model performance.

Choose a different smoke output root when needed:

```bash
python -m coop_navigation_sds --smoke --results-dir results/smoke
```

## Run an experiment

| Task | Entry point |
|---|---|
| Configure one run in the startup GUI | `python -m coop_navigation_sds` |
| Reproduce a scripted single run | `python scripts/run_from_script_config.py` |
| Compare declared factors and repetitions | [Job and batch guide](RESEARCH_GUIDE.md#12-job-files-and-batch-execution) |
| Run focused Agent B model comparisons | [Agent B experiments](jobs/agent_b_llm/README.md) |
| Compare completed runs | [Comparison and visualization](RESEARCH_GUIDE.md#13-batch-comparison-and-visualization) |

The GUI requires Tk and a graphical session. It closes before the experiment
starts. Headless batches use the same experiment runtime without the GUI.
Prepare the selected model and speech providers before running their conditions;
the system must not silently substitute a different backend.

## Read the results

Each execution writes a self-contained directory under its configured result
root. Start with `run_summary.json`, then use:

- `conditions.jsonl` for condition factors and outcomes;
- `metrics_long.csv` for per-metric analysis and plotting;
- `metrics_wide.csv` for condition-level comparisons;
- the protocol, transcript and `metric_inputs.json` for underlying evidence.

Keep a run directory together when moving or archiving it. Manifest paths are
relative to that directory. See the [result schema](RESEARCH_GUIDE.md#16-result-structure).
Configured condition counts are experiment designs, not completed-run counts;
read actual completion and success from each run's artifacts.

## Documentation

| Topic | Source of truth |
|---|---|
| Complete specification, configuration and operating guide | [Research guide](RESEARCH_GUIDE.md) |
| Transport task and constraints | [Network contract](RESEARCH_GUIDE.md#7-transport-network-and-dialogue-task), [diagram](docs/network_graph.svg) |
| Measurement definitions | [Metric reference](METRIC_REFERENCE.md) |
| Metric methodology and evidence limits | [Automatic metrics specification](AUTOMATIC_METRICS_SPEC.md) |
| Package modules and functions | [Generated API reference](API_REFERENCE.md) |
| Historical reconstruction requirements | [Rebuild specification](REBUILD_SPEC.md) |

The full specification formerly in this README is preserved in the research
guide. Keep normative configuration and network descriptions there rather than
duplicating them in quick-start documents.

## Validate changes

With project and test dependencies installed:

```bash
python -m pytest tests/test_cli_entrypoint.py tests/test_main_controller.py tests/test_research_contract.py
python -m coop_navigation_sds --smoke
```

The complete `python -m pytest` suite includes prepared-provider/model checks.
Run `python scripts/prepare_test_environment.py --check` to inspect readiness;
see [setup](RESEARCH_GUIDE.md#10-setup) before choosing preparation commands that
download models. Missing-model failures are not successful validation.

Regenerate API and metric references after structural changes:

```bash
python scripts/generate_research_docs.py
```

Learned metrics require local estimators; intrusive audio metrics require aligned
references, and POLQA requires a licensed provider. Proxy scores are not human
judgments. Full-model capacity and experimental findings require completed runs
on suitable hardware, not only a passing smoke check.
