# JWT auth with FastAPI

[![build](https://github.com/nightblure/jwt_auth/actions/workflows/checks.yaml/badge.svg?branch=main)](https://github.com/nightblure/jwt_auth/actions/workflows/checks.yaml)
[![codecov](https://codecov.io/gh/nightblure/jwt_auth/branch/main/graph/badge.svg?token=7JFXGJJAF3)](https://codecov.io/gh/nightblure/jwt_auth)

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
```
pytest -rA --cov=src
```

### Links
* [Check JWT tokens](https://jwt.io/)