import re
from datetime import datetime, timedelta
from playwright.sync_api import Page, Locator

airport_calculator = {"RTM": "Rotterdam, Netherlands", "MAD": "Madrid, Spain"}


class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.kiwi.com/en"

        self.cookie_reject_btn = page.get_by_role("button", name="Reject all")
        self.choose_trip_type = page.get_by_role("button", name="Return")
        self.trip_type = {
            "one_way_choice": page.locator('[data-test="ModePopupOption-oneWay"]')
        }
        self.picked_locations_close = page.locator(
            'div[data-test="PlacePickerInputPlace-close"]'
        )
        self.depart_field = page.locator(
            '[data-test="PlacePickerInput-origin"] [data-test="SearchField-input"]'
        )
        self.arrive_field = page.locator(
            '[data-test="PlacePickerInput-destination"] [data-test="SearchField-input"]'
        )
        self.departure_time = page.get_by_text("Departure")
        self.accommodation_checkbox = page.locator(
            ".orbit-checkbox-icon-container"
        ).first
        self.search_button = page.locator('[data-test="LandingSearchButton"]')

    @staticmethod
    def unique_locator_exists(loc: Locator) -> bool:
        return loc.count() == 1

    @staticmethod
    def check_for_locators(loc: Locator) -> bool:
        return loc.count() > 0

    def enter_page(self) -> None:
        self.page.goto(self.url)

    def reject_cookie_alert_if_exist(self) -> None:
        if self.unique_locator_exists(self.cookie_reject_btn):
            self.cookie_reject_btn.click()

    def clear_dest_and_arrive_fields(self) -> None:
        while self.check_for_locators(self.picked_locations_close):
            self.picked_locations_close.first.click()

    def set_trip_type(self, trip_type_locator: Locator) -> None:
        self.choose_trip_type.click()
        trip_type_locator.click()

    def set_one_way_trip(self) -> None:
        self.set_trip_type(self.trip_type.get("one_way_choice"))

    def pick_airport(self, field_loc: Locator, code: str) -> None:
        if code not in airport_calculator.keys():
            raise "Fill location for given code"
        field_loc.fill(code)
        self.page.get_by_role("button", name=airport_calculator.get(code)).click()

    def set_flight_from(self, airport_code: str) -> None:
        self.pick_airport(field_loc=self.depart_field, code=airport_code)

    def set_flight_to(self, airport_code: str) -> None:
        self.pick_airport(field_loc=self.arrive_field, code=airport_code)

    def enter_calendar(self) -> None:
        self.departure_time.click()

    def toggle_accommodation(self, enabled: bool) -> None:
        if enabled:
            self.accommodation_checkbox.check()
        else:
            self.accommodation_checkbox.uncheck()

    def run_search(self) -> None:
        self.search_button.click()

    def wait_for_results(self) -> None:
        self.page.wait_for_selector('[data-test="ResultCardWrapper"]', state="visible")


class DatePicker:
    def __init__(self, page: Page):
        self.page = page

        self.set_dates = page.locator('[data-test="SearchFormDoneButton"]')
        self.calendar_left = page.locator(
            'div:nth-child(1) > div > div[data-test="CalendarContainer"]'
        )
        self.calendar_right = page.locator(
            'div:nth-child(2) > div > div[data-test="CalendarContainer"]'
        )

    @staticmethod
    def days_ahead(days: int) -> datetime:
        today = datetime.now()
        return today + timedelta(days=days)

    @staticmethod
    def day_button_name(day: int) -> None:
        return re.compile(f"^Left\s{day}\s")

    def set_date(self, date: datetime) -> None:
        current_date = datetime.now()
        calendar_loc: Locator = None
        if date.month == current_date.month:
            calendar_loc = self.calendar_left
        elif date.month % 12 == (current_date.month + 1) % 12:
            calendar_loc = self.calendar_right
        else:
            raise "Date too far in future, browsing calendar not supported"
        calendar_loc.get_by_role("button", name=self.day_button_name(date.day)).click()

    def set_calendar_dates(
        self, departure_date: datetime, return_date: datetime = None
    ) -> None:
        self.set_date(departure_date)
        if return_date:
            self.set_date(return_date)
        self.set_dates.click()
