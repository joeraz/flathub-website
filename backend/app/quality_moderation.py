import datetime
from dataclasses import dataclass

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from fastapi.responses import ORJSONResponse
from fastapi_sqlalchemy import db
from pydantic import BaseModel

from . import models
from .db import get_all_appids_for_frontend
from .logins import LoginStatusDep

router = APIRouter(prefix="/quality-moderation", default_response_class=ORJSONResponse)


@dataclass
class Guideline:
    id: str
    url: str
    needed_to_pass_since: datetime.datetime
    read_only: bool = False


@dataclass
class GuidelineCategory:
    id: str
    guidelines: list[Guideline]


GUIDELINES = [
    GuidelineCategory(
        "general",
        [
            Guideline(
                "general-no-trademark-violations",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#no-trademark-violations",
                datetime.datetime(2023, 9, 1),
            ),
        ],
    ),
    GuidelineCategory(
        "app-icon",
        [
            # This guideline can't be checked, as currently icons are a maximal size of 128x128
            # Guideline(
            #     "app-icon-size",
            #     "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#icon-size",
            #     datetime.datetime(2023, 9, 1),
            # ),
            Guideline(
                "app-icon-footprint",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#reasonable-footprint",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-icon-contrast",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#good-contrast",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-icon-detail",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#not-too-much-or-too-little-detail",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-icon-no-baked-in-shadows",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#no-baked-in-shadows",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-icon-in-line-with-contemporary-styles",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#in-line-with-contemporary-styles",
                datetime.datetime(2023, 9, 1),
            ),
        ],
    ),
    GuidelineCategory(
        "app-name",
        [
            Guideline(
                "app-name-not-too-long",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#not-too-long",
                datetime.datetime(2023, 9, 1),
                read_only=True,
            ),
            Guideline(
                "app-name-just-the-name",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#just-the-name",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-no-weird-formatting",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#no-weird-formatting",
                datetime.datetime(2023, 9, 1),
            ),
        ],
    ),
    GuidelineCategory(
        "app-summary",
        [
            Guideline(
                "app-summary-not-too-long",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#not-too-long-1",
                datetime.datetime(2023, 9, 1),
                read_only=True,
            ),
            Guideline(
                "app-summary-not-technical",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#not-technical",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-summary-no-weird-formatting",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#no-weird-formatting-1",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-summary-dont-repeat-app-name",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#dont-repeat-the-name",
                datetime.datetime(2023, 9, 1),
            ),
            Guideline(
                "app-summary-dont-start-with-an-article",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#dont-start-with-an-article",
                datetime.datetime(2023, 9, 1),
            ),
        ],
    ),
    GuidelineCategory(
        "screenshots",
        [
            Guideline(
                "screenshots-at-least-one-screenshot",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#at-least-one-screenshot",
                datetime.datetime(2023, 9, 30),
                read_only=True,
            ),
            Guideline(
                "screenshots-tag-screenshots-with-correct-language",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#tag-screenshots-with-correct-language",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-just-the-app-window",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#just-the-app-window",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-take-screenshots-on-linux",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#take-screenshots-on-linux",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-default-settings",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#default-settings",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-include-window-shadow-and-rounded-corners",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#include-window-shadow-and-rounded-corners",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-reasonable-window-size",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#reasonable-window-size",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-good-content",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#good-content",
                datetime.datetime(2023, 9, 30),
            ),
            Guideline(
                "screenshots-up-to-date",
                "https://docs.flathub.org/docs/for-app-authors/appdata-guidelines/quality-guidelines/#up-to-date",
                datetime.datetime(2023, 9, 30),
            ),
        ],
    ),
]


class UpsertQualityModeration(BaseModel):
    guideline_id: str
    passed: bool


def register_to_app(app: FastAPI):
    app.include_router(router)


def quality_moderator_only(login: LoginStatusDep):
    if not login.user or not login.state.logged_in():
        raise HTTPException(status_code=401, detail="not_logged_in")
    if not login.user.is_quality_moderator:
        raise HTTPException(status_code=403, detail="not_quality_moderator")

    return login


@router.get("/status")
def get_quality_moderation_status(_moderator=Depends(quality_moderator_only)):
    return {
        "apps": [
            {
                "id": appId,
                "quality-moderation-status": get_quality_moderation_status_for_appid(
                    appId
                ),
            }
            for appId in get_all_appids_for_frontend()
        ]
    }


@router.get("/{app_id}")
def get_quality_moderation_for_app(
    app_id: str = Path(
        min_length=6,
        max_length=255,
        regex=r"^[A-Za-z_][\w\-\.]+$",
        example="org.gnome.Glade",
    ),
    _moderator=Depends(quality_moderator_only),
):
    items = models.QualityModeration.by_appid(db, app_id)
    return {
        "categories": GUIDELINES,
        "marks": {item.guideline_id: item for item in items},
    }


@router.post("/{app_id}")
def set_quality_moderation_for_app(
    body: UpsertQualityModeration,
    app_id: str = Path(
        min_length=6,
        max_length=255,
        regex=r"^[A-Za-z_][\w\-\.]+$",
        example="org.gnome.Glade",
    ),
    moderator=Depends(quality_moderator_only),
):
    models.QualityModeration.upsert(
        db, app_id, body.guideline_id, body.passed, moderator.user.id
    )


@router.get("/{app_id}/status")
def get_quality_moderation_status_for_app(
    app_id: str = Path(
        min_length=6,
        max_length=255,
        regex=r"^[A-Za-z_][\w\-\.]+$",
        example="org.gnome.Glade",
    )
):
    return get_quality_moderation_status_for_appid(app_id)


def get_quality_moderation_status_for_appid(app_id: str):
    marks = models.QualityModeration.by_appid(db, app_id)
    unrated = 0

    checks = []

    for category in GUIDELINES:
        for guideline in category.guidelines:
            if guideline.needed_to_pass_since > datetime.datetime.now():
                continue

            firstMatch = next(
                (mark for mark in marks if mark.guideline_id == guideline.id), None
            )

            checks.append(
                {
                    "category": category.id,
                    "guideline": guideline.id,
                    "needed_to_pass_since": guideline.needed_to_pass_since,
                    "passed": firstMatch.passed if firstMatch else None,
                    "updated_at": firstMatch.updated_at if firstMatch else None,
                }
            )

            if firstMatch is None:
                unrated += 1

    passed = len(
        [
            item
            for item in checks
            if item["passed"] and item["needed_to_pass_since"] < datetime.datetime.now()
        ]
    )
    not_passed = len(
        [
            item
            for item in checks
            if item["passed"] is False
            and item["needed_to_pass_since"] < datetime.datetime.now()
        ]
    )

    def last_updated(checks):
        return max([check.updated_at for check in checks] + [datetime.datetime.min])

    return {
        "passes": unrated + not_passed == 0,
        "unrated": unrated,
        "passed": passed,
        "not-passed": not_passed,
        "last-updated": last_updated(marks),
    }
