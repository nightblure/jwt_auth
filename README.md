# JWT auth with FastAPI

[![build](https://github.com/nightblure/jwt_auth/actions/workflows/ci.yaml/badge.svg)](https://github.com/nightblure/jwt_auth/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/nightblure/jwt_auth/branch/main/graph/badge.svg)](https://codecov.io/gh/{{REPOSITORY}})
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MyPy Strict](https://img.shields.io/badge/mypy-strict-blue)](https://mypy.readthedocs.io/en/stable/getting_started.html#strict-mode-and-configuration)
---

### Create migration
```
alembic revision --autogenerate -m 'Create user table'
```

### Run migration
```
alembic upgrade head
```

### Run tests
```bash
make test
```

### Static analyze
```bash
make lint
```
```bash
make mypy
```
