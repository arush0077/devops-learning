# Node.js + PostgreSQL with Docker Compose

This project shows how to spin up a **PostgreSQL** database and a small **Node.js** service using **Docker Compose** and a **multi-stage Docker build**.

---
## 🗂️ Folder structure
```
.
├── .dockerignore          # files ignored by docker build context
├── Dockerfile             # multi-stage build (builder ➜ production)
├── docker-compose.yml     # brings up the app + database together
├── package.json           # Node.js metadata & deps
├── app.js                 # tiny HTTP server that queries Postgres
└── README.md              # (this file)

```

---
## 🚀 Quick start
1.  Make sure **Docker Desktop** (or Docker Engine) is running.
2.  From this directory run:

```bash
# build images and start containers
docker compose up --build
```

*   `db` (PostgreSQL 15) becomes healthy first.
*   `app` (Node.js) starts afterwards and listens on **http://localhost:3000**.

Open <http://localhost:3000> – you should see a JSON payload containing the current database time.

To stop everything:
```bash
docker compose down   # add -v to also delete database volume
```

---
## 🐘 PostgreSQL service (`db`)
| Setting | Value |
|---------|-------|
| Image   | `postgres:15` |
| DB name | `mydatabase`  |
| User    | `myuser`      |
| Pass    | `mysecretpassword` |
| Port    | `5432` (exposed to host) |
| Volume  | `postgres_data` (persists data between runs) |

A health-check (`pg_isready`) makes sure Postgres is ready before the Node.js container tries to connect.

---
## 🟢 Node.js service (`app`)
* Built via the **`production` stage** of the multi-stage Dockerfile.
* Connects to Postgres using environment variables provided in `docker-compose.yml`.
* Exposes port **3000**.
* Simple endpoint returns `SELECT NOW()` result so you know the DB connection works.

### Environment variables
```
DB_HOST=db
DB_USER=myuser
DB_PASSWORD=mysecretpassword
DB_NAME=mydatabase
DB_PORT=5432
```

---
## 🛠️ Multi-stage Dockerfile explained
```Dockerfile
# Stage 1 – builder
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install            # install dev + prod deps
COPY . .

# Stage 2 – production runtime
FROM node:18-slim AS production
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production   # keep image small
COPY --from=builder /app/app.js .   # copy compiled / tested artifacts
EXPOSE 3000
HEALTHCHECK CMD curl -f http://localhost:3000/ || exit 1
CMD ["node", "app.js"]
```
* Using **two stages** keeps the final image tiny because dev dependencies are left behind in the builder layer.
* `docker compose` is told to build **only** the `production` stage (`target: production`).

---
## 🔍 Useful commands
| Purpose | Command |
|---------|---------|
| Start services in background | `docker compose up -d` |
| View combined logs           | `docker compose logs -f` |
| Stop services                | `docker compose down` |
| Remove containers **and** volume | `docker compose down -v` |
| Connect to Postgres CLI      | `docker exec -it <db_container_id> psql -U myuser -d mydatabase` |

---
## 📝 What we did (summary)
1. **Created** a simple Node.js server that queries Postgres ( `app.js` ).
2. **Added** `package.json` listing only runtime dep `pg`.
3. **Wrote** a **multi-stage Dockerfile** for an efficient production image.
4. **Authored** `docker-compose.yml` that
   * pulls `postgres:15`, primes it with credentials and a volume,
   * builds the Node.js service via the `production` stage,
   * wires the two using service names and waits for DB readiness.
5. **Documented** everything in this `README.md` so you can reproduce the steps quickly.

Happy Dockering! 🎉
