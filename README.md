# Trigger External Workflow Action

GitHub Action that triggers a Workflow from another repository using `[repository_dispatch](https://docs.github.com/pt/free-pro-team@latest/actions/reference/events-that-trigger-workflows#repository_dispatch)` event.

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
        PAYLOAD_REVISION: "3"
      with:
        repository: my-org/my-repo
        event: doc_update
        github_pat: ${{ secrets.pat_with_access }}
```

Be sure your `github_pat` has `workflow` scope on the target repository.

Any env var you pass using the preffix `PAYLOAD_` will be sent to the repository as the `client_payload` object. For instance, if you have previous example triggered, you could have the following workflow on `my-org/my-repo`:

```yaml
name: Repository Dispatch
on:
  repository_dispatch:
    types: [doc_update]
jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - run: echo '${{ github.event.client_payload.PAYLOAD_AUTHOR }} sent this revision: ${{ github.event.client_payload.PAYLOAD_REVISION }}'
```

Make sure all your PAYLOAD variables are strings. GHA does not allow different types, such as booleans and integers. You can also use this action with [matrix strategy](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions/managing-complex-workflows#using-a-build-matrix), such as:

```yaml
on: [push, workflow_dispatch]
name: 'Trigger new update'
jobs:
  trigger:
    runs-on: ubuntu-latest
    name: "Notify about update"
    strategy:
      matrix:
        repo: ['repo01', 'repo02']
    steps:
    - uses: passeidireto/trigger-external-workflow-action@main
      env:
        PAYLOAD_REBUILD: "false"
        PAYLOAD_BRANCH: ${{github.ref}}
      with:
        repository: PasseiDireto/${{ matrix.repo }}
        event: update
        github_pat: ${{ secrets.my_super_pat }}
```


## Contributing

PRs welcome! This action is a Docker container, so it is very easy run it locally. Be sure you have all the required inputs represented as envrionment variables. For instance you will need a `INPUT_GITHUB_PAT` to represent the input `github_pat` the action will actually pass. Note the `INPUT_` preffix and the camel case representation.

### Development guide

Clone the repository using Git:
```sh
git clone git@github.com:PasseiDireto/trigger-external-workflow-action.git
```

You can build the image as:

```sh
docker build -t trigger-external-workflow-action .
```

Have an [env file](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) ready with all the variables you need, such as:

```sh
INPUT_REPOSITORY=my-org/my-repo
INPUT_EVENT=new_event
INPUT_GITHUB_PAT=my-gh-pat
PAYLOAD_AUTHOR=the-author
PAYLOAD_VAR2=123

```

You can name it `.env` and then then run it the freshly built image:

```sh
docker run --rm --env-file=.env trigger-external-workflow-action
```

### Before you commit

Be sure all the tests and all the checks are passing:
```sh
pip install -r requirements/all.txt
make # run all checks
make tests # run all tests

```


# Similar actions

[This project](https://github.com/peter-evans/repository-dispatch) is somehow close to this one, with a main difference on the payload strategy.
