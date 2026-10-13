
import re

from playwright.sync_api import expect


def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role(
        "heading", name="Toyota Yaris"
    )).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))

    page.get_by_role("link", name="Edit car").click()

    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()

    # Wait for the save operation to redirect to the detail page
    expect(page).to_have_url(
        re.compile(r"/cars/\d+$"),
        timeout=15000,
    )

    # Inspect the actual details after navigation
    print("DEBUG URL:", page.url, flush=True)
    print(
        "DEBUG PAGE:",
        page.locator("body").inner_text()[:2000],
        flush=True,
    )
    print(
        "DEBUG HEADING:",
        page.locator("h1").all_text_contents(),
        flush=True,
    )
    print(
        "DEBUG MODEL:",
        page.locator("#car-model").all_text_contents(),
        flush=True,
    )
    print(
        "DEBUG YEAR:",
        page.locator("#car-year").all_text_contents(),
        flush=True,
    )

    expect(
        page.get_by_role("heading", name="Honda Accord")
    ).to_be_visible(timeout=15000)

    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")

    page.reload()

    expect(
        page.get_by_role("heading", name="Honda Accord")
    ).to_be_visible(timeout=15000)

    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")

