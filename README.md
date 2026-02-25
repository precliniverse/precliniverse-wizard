# Precliniverse Wizard

**Precliniverse Wizard** is the dedicated infrastructure manager and deployment orchestrator for the Precliniverse ecosystem. It provides a guided, secure, and modular interface to install, configure, and maintain your research facility OS.

## 🌟 Key Features

### 🏗️ Infrastructure Orchestration
Deploy the entire Precliniverse stack with a single command.
- **Modular Deployment**: Choose only the bricks you need (Quote, Set, Train).
- **Update Manager**: Simplified GUI to track version updates and apply them without breaking your facility.
- **Core Provisioning**: Automatically sets up the mandatory Core (Log + Authentik) and its persistence layers.

### 🧩 Service Broker
Smart integration of ecosystem components.
- **OIDC Auto-Config**: Hands-off configuration of Authentik and client applications (OIDC/SSO).
- **External Integration**: Support for external PostgreSQL instances and third-party OIDC providers for enterprise environments.

### 🛠️ Maintenance & Health
Keep your facility running smoothly.
- **Docker Centric**: Native management of container lifecycles and migrations.
- **Health-check**: Real-time validation of connectivity between modules.

## 🛡️ Security & Compliance
Built with the same rigor as the research briques.
- **Security First**: Native support for strict Content Security Policy (CSP).
- **Secret Management**: Secure injection of environment variables and automated secret generation.
- **Isolation**: The Wizard is designed to be ephemeral or isolated from the main business logic to reduce attack surface.

---

## 🛠️ Quick Start

The Wizard is the recommended entry point for any new Precliniverse installation.

### 1. Download the Bootstrap Script
```bash
curl -sSL https://raw.githubusercontent.com/precliniverse/precliniverse-wizard/main/installer.sh -o installer.sh
chmod +x installer.sh
```

### 2. Launch the Wizard
```bash
./installer.sh
```

### 3. Complete Setup in Browser
Follow the URL provided (usually `http://localhost:8000`) to select your modules and configure your facility.

---

## 📜 License
This project is licensed under the **GNU Affero General Public License v3.0 (AGPLv3)**.
*   **Free for Open Source**: Modify and use freely for academic/community projects.
*   **Commercial**: Contact us for proprietary licensing if you cannot share your modifications.
