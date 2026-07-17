# GitHub MCP Workflow for PR/Issue Management

When the GitHub MCP server is available, use it instead of `gh` CLI or `curl` for creating branches, PRs, and issues. The MCP tools are more reliable and handle auth automatically.

## Creating a Branch

```
mcp_github_create_branch(branch="feat/my-feature", from_branch="main", owner="user", repo="repo")
```

Then fetch and checkout locally:
```bash
git fetch origin feat/my-feature && git checkout feat/my-feature
```

## Creating a PR

After pushing commits:
```bash
git push origin feat/my-feature
```

Use MCP to create the PR:
```
mcp_github_create_pull_request(
  owner="user",
  repo="repo",
  title="feat: description",
  head="feat/my-feature",
  base="main",
  body="## Changes\n- Item 1\n- Item 2\n\nCloses #4"
)
```

Then switch back to main:
```bash
git checkout main
```

## Creating Issues

Create issues for future work (not yet implementing):
```
mcp_github_create_issue(
  owner="user",
  repo="repo",
  title="feat: feature description",
  body="## Tasks\n- [ ] Task 1\n- [ ] Task 2\n\n## Related\nSpec: [[doc name]]",
  labels=["enhancement"]
)
```

## Adding Comments to Issues

```
mcp_github_add_issue_comment(
  owner="user",
  repo="repo",
  issue_number=5,
  body="## Note\nAdditional context or decision."
)
```

## Workflow Pattern

1. `mcp_github_create_branch` — create remote branch
2. `git fetch + git checkout` — switch to branch locally
3. Make changes, commit, push
4. `mcp_github_create_pull_request` — create PR
5. `git checkout main` — switch back
6. `mcp_github_create_issue` — create issues for future work

## Pitfalls

- MCP `create_branch` creates on remote only — must `git fetch` + `git checkout` locally
- MCP `create_pull_request` requires `owner` and `repo` params (not inferred from git remote)
- Always switch back to `main` after creating a PR — don't accidentally commit on the feature branch
