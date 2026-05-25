from app import person_option_label, top_records


def test_top_records_ignores_empty_ranking_rows():
    records = [
        {"name": "United States", "papers": 3},
        {"name": "Belgium", "papers": 0},
        {"name": "United Kingdom", "papers": 1},
        {"name": "Italy", "papers": None},
    ]

    ranking = top_records(records, "papers", limit=5)

    assert ranking == [
        {"name": "United States", "papers": 3},
        {"name": "United Kingdom", "papers": 1},
    ]


def test_person_option_label_shows_orcid_when_available():
    label = person_option_label(
        {
            "name": "Ada Lovelace",
            "orcid": "0000-0001-1111-1111",
        }
    )

    assert label == "Ada Lovelace · ORCID 0000-0001-1111-1111"
