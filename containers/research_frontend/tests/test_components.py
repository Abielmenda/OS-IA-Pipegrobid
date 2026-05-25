from components import funding_records_for_display


def test_funding_records_for_display_renames_and_formats_unknown_amounts():
    records = [
        {
            "name": "United States",
            "papers": 4,
            "projects": 9,
            "funding_amount": None,
            "funding_amount_known": False,
        },
        {
            "name": "United Kingdom",
            "papers": 1,
            "projects": 1,
            "funding_amount": 6898910.0,
            "funding_amount_known": True,
        },
    ]

    display_records = funding_records_for_display(records)

    assert display_records[0]["financiacion conocida asociada"] == "N/D"
    assert display_records[1]["financiacion conocida asociada"] == 6898910.0
    assert "funding_amount" not in display_records[0]
    assert "funding_amount_known" not in display_records[0]
