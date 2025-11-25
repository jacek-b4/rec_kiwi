import pytest
from playwright.sync_api import Page
from pages.kiwi_page import MainPage, DatePicker


# @pytest.mark.parametrize(
#     "start, stop, days_delay", [("RTM", "MAD", 5), ("RTM", "MAD", 10)]
# )
@pytest.mark.parametrize("start, stop, days_delay", [("RTM", "MAD", 10)])
def test_kiwi(page: Page, start: str, stop: str, days_delay: int):
    mp = MainPage(page)
    dp = DatePicker(page)

    mp.enter_page()
    mp.reject_cookie_alert_if_exist()
    mp.set_one_way_trip()
    mp.clear_dest_and_arrive_fields()
    mp.set_flight_from(start)
    mp.set_flight_to(stop)
    mp.enter_calendar()
    dp.set_calendar_dates(departure_date=dp.days_ahead(days_delay))
    mp.toggle_accommodation(enabled=False)
    mp.run_search()
    mp.wait_for_results()
    page.screenshot(path=f"last-result-{days_delay}.png")
    assert page.title() == "Rotterdam‎ – Madrid‎ trips", "Not finished on expected page"
