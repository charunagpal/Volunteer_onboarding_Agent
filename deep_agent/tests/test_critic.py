"""
Lesson 9 — Critic tests.

Run from deep_agent/:
    python -m pytest tests/test_critic.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.critic import Critic, MAX_RETRIES
from models.execution import ExecutionResult


def _make_results(
    *,
    register_ok: bool = True,
    register_retryable: bool = True,
    email_ok: bool = True,
) -> list[ExecutionResult]:
    """Helper — build a minimal but realistic result list."""
    return [
        ExecutionResult(task="Check Existing Volunteer", success=True,  message="Not found."),
        ExecutionResult(task="Collect Details",          success=True,  message="All collected."),
        ExecutionResult(task="Validate Information",     success=True,  message="Valid."),
        ExecutionResult(task="Confirm Registration",     success=True,  message="Confirmed."),
        ExecutionResult(
            task="Register Volunteer",
            success=register_ok,
            message="Registered." if register_ok else "Disk full.",
            retryable=register_retryable,
        ),
        ExecutionResult(
            task="Send Welcome Email",
            success=email_ok,
            message="Sent." if email_ok else "SMTP timeout.",
        ),
    ]


class TestCriticPassScenarios:

    def test_all_success(self):
        critic = Critic()
        report = critic.evaluate(_make_results())
        assert report.passed is True
        assert report.failed_tasks == []
        assert report.hard_failures == []
        assert "✅" in report.summary

    def test_email_failure_is_non_critical(self):
        """A failed Send Welcome Email must NOT cause passed=False."""
        critic = Critic()
        report = critic.evaluate(_make_results(email_ok=False))
        assert report.passed is True, "Email failure should be non-critical"

    def test_email_failure_logged(self, capsys):
        critic = Critic()
        critic.evaluate(_make_results(email_ok=False))
        captured = capsys.readouterr()
        assert "Non-critical failure" in captured.out


class TestCriticFailScenarios:

    def test_retryable_failure_detected(self):
        critic = Critic()
        report = critic.evaluate(_make_results(register_ok=False, register_retryable=True))
        assert report.passed is False
        assert "Register Volunteer" in report.failed_tasks
        assert report.hard_failures == []

    def test_hard_failure_detected(self):
        critic = Critic()
        report = critic.evaluate(_make_results(register_ok=False, register_retryable=False))
        assert report.passed is False
        assert report.hard_failures != []
        assert report.failed_tasks == []

    def test_summary_contains_failure_info(self):
        critic = Critic()
        report = critic.evaluate(_make_results(register_ok=False, register_retryable=True))
        assert "Register Volunteer" in report.summary
        assert "❌" in report.summary


class TestMaxRetries:
    def test_max_retries_constant(self):
        assert MAX_RETRIES == 2
