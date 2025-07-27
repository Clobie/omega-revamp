# omega-revamp

AI driven discord bot.

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
chmod +x setup-dev.sh
./setup-dev.sh
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


## 🧩 Creating Cogs

Cogs are modular components of the bot and should be placed in the `./cogs/` directory.

If a cog requires persistent or static data, place it in a subdirectory of `./cogs/cogdata/` using the same name as the cog.

### 📄 Example Cog: `cogs/template.py`

```python
# cogs/template.py

import discord
from discord.ext import commands, tasks
import os

class TemplateSimple(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Initialize anything needed here

async def setup(bot: commands.Bot):
    cog = TemplateSimple(bot)
    await bot.add_cog(cog)
```

### 📁 Directory Structure

```
root/
├── cogs/
│   ├── template.py
│   └── ...
└── cogs/cogdata/
    └── template/
        └── any_data_you_need.json
```

> 🛠️ New cogs will auto-register and enable.  If you want it disabled by default, edit `./config/cogs.yaml`

---

## 📝 Notes

- Ensure Docker and Docker Compose are installed and running.
- All general configuration is handled through the `.env` file.
- All cog configuration is handled through the `cogs.yaml` file.
- All personalities are handles through the `personalities.yaml` file.
- The Discord bot’s coverage report will be available at:  
  `http://localhost:8000/htmlcov/index.html`  

---

## 💬 Commit Style

Follow [Conventional Commits](https://www.conventionalcommits.org/) for clear and consistent messages:

| Tag        | Purpose                                                                  |
| ---------- | ------------------------------------------------------------------------ |
| `feat`     | A new feature                                                            |
| `fix`      | A bug fix                                                                |
| `docs`     | Documentation changes (e.g., README, comments)                           |
| `style`    | Code style changes (formatting, white-space, missing semicolons, etc.)   |
| `refactor` | Code change that neither fixes a bug nor adds a feature                  |
| `perf`     | A change that improves performance                                       |
| `test`     | Adding or updating tests                                                 |
| `build`    | Changes that affect the build system or dependencies (e.g., npm, Docker) |
| `ci`       | Changes to CI configuration files and scripts (GitHub Actions, Travis)   |
| `chore`    | Routine maintenance (e.g., version bumps, package.json updates)          |
| `revert`   | Reverts a previous commit                                                |

**Example:**

```bash
feat(reactor): Created reactor cog
```

---

## 🧑‍💻 Coding Style

> This section reflects current project conventions. Contributors should match the existing style for consistency.

- Tabs instead of spaces for indentation.
- Class names use `PascalCase`.
- Function and variable names use `snake_case`.
- Imports are grouped: standard library, third-party, local modules.
- Avoid unnecessary comments – code should be self-documenting when possible.
- Use docstrings for public classes and functions.
