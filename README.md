# **do-function-tester** A small codebase to test DigitalOcean Function `blocking=false` functionality

> Code repository author: [Alexandre Harano](mailto:email@ayharano.dev)

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=532177d7d8ec&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

This project provides a small [DigitalOcean Function](https://docs.digitalocean.com/products/functions/)
using Python to validate `blocking=false` functionality.

# Project Configuration
This project uses [the twelve-factor app](https://12factor.net/) methodology.

Environment variables in this project can be stored using a `.env` (dot env) file.
For initial setup, a sample is provided as [`.env.sample`](.env.sample).

A description of each of the variables is provided as the following list.

- `FUNCTION_URL`: the DigitalOcean Function URL to be called
- `AUTHORIZATION_TOKEN`: a string value to be used as [the Functions REST API Authorization token](https://docs.digitalocean.com/products/functions/how-to/async-functions/#call-a-function-asynchronously-using-curl-and-the-rest-api)

# Project Installation
First, clone this repo:

```shell
$ git clone https://github.com/ayharano/do-function-tester.git
```

After cloning the repository, change the directory to the project root.
All instructions below, including configuring the virtual environment and running the project,
depend on being in the project root directory.

## Consistency of contributions using `pre-commit`

To maintain consistency between individual commits,
this repo is adopting the use of [`pre-commit`](https://pre-commit.com/).

The recommended way to install it for this repo is by installing via [`pipx`](https://pipx.pypa.io/stable/).
After installing `pipx`, issue the following commands:

```shell
$ pipx install pre-commit
$ pre-commit install --install-hooks --overwrite
```

`pre-commit` is configured to also run per push and pull requests in GitHub workflow.

## Python Version and Virtual Environment Setup
This project was tested by using CPython 3.10. In order to keep multiple versions of the Python interpreter, we recommend the use of pyenv.

- pyenv (Linux, macOS): [link](https://github.com/pyenv/pyenv)
- pyenv for Windows (Windows): [link](https://pyenv-win.github.io/pyenv-win/)

Once it is installed, we can use the same version as the one used during this project development, which was CPython 3.12.1.

Run the following:
```shell
$ pyenv install 3.10.3  # install CPython 3.10.3
$ pyenv local 3.10.3    # select CPython 3.10.3 as the local interpreter
```

As a directory name for the virtual env, for this tutorial we will use it as `virtualenvironment`.
If you prefer another name, just replace all the occurrences from here.

To install a virtual env, run the following:

```shell
$ python -m venv virtualenvironment
```

This way, a directory named `virtualenvironment` will be created at the project root to store the Python project dependencies.

## Using the local virtual env

Regarding the installation and the use of virtual envs, more details can be found at [the `venv` module documentation](https://docs.python.org/3/library/venv.html).

To use the virutal env, the instructions depend on the target operating system:

- venv for Linux or macOS

```shell
$ source virtualenvironment/bin/activate
```

- venv for Windows (PowerShell)

```powershell
virtualenvironment\Scripts\Activate.ps1
```

## Installing the project dependencies in the virtual env

Once the virtual env is activated, run:

```shell
python -m pip install --upgrade pip && python -m pip install --editable '.[local]' && python -m pip install --upgrade tzdata
```

This command is a chained call of 3 executions, being
1. upgrading the local `pip` to its most recent version
2. installing all the project dependencies, including the ones for local dev use, and installing the project as [an editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html), and
3. enforce the most recent version of `tzdata`, which is used by Python to manage timezone data without relying on the data from the target operating system (more details at [the `zoneinfo` module documentation](https://docs.python.org/3/library/zoneinfo.html))

# DigitalOcean Functions Usage

## DigitalOcean Functions Deployment

To deploy this function, a DigitalOcean account is required.

For this tutorial, we rely on `doctl` CLI ([installation instructions](https://docs.digitalocean.com/reference/doctl/how-to/install/)).

Following the [Functions Quickstart](https://docs.digitalocean.com/products/functions/getting-started/quickstart/),
we must create a namespace before deploying a Function.
Two parameters are required:
- `label`: an arbitrary label for the namespace
- `region`: one of the available DigitalOcean's datacenter - [list for Functions](https://docs.digitalocean.com/products/functions/details/availability/)

For this example, we used `functions-ns` as its label and `nyc` as its region:

```shell
$ doctl serverless namespaces create --label functions-ns --region nyc
```

If it is correctly configured, an output similar to the following should be displayed

```
Connected to functions namespace 'fn-01234567-89ab-cdef-0123-456789abcdef' on API host 'https://faas-nyc1-abcdef01.doserverless.co'
```

To deploy the function(s), run:

```shell
$ doctl serverless deploy .  # yes, it is a dot after deploy
```

If it is correctly runs, an output such as the following should be displayed

```
Deploying '/home/user/projects/do-function-tester'
  to namespace 'fn-01234567-89ab-cdef-0123-456789abcdef'
  on host 'https://faas-nyc1-abcdef01.doserverless.co'

Deployed functions ('doctl sls fn get <funcName> --url' for URL):
  - tester/blocking_false_handler
```

## DigitalOcean Functions Tester

### Environmental Variables
To test the Function, we need to populate the environmental variables:

#### `FUNCTION_URL`

As we will need the Function URL, we should run the suggested command:

```shell
$ doctl sls fn get tester/blocking_false_handler --url
```

The output is a URL similar to this

```
https://faas-nyc1-abcdef01.doserverless.co/api/v1/web/fn-01234567-89ab-cdef-0123-456789abcdef/tester/blocking_false_handler
```

We can set that value in the `.env` file as `FUNCTION_URL`:

```
FUNCTION_URL=https://faas-nyc1-abcdef01.doserverless.co/api/v1/web/fn-01234567-89ab-cdef-0123-456789abcdef/tester/blocking_false_handler
```

#### `AUTHORIZATION_TOKEN`

Follow the instructions described in [Call a Function Asynchronously using `curl` and the REST API](https://docs.digitalocean.com/products/functions/how-to/async-functions/#call-a-function-asynchronously-using-curl-and-the-rest-api) to retrieve the token.

Having its full value (everything after `Authorization:`), set it in the `.env` file as `AUTHORIZATION_TOKEN`:

```
AUTORIZATION_TOKEN=Basic VeryBase64EncodedValue=
```

### Issue Asynchronous Function Call

If the project was correctly installed as described in the [Project Installation section](#project-installation), we can just test the Function by running

```shell
$ python -m tester issue any value here after issue will be grouped as a list
```

Example output:

```python
{'after_request': '2024-02-16T18:46:24.745284+00:00',
 'before_request': '2024-02-16T18:46:24.319217+00:00',
 'body': {'activationId': 'abcdef0123456789abcdef0123456789'},
 'status_code': 202,
 'time_diff': 0.426067}
```


### Retrieve Activation Record

As described in [Retrieve Activation Records Using `curl` and the REST API](https://docs.digitalocean.com/products/functions/how-to/async-functions/#call-a-function-asynchronously-using-curl-and-the-rest-api), we can retrieve the actual values using the `activationId`.

If the project was correctly installed as described in the [Project Installation section](#project-installation), we can just test the Function by running

```shell
$ python -m tester retrieve abcdef0123456789abcdef0123456789
```

where `abcdef0123456789abcdef0123456789` would be the `activationId` value.

Example output:

```python
{'after_request': '2024-02-16T18:47:09.740636+00:00',
 'before_request': '2024-02-16T18:47:09.255087+00:00',
 'body': {'activationId': 'abcdef0123456789abcdef0123456789',
          'annotations': [{'key': 'path',
                           'value': 'fn-01234567-89ab-cdef-0123-456789abcdef/tester/blocking_false_handler'},
                          {'key': 'waitTime', 'value': 769},
                          {'key': 'uuid',
                           'value': 'fedcba98-7654-3210-0123-456789abcdef'},
                          {'key': 'entry', 'value': 'main'},
                          {'key': 'user_id', 'value': '12345678'},
                          {'key': 'gbs', 'value': 0.0125},
                          {'key': 'kind', 'value': 'python:3.9'},
                          {'key': 'timeout', 'value': False},
                          {'key': 'limits',
                           'value': {'logs': 5,
                                     'memory': 128,
                                     'timeout': 1000}},
                          {'key': 'initTime', 'value': 10}],
          'duration': 2,
          'end': 1708109185446,
          'logs': [],
          'name': 'blocking_false_handler',
          'namespace': 'fn-01234567-89ab-cdef-0123-456789abcdef',
          'publish': False,
          'response': {'result': {'body': {'list_args': ['any',
                                                         'value',
                                                         'here',
                                                         'after',
                                                         'issue',
                                                         'will',
                                                         'be',
                                                         'grouped',
                                                         'as',
                                                         'a',
                                                         'list'],
                                           'received_at': '2024-02-16T18:46:25.445336+00:00',
                                           'sent_at_arg': '2024-02-16T18:46:24.319205+00:00'},
                                  'statusCode': 202},
                       'size': 232,
                       'status': 'success',
                       'success': True},
          'start': 1708109185444,
          'subject': '01234567-89ab-cdef-0123-456789abcdef',
          'version': '0.0.1'},
 'status_code': 200,
 'time_diff': 0.485549}
```
