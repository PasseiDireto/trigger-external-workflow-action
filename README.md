# Trigger External Workflow Action

GitHub Action that triggers a Workflow from another repository using "repository_dispatch" event

## Usage

```yaml

on: [push, workflow_dispatch]
jobs:
  trigger:
    runs-on: ubuntu-latest
    name: "📦 Trigger Project Test"
    steps:
    - uses: passeidireto/trigger-external-workflow-action@main
      env:
        PAYLOAD_AUTHOR: ${{ github.author }}
      with:
        repository: my-org/my-repo
        event: doc_update
        github_pat: ${{ secrets.pat_with_access }}
```