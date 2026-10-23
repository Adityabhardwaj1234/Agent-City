# Fresh-user documentation test

- Date: 2026-10-23
- Tester: fresh general subagent with no prior project context
- Mode: offline
- Provider: none
- Scope: README quick start, AI_CONTEXT, dev-setup, mcp-and-skills

## Method

The tester was told to follow the README M0 quick start without editing files,
without network access, without opening the real SkillBridge catalog, and
without starting long-running servers. It ran the safe commands, compared the
documented expectations with real output, and reported broken instructions and
contradictions. A second pass re-tested the fixes.

## Round 1 findings (all reproduced)

1. SkillBridge snippets in dev-setup and mcp-and-skills omitted `PYTHONPATH` and
   failed with `No module named skillbridge` when copied as printed.
2. README led with URL placeholders that only worked because the clones already
   existed, creating a false-positive setup.
3. README's `mcp-serve` example used the corrupt real catalog and did not say
   the process blocks on stdin.
4. `generate-context.py` was described as a check; it rewrites generated docs
   unconditionally, and the committed state-of-build had drifted from it.
5. `.env` was presented as active configuration although no M0 code reads it.
6. `doctor --json` had no pass/fail criteria beyond "exit 0".
7. Execution-policy failure had no documented recovery.
8. The corrupt-catalog quarantine wording described a warning as if it had
   already happened.
9. Path conventions were inconsistent across README, AI_CONTEXT, and runbooks.

## Fixes applied

- README now leads with `-VerifyOnly`, labels the URL/local-source path as
  fresh-machine only, explains that repository URLs are not recorded, and notes
  the one-command `-ExecutionPolicy Bypass` fallback.
- Every executable SkillBridge block sets `PYTHONPATH` and runs from the repo
  root.
- README and the MCP runbook start `mcp-serve` with a throwaway `--home` and
  state that it blocks while waiting for stdin.
- Generator vs. checker roles are separated in README, AI_CONTEXT, dev-setup,
  docs/README, and documentation-standards. Generated docs were regenerated and
  now match the generator byte for byte.
- `.env` is marked as an M1 contract that no M0 code reads; the
  `SKILLBRIDGE_HOME` scope is stated.
- Doctor pass criteria, execution-policy recovery, and quarantine wording were
  corrected. Path references were normalized where they were misleading.

## Round 2 result

The tester re-ran the affected commands and reported:

- `bootstrap-skills.ps1 -VerifyOnly`: passed, both pins correct.
- dev-setup §4 and §5, and mcp-and-skills §3, copied exactly: passed.
- `check-docs.py`: passed, 60 Markdown files.
- `mcp-serve --help` argument form: accepted; server not started.
- Generated docs: identical to a fresh generator run into a temp directory.
- Real catalog unchanged: 9,609,216 bytes, last write 2026-10-19, no quarantine
  file. No network or real-home access.

Verdict: **go**, conditional on correcting the README provider-key sentence and
the fresh-machine source-discovery wording. Both were corrected immediately
after the report. The remaining `git status` concern is repository state, not
documentation: the M0 tree had no first commit when the test ran.

## Residual notes

- The two tool sources cannot be hardcoded in the repository. A fresh machine
  needs the user to supply upstream URLs or local checkouts; this is stated in
  README and dev-setup.
- Cosmetic bare filenames remain in a few prose sentences; they are not links and
  do not block setup.
- A true end-to-end test of `mcp-serve` (initialize handshake, tool discovery)
  is deferred to the M2 contract tests; M0 proves the package starts and the
  read-only CLI path works.
