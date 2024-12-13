# JWT auth with FastAPI

[![build](https://github.com/nightblure/jwt_auth/actions/workflows/checks.yaml/badge.svg?branch=main)](https://github.com/nightblure/jwt_auth/actions/workflows/checks.yaml)
[![codecov](https://codecov.io/gh/nightblure/jwt_auth/branch/main/graph/badge.svg)](https://codecov.io/gh/{{REPOSITORY}})

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
