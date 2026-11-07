from pathlib import Path

from scripts.cost_tag_check import check_plan


PLAN_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "plan.json"


def test_check_plan_happy_path(capsys):
    result = check_plan(str(PLAN_PATH))
    output = capsys.readouterr().out

    assert result == 1
    assert output == (
        "Resources missing 'landlord_account_id' tag:\n"
        "  - aws_s3_bucket.listing_media\n"
        "  - aws_lambda_function.mls_feed_sync\n"
    )


def test_check_plan_is_idempotent(capsys):
    first_result = check_plan(str(PLAN_PATH))
    first_output = capsys.readouterr().out

    second_result = check_plan(str(PLAN_PATH))
    second_output = capsys.readouterr().out

    assert second_result == first_result == 1
    assert second_output == first_output
    assert first_output.count("aws_s3_bucket.listing_media") == 1
    assert first_output.count("aws_lambda_function.mls_feed_sync") == 1
