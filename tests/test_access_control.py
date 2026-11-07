"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""
from app.access_control import can_access_screening_report

def test_cross_account_access_denied(property_managers, properties, tenants, screening_reports):
    pm_001 = property_managers[0]
    rep_002 = screening_reports[1]

    # pm-001 should NOT have access to rep-002 (which belongs to la-002)
    assert not can_access_screening_report(
        actor=pm_001,
        report=rep_002,
        properties=properties,
        tenants=tenants,
    )


def test_same_account_access_allowed(property_managers, properties, tenants, screening_reports):
    pm_001 = property_managers[1]
    rep_001 = screening_reports[1]

    # pm-001 should have access to rep-001 (which belongs to la-001)
    assert can_access_screening_report(
        actor=pm_001,
        report=rep_001,
        properties=properties,
        tenants=tenants,
    )