import urllib.request
import json

def test_profile(payload):
    req = urllib.request.Request('http://localhost:8000/api/roadmap', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return str(e)

print('--- PROFILE 1: Pharma, Pune, 50 Cr, Large, New Land ---')
p1 = {'industry_type': 'Pharmaceutical Manufacturing', 'district': 'Pune', 'investment_scale_crores': 50, 'unit_size': 'large', 'existing_land': False}
res1 = test_profile(p1)
if isinstance(res1, dict):
    print(f"Total Days: {res1.get('total_estimated_days')}")
    print(f"Total Clearances: {len(res1.get('clearances', []))}")
    fee1 = sum(c.get('estimated_fee_inr', 0) for c in res1.get('clearances', []))
    print(f"Total Fee INR: {fee1}")
else:
    print('Error:', res1)

print('\n--- PROFILE 2: Software Services, Mumbai, 800 Cr, Small, Existing Land ---')
p2 = {'industry_type': 'Software Services', 'district': 'Mumbai', 'investment_scale_crores': 800, 'unit_size': 'small', 'existing_land': True}
res2 = test_profile(p2)
if isinstance(res2, dict):
    print(f"Total Days: {res2.get('total_estimated_days')}")
    print(f"Total Clearances: {len(res2.get('clearances', []))}")
    fee2 = sum(c.get('estimated_fee_inr', 0) for c in res2.get('clearances', []))
    print(f"Total Fee INR: {fee2}")
else:
    print('Error:', res2)
