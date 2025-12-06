import pytest
from playwright.sync_api import Page
from pages.kiwi_page import MainPage, DatePicker


# @pytest.mark.parametrize(
#     "start, stop, days_delay", [("RTM", "MAD", 5), ("RTM", "MAD", 10)]
# )
@pytest.mark.parametrize("start, stop, days_delay", [("RTM", "MAD", 10)])
def test_basic_search(page: Page, start: str, stop: str, days_delay: int):
    """
    Test to verify basic one-way flight search from Rotterdam to Madrid
    """
    kiwi_page = MainPage(page)
    date_picker = DatePicker(page)

    kiwi_page.enter_page()
    kiwi_page.reject_cookie_alert_if_exist()
    kiwi_page.set_one_way_trip()
    kiwi_page.clear_dest_and_arrive_fields()
    kiwi_page.set_flight_from(start)
    kiwi_page.set_flight_to(stop)
    kiwi_page.enter_calendar()
    date_picker.set_calendar_dates(departure_date=date_picker.days_ahead(days_delay))
    kiwi_page.toggle_accommodation(enabled=False)
    kiwi_page.run_search()
    kiwi_page.wait_for_results()
    page.screenshot(path=f"last-result-{days_delay}.png")
    assert page.title() == "Rotterdam‎ – Madrid‎ trips", "Not finished on expected page"
