# Cisco Meraki Network Automation Toolkit

A read-only Python portfolio project demonstrating Cisco Meraki Dashboard API integration, network inventory reporting, and WAN uplink status analysis. Built for network operations and infrastructure automation learning.

> **Portfolio demo:** Sample data is fictional. This is not a production deployment and does not imply access to any employer network.

## Features

- Offline demo mode with fictional MX/MS device inventory and uplink status
- Optional live mode using a **read-only** Meraki Dashboard API key
- REST API GET requests over HTTPS
- Inventory-to-uplink correlation by device serial number
- CSV reporting for network operations review
- Unit tests and GitHub Actions CI
- Python standard library only; no dependencies to install

## Architecture

```text
Meraki Dashboard API (live) OR sample JSON (demo)
                    |
                    v
            Inventory + uplink status
                    |
                    v
              Serial-based join
                    |
                    v
               CSV report
```

## Quick start (Windows / Linux / macOS)

Requires Python 3.10+.

```bash
python -m src.meraki_toolkit --mode demo
python -m unittest discover -s tests -v
```

Output: `output/meraki_uplink_report.csv` (ignored by Git).

## Optional live mode

**Only use networks you own or have permission to access.** Use a least-privilege read-only API key. Never commit a key, token, or real network inventory to GitHub.

PowerShell:

```powershell
$env:MERAKI_API_KEY = "YOUR_READ_ONLY_API_KEY"
python -m src.meraki_toolkit --mode live --organization-id YOUR_ORG_ID
Remove-Item Env:MERAKI_API_KEY
```

The toolkit calls `GET /organizations/{organizationId}/devices` and `GET /organizations/{organizationId}/uplinks/statuses`. API permissions and organization capabilities determine the results. The current implementation does not paginate large inventory responses or retry rate limits; use demo mode until those improvements are added.

## Repository layout

```text
src/meraki_toolkit.py       CLI, GET client, reporting
examples/devices.json      Fictional inventory
examples/uplinks.json      Fictional uplink data
tests/test_toolkit.py      Unit tests
.github/workflows/ci.yml  CI test and demo execution
```

## Skills demonstrated

Python, REST API fundamentals, Cisco Meraki Dashboard, LAN/WAN operations, inventory management, CSV reporting, test automation, and secure credential handling.

## Roadmap

- API pagination and rate-limit handling
- Inventory summary by model and network
- Change detection and WAN failover event reporting
- Structured logging and richer error handling
- Optional visual dashboard

## Limitations

The example is a demonstration, not an operational monitoring platform. Live API behavior must be verified against an authorized Meraki organization. No device configurations are modified.
