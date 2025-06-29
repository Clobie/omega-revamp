# omega-revamp

---

## Setup

1. Create a `.env` file in the root directory (`.`) with the following contents:

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

Replace `XXXX` with your actual Discord bot token.

---

## Running the services

Start all services and open an interactive shell in the bot container by running the appropriate command for your shell environment **from the project root**:

| Environment                 | Command                                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------------------|
| **PowerShell**              | `docker-compose -f docker-compose-dev.yaml up -d ; docker exec -it bot bash`                 |
| **Command Prompt (cmd.exe)**| `docker-compose -f docker-compose-dev.yaml up -d && docker exec -it bot bash`                |
| **Linux / macOS (bash/zsh)**| `docker-compose -f docker-compose-dev.yaml up -d && docker exec -it bot bash`                |

---

## Shutting down

To stop and remove all running containers, networks, and volumes created by the compose file, run:

```bash
docker-compose -f docker-compose-dev.yaml down
```

---

## Notes

- Ensure Docker and Docker Compose are installed and running on your machine.
- The `.env` file provides environment variables to configure the bot, database, and pgAdmin services.
- The bot container will be accessible on the port specified by `COVERAGE_PORT` in your `.env` file.

---
