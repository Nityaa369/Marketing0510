import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from studio.config import load_brand, load_layout  # noqa: E402

GOOD = {
    "id": "t01",
    "campaign": "TEST",
    "icp": "New law grads",
    "headline": "You can qualify NCA, then the *Canadian bar*, from home.",
    "supporting": "Qualify through the NCA from home. Become eligible for the Canadian bar.",
    "cta": "JOIN NOW",
    "hero_prompt": "a young Indian woman lawyer in a black blazer",
}


@pytest.fixture
def layout():
    return load_layout("ncacanada")


@pytest.fixture
def program(layout):
    return load_brand()["programs"][layout["program"]]


@pytest.fixture
def good_row():
    return dict(GOOD)


def write_sheet(path: Path, rows: list[dict]) -> Path:
    import pandas as pd

    pd.DataFrame(rows).to_excel(path, index=False)
    return path
