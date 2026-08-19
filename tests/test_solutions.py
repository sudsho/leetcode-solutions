"""Pytest wrapper over the offline smoke registry.

Parametrizes the same known-answer cases used by scripts/smoke.py so that
`pytest` exercises every sampled solution as an individual test.
"""

import os
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import smoke  # noqa: E402


@pytest.mark.parametrize(
    "problem_dir,case_fn",
    smoke.CASES,
    ids=[c[0] for c in smoke.CASES],
)
def test_solution(problem_dir, case_fn):
    ok, detail = smoke.run_case(problem_dir, case_fn)
    assert ok, "{}: {}".format(problem_dir, detail)
