"""
B2, part 1 — implement can_access_screening_report().

Read README.md's domain model first. A ScreeningReport belongs to a Tenant, a Tenant belongs to
a Property, and a Property belongs to a LandlordAccount. A PropertyManager is scoped to exactly
one LandlordAccount.

Work out from that hierarchy which boundary actually gates access to a ScreeningReport.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    actor: the PropertyManager requesting access
    report: the ScreeningReport they're trying to view
    properties: all known Property records
    tenants: all known Tenant records

    Return True if actor may view report, False otherwise. Fail closed — if anything needed to
    make this determination is missing (tenant not found, property not found), return False.
    """

    tenant = next((t for t in tenants if t.id == report.tenant_id), None)
    if tenant is None:
        return False # Tenant not found

    # Find the property associated with the tenant
    property = next((p for p in properties if p.id == tenant.property_id), None)
    if property is None:
        return False # Property not found

    # Check if the actor's landlord account matches the property's landlord account
    if actor.landlord_account_id == property.landlord_account_id:
        return True
    
