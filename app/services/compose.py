import yaml
import secrets
import os

def generate_precliniverse_compose(config):
    """
    Modernized Compose Generator for Precliniverse Wizard V2.
    config: dict {facility_name, modules, db_external, db_config, sso_external, sso_config}
    """
    db_pass = config.get("db_pass", secrets.token_urlsafe(16))
    sso_pass = config.get("sso_pass", secrets.token_urlsafe(16))
    secret_key = secrets.token_urlsafe(32)
    
    services = {}
    networks = {"preclini-net": {"driver": "bridge"}}
    volumes = {}

    # 1. CORE: Database (if not external)
    if not config.get("db_external", False):
        services["db"] = {
            "image": "postgres:16-alpine",
            "restart": "always",
            "environment": {
                "POSTGRES_USER": "precliniverse",
                "POSTGRES_PASSWORD": db_pass,
                "POSTGRES_DB": "precliniverse"
            },
            "volumes": ["db_data:/var/lib/postgresql/data"],
            "networks": ["preclini-net"]
        }
        volumes["db_data"] = {}
        db_host = "db"
    else:
        db_host = config["db_config"].get("host")
        db_pass = config["db_config"].get("password")

    # 2. CORE: SSO (Authentik)
    services["redis"] = {
        "image": "redis:7-alpine",
        "restart": "always",
        "command": f"--requirepass {sso_pass}",
        "networks": ["preclini-net"]
    }
    
    services["authentik-server"] = {
        "image": "ghcr.io/goauthentik/server:2024.12.3",
        "restart": "always",
        "command": "server",
        "environment": {
            "AUTHENTIK_REDIS__HOST": "redis",
            "AUTHENTIK_REDIS__PASSWORD": sso_pass,
            "AUTHENTIK_POSTGRESQL__HOST": db_host,
            "AUTHENTIK_POSTGRESQL__USER": "precliniverse",
            "AUTHENTIK_POSTGRESQL__NAME": "precliniverse",
            "AUTHENTIK_POSTGRESQL__PASSWORD": db_pass,
            "AUTHENTIK_SECRET_KEY": secret_key
        },
        "volumes": ["./media:/media"],
        "networks": ["preclini-net"],
        "ports": ["9000:9000"]
    }

    # 3. CORE: Preclinilog (The Notary) - Mandatory
    services["preclinilog"] = {
        "image": "ghcr.io/precliniverse/preclinilog:latest",
        "restart": "always",
        "environment": {
            "DATABASE_URL": f"postgresql://precliniverse:{db_pass}@{db_host}:5432/precliniverse",
            "SECRET_KEY": secrets.token_urlsafe(32),
            "OIDC_ISSUER": "http://authentik-server:9000/application/o/preclinilog/"
        },
        "depends_on": ["db", "authentik-server"],
        "networks": ["preclini-net"],
        "ports": ["8001:8000"]
    }

    # 4. BRICKS: PrecliniQuote
    if "precliniquote" in config.get("modules", []):
        services["precliniquote"] = {
            "image": "ghcr.io/precliniverse/precliniquote:latest",
            "restart": "always",
            "environment": {
                "DATABASE_URL": f"postgresql://precliniverse:{db_pass}@{db_host}:5432/precliniverse",
                "SECRET_KEY": secrets.token_urlsafe(32),
                "OIDC_ISSUER": "http://authentik-server:9000/application/o/precliniquote/",
                "PRECLINILOG_URL": "http://preclinilog:8000"
            },
            "depends_on": ["preclinilog"],
            "networks": ["preclini-net"],
            "ports": ["5000:5000"]
        }

    compose = {
        "version": "3.8",
        "services": services,
        "networks": networks,
        "volumes": volumes
    }
    return yaml.dump(compose, sort_keys=False)
