"""Render MATLAB JUnit test results as Markdown for the GitHub job summary."""
import os
import sys
import xml.etree.ElementTree as ET

results_path = sys.argv[1]
summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
out = open(summary_path, "a", encoding="utf-8") if summary_path else sys.stdout

if not os.path.exists(results_path):
    out.write("## MATLAB Test Results\n\n"
              ":warning: No test results found. The build failed before "
              "tests ran — see the job log.\n")
    sys.exit(0)

root = ET.parse(results_path).getroot()
suites = [root] if root.tag == "testsuite" else root.findall("testsuite")

rows = []
counts = {"passed": 0, "failed": 0, "skipped": 0}
total_time = 0.0
for suite in suites:
    for case in suite.findall("testcase"):
        name = f"{case.get('classname', '')}/{case.get('name', '')}"
        time = float(case.get("time") or 0)
        total_time += time
        if case.find("failure") is not None or case.find("error") is not None:
            status, icon = "failed", ":x:"
        elif case.find("skipped") is not None:
            status, icon = "skipped", ":warning:"
        else:
            status, icon = "passed", ":white_check_mark:"
        counts[status] += 1
        rows.append((icon, status, name, time))

total = sum(counts.values())
headline = ":x: Tests failed" if counts["failed"] else ":white_check_mark: All tests passed"

out.write("## MATLAB Test Results\n\n")
out.write(f"**{headline}** — {counts['passed']} passed, {counts['failed']} failed, "
          f"{counts['skipped']} skipped of {total} ({total_time:.2f} s)\n\n")

# List failures first so they are visible without scrolling.
rows.sort(key=lambda r: {"failed": 0, "skipped": 1, "passed": 2}[r[1]])
out.write("| Status | Test | Time (s) |\n|---|---|---|\n")
for icon, _, name, time in rows:
    out.write(f"| {icon} | `{name}` | {time:.3f} |\n")
