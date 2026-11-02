"""Read-only Meraki inventory and uplink reporting toolkit."""
import argparse
import csv
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = 'https://api.meraki.com/api/v1'


def request_json(path, api_key, base_url=BASE_URL):
    """Read JSON from the Meraki Dashboard API (GET only)."""
    url = base_url.rstrip('/') + '/' + path.lstrip('/')
    if not url.startswith('https://'):
        raise ValueError('HTTPS is required for API requests')
    req = urllib.request.Request(url, headers={
        'X-Cisco-Meraki-API-Key': api_key,
        'Accept': 'application/json',
        'User-Agent': 'meraki-network-automation-toolkit/1.0',
    }, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'Meraki API returned HTTP {exc.code}') from exc
    except urllib.error.URLError as exc:
        raise RuntimeError('Unable to connect to Meraki API') from exc


def build_report(devices, uplinks):
    """Join inventory and uplink statuses without modifying input data."""
    by_serial = {u.get('serial'): u for u in uplinks}
    rows = []
    for device in devices:
        serial = device.get('serial', '')
        item = by_serial.get(serial, {})
        for interface in item.get('uplinks', []) or []:
            rows.append({
                'name': device.get('name') or '',
                'serial': serial,
                'model': device.get('model') or '',
                'networkId': device.get('networkId') or '',
                'interface': interface.get('interface') or '',
                'status': interface.get('status') or 'unknown',
                'ip': interface.get('ip') or '',
            })
        if not item.get('uplinks'):
            rows.append({'name': device.get('name') or '', 'serial': serial,
                         'model': device.get('model') or '', 'networkId': device.get('networkId') or '',
                         'interface': '', 'status': 'not_applicable', 'ip': ''})
    return rows


FIELDS = ('name', 'serial', 'model', 'networkId', 'interface', 'status', 'ip')


def save_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description='Read-only Cisco Meraki inventory and WAN uplink report')
    parser.add_argument('--mode', choices=['demo', 'live'], default='demo')
    parser.add_argument('--organization-id', help='Required for live mode')
    parser.add_argument('--output', default='output/meraki_uplink_report.csv')
    args = parser.parse_args()
    if args.mode == 'demo':
        folder = Path(__file__).resolve().parent.parent / 'examples'
        devices = json.loads((folder / 'devices.json').read_text(encoding='utf-8'))
        uplinks = json.loads((folder / 'uplinks.json').read_text(encoding='utf-8'))
    else:
        api_key = os.environ.get('MERAKI_API_KEY')
        if not api_key or not args.organization_id:
            parser.error('Live mode requires MERAKI_API_KEY and --organization-id')
        org = urllib.parse.quote(args.organization_id, safe='')
        devices = request_json(f'organizations/{org}/devices', api_key)
        uplinks = request_json(f'organizations/{org}/uplinks/statuses', api_key)
    rows = build_report(devices, uplinks)
    save_csv(rows, args.output)
    print(f'Generated {len(rows)} rows in {args.output}')


if __name__ == '__main__':
    main()
