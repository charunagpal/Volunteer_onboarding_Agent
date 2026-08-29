from models.execution import ExecutionResult, CriticReport


# Tasks that are allowed to fail without blocking registration.
# e.g. WhatsApp/email is nice-to-have — a failure should not roll back the record.
_NON_CRITICAL_TASKS = {"Send Welcome Email"}

# Maximum number of automatic retries for a retryable failure.
MAX_RETRIES = 2


class Critic:
    """
    Evaluates the list of ExecutionResults produced by the Executor.

    Responsibilities:
      - Classify each result as critical vs non-critical.
      - Distinguish retryable (transient) failures from hard (data) failures.
      - Produce a CriticReport that the Supervisor acts on.

    The Critic never executes actions itself — it only analyses outcomes.
    """

    def evaluate(self, results: list[ExecutionResult]) -> CriticReport:
        failed_tasks: list[str] = []
        hard_failures: list[str] = []

        for result in results:
            if result.success:
                continue

            if result.task in _NON_CRITICAL_TASKS:
                # Log but do not treat as a blocking failure.
                print(f"[Critic] ⚠️  Non-critical failure — {result.task}: {result.message}")
                continue

            if not result.retryable:
                hard_failures.append(f"{result.task}: {result.message}")
            else:
                failed_tasks.append(result.task)

        passed = not failed_tasks and not hard_failures

        summary = self._build_summary(passed, failed_tasks, hard_failures)
        return CriticReport(
            passed=passed,
            failed_tasks=failed_tasks,
            hard_failures=hard_failures,
            summary=summary,
        )

    # ── Private helpers ──────────────────────────────────────────────────────

    def _build_summary(
        self,
        passed: bool,
        failed_tasks: list[str],
        hard_failures: list[str],
    ) -> str:
        if passed:
            return "✅ All critical tasks completed successfully."

        lines = ["❌ Execution did not complete cleanly."]

        if hard_failures:
            lines.append("\nThe following failures cannot be retried:")
            for msg in hard_failures:
                lines.append(f"  • {msg}")

        if failed_tasks:
            lines.append("\nThe following tasks failed but may succeed on retry:")
            for task in failed_tasks:
                lines.append(f"  • {task}")

        return "\n".join(lines)
