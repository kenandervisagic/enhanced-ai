# Enhanced AI

---

## Setup Instructions

1. **Ensure Docker is running:**
   * Make sure Docker Desktop (or Docker Engine) is installed and running on your machine.


2. **Setup ```.env``` file:**
   ```bash
   cp .env-example .env
   ```
   * Replace ```OPENAI_API_KEY``` with you acctual key


3. **Start the Docker containers:**
    ```bash
   docker compose up 
    ```

---
## PyCharm Setup

1. Set ```app``` as the Project Root:
   * Open PyCharm.
   * Right-click the ```app``` directory in the Project Explorer.
   * Select **Mark Directory as** → **Sources Root**. This will ensure that PyCharm can properly resolve imports and treat the app directory as the project root.