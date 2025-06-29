# omega-revamp

A development environment for the Omega Discord bot using Docker Compose.

---

## ⚙️ Setup

1. Create a `.env` file in the root of the project (`.`) with the following content:

    ```env
    DISCORD_BOT_TOKEN=XXXX
    DB_USER=test
    DB_PASS=test
    DB_HOST=127.0.0.1
    DB_NAME=test
    DB_PORT=5432
    PGADMIN_EMAIL=admin@example.com
    PGADMIN_PASS=admin
    PGADMIN_PORT=5050
    COVERAGE_PORT=8000
    ```

    > 🔒 Replace `XXXX` with your actual Discord bot token.  Edit others as needed.

---

## ▶️ Starting and connecting to the container

Start the development environment and open a shell inside the bot container. Run the following commands **from the project root**:

```bash
docker-compose -f docker-compose-dev.yaml up -d
docker exec -it bot bash
```

---

## ⏹️ Setting up services and running the bot

To run the setup, run the following commands **inside the container**:

```bash
chmod +x setup.sh
./setup.sh
```

To run the bot, run the following command **inside the container**:

```bash
python main.py
```

---

## ⏹️ Shutting Down

To stop and remove all services, containers, and networks created by Docker Compose:

```bash
docker-compose -f docker-compose-dev.yaml down
```

---

## 📝 Notes

- Ensure Docker and Docker Compose are installed and running.
- All configuration is handled through the `.env` file.
- The Discord bot’s coverage report will be available at:  
  `http://localhost:8000/htmlcov/index.html`  

---
