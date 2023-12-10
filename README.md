# JWT auth with FastAPI

![Build Status](https://github.com/nightblure/jwt_auth/actions/workflows/checks.yml/badge.svg?branch=main)
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
pytest --cov=src
```

### Links
* [Check JWT tokens](https://jwt.io/)