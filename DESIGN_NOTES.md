# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide whether two resources in the
same run are "the same" for dedup purposes, and why running it twice against an unchanged
plan file produces identical output and exit code without the script keeping any record
between runs. Use the word "idempotency" in your explanation.

The check uses the Terraform resource `address` (for example,
`aws_s3_bucket.listing_media`) as its deduplication key. It reports each missing-tag address
only once, preserving the order in which addresses first appear in the plan. For an unchanged
plan file, the check reads the same input and applies the same action and tag checks, so the
output and exit code are identical each time. This idempotency is repeatable validation, not a
stateful operation: the script does not modify the plan or store records between runs.

## Any other decision with a non-obvious alternative

The required tag is `landlord_account_id` because the landlord account is the billing unit;
tags such as `tenant_id` do not identify the billing owner. The check is limited to create and
update actions, since no-op and delete changes do not represent resources being provisioned or
changed with new billing tags.
