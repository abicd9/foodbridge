"""FOOD DATA CONNECTOR - this is where your food-data API plugs in.

1. Put these in .env:  FOOD_DATA_API_URL, FOOD_DATA_API_KEY (and FOOD_DATA_SOURCE_NAME)
2. Edit FIELD_MAP below so each FoodBridge field points at the matching key in your API's JSON.
3. Run (API server must be running):   python -m app.food_data [--publish]

Rows are imported through the normal admin import, so they validate, de-duplicate and wait as PENDING
until an administrator publishes them (or pass --publish to publish them straight away).
"""
import argparse
import os
import httpx

# FoodBridge field  ->  key in YOUR api's JSON row (edit the right-hand side)
# TODO(food data): right-hand side = the key names your food-data API actually returns.
FIELD_MAP = {
    'id': 'id', 'name': 'name', 'organisation': 'organisation', 'support_type': 'type',
    'address': 'address', 'postal': 'postal_code', 'latitude': 'lat', 'longitude': 'lng',
    'description': 'description', 'eligibility': 'eligibility', 'phone': 'phone', 'website': 'website',
}
TYPE_MAP = {'meal': 'Hot meals', 'grocery': 'Groceries', 'foodbank': 'Food bank', 'delivery': 'Delivery'}  # your values -> ours


# TODO(food data): set FOOD_DATA_API_URL and FOOD_DATA_API_KEY in backend/.env, then adjust FIELD_MAP / TYPE_MAP above.
# TODO(food data): change the auth header below if your provider does not use "Authorization: Bearer <key>".
# TODO(food data): add paging here if your API returns results in pages.
def fetch_rows():
    url = os.environ['FOOD_DATA_API_URL']
    key = os.getenv('FOOD_DATA_API_KEY', '')
    headers = {'Authorization': 'Bearer ' + key} if key else {}  # change if your API uses a different auth header
    response = httpx.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else data.get('results', data.get('data', []))


def convert(row, org_ids):
    g = lambda field: row.get(FIELD_MAP[field])
    kind = TYPE_MAP.get(str(g('support_type')).lower(), g('support_type'))
    return {'id': 'fd-' + str(g('id')), 'organisation_id': org_ids[g('organisation') or g('name')], 'name': g('name'),
            'support_type': kind, 'address': g('address'), 'postal': str(g('postal')), 'latitude': float(g('latitude')),
            'longitude': float(g('longitude')), 'description': g('description') or '', 'eligibility': g('eligibility') or 'Contact to confirm',
            'phone': g('phone') or None, 'website': g('website') or None, 'verified_at': __import__('datetime').datetime.now().astimezone().isoformat()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    base = os.getenv('FOODBRIDGE_API', 'http://127.0.0.1:8000')
    with httpx.Client(base_url=base, timeout=60) as api:
        login = api.post('/api/admin/login', json={'email': os.getenv('ADMIN_EMAIL', 'admin@foodbridge.sg'),
                                                   'password': os.getenv('ADMIN_PASSWORD', 'FoodBridge@Admin2026')})
        login.raise_for_status()
        api.headers['Authorization'] = 'Bearer ' + login.json()['token']
        rows, org_ids = fetch_rows(), {}
        for row in rows:
            name = row.get(FIELD_MAP['organisation']) or row.get(FIELD_MAP['name'])
            if name not in org_ids:
                created = api.post('/api/admin/organisations', json={'name': name, 'source': os.getenv('FOOD_DATA_SOURCE_NAME', 'Food data API')})
                created.raise_for_status()
                org_ids[name] = created.json()['id']
        records = [convert(r, org_ids) for r in rows]
        result = api.post('/api/admin/import', json={'source': os.getenv('FOOD_DATA_SOURCE_NAME', 'Food data API'),
                                                     'permission': os.getenv('FOOD_DATA_PERMISSION', 'Licensed API access'), 'records': records})
        result.raise_for_status()
        print(result.json())
        if args.publish:
            for record in records:
                published = api.post(f"/api/admin/services/{record['id']}/publish")
                print(record['id'], 'published' if published.is_success else published.text)


if __name__ == '__main__':
    main()
