# Wiki Schema — iOS Major Version Restore

## Structure

This wiki documents the diagnostic and repair process for an iPhone stuck with error 4030 during an iOS restore spanning many major versions.

### Conventions
- Page names use kebab-case (e.g., `error-4030.md`)
- Internal links use `[[page-name]]` Obsidian-style wikilinks
- Each page has YAML frontmatter with `tags`, `date`, and `type`
- Types: `entity`, `concept`, `attempt`, `bug`, `overview`, `log`

### Directory layout
```
wiki/
  index.md        — catalog of all pages
  log.md          — chronological event log
  schema.md       — this file
  overview.md     — project summary and outcome
  error-4030.md   — the error being solved
  device.md       — device details
  dfu-vs-recovery.md — key concept that unlocked the solution
  root-cause.md   — root cause analysis
  attempt-*.md    — individual restore attempts (1-5)
  bug-*.md        — bugs encountered and fixed
  tools.md        — tools and versions used
  commands.md     — key commands reference
  lessons.md      — lessons learned
```

### Workflows
- **Ingest**: When new information is learned, update relevant pages and log
- **Query**: Read index first, drill into pages
- **Lint**: Check for stale info, missing cross-references
