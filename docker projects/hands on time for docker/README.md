
# What to do?

- docker compose up -d --build 
- run this to make it working and go to localhost:3000 
- and remove by 
- docker compose down --rmi all --volumes


# Detailed Written
# Dockerizing Node.js + PostgreSQL
---

## 1. What we wanted

1. Have a PostgreSQL database running in Docker.
2. Write a tiny Node.js server that talks to that database.
3. Package the app with a small, production-ready image.
4. Start / stop everything with one simple command.

---
## 2. What we built

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage build (builder ➜ slim runtime) to keep the final image small. |
| `docker-compose.yml` | Describes two services: `db` (Postgres 15) and `app` (our Node service). |
| `app.js` | Bare-bones HTTP server that runs `SELECT NOW()` to prove the DB works. |
| `.dockerignore` | Tells Docker what NOT to copy into the image. |

---
## 3. Zero-to-running in three commands

```bash
# 1) Build images & launch containers
$ docker compose up --build

# 2) Hit the endpoint ➜ http://localhost:3000
#    You should see JSON with the current PostgreSQL time.

# 3) When you’re done, clean up
$ docker compose down -v --rmi all
```

*(Skip `-v --rmi all` if you want to keep the database files and images.)*

---
## 4. Database login info

- Host: **localhost**  
- Port: **5432**  
- DB name: **mydatabase**  
- User: **myuser**  
- Password: **mysecretpassword**

```bash
psql -h localhost -p 5432 -U myuser -d mydatabase
```

---
## 5. What in  Dockerfile?

1. **Stage 1 – builder** installs *all* dependencies, runs any tests, etc.
2. **Stage 2 – production** copies only the code and *runtime* deps, so the final image stays lean.

Result: faster pulls, smaller attack surface. 





