from ui.pages.home_page import HomePage
from ui.pages.mens_clothes_page import MensClothesPage


class ProductCatalogSteps:
    def __init__(self, driver):
        self.home_page = HomePage(driver)
        self.mens_clothes_page = MensClothesPage(driver)

    def open_mens_clothes_catalog(self):
        self.home_page.open()

        self.mens_clothes_page.move_to_men_menu()
        self.mens_clothes_page.click_view_all_categories()
        self.mens_clothes_page.close_popup_if_available()

    def open_first_available_mens_product(self) -> str:
        self.open_mens_clothes_catalog()

        return (
            self.mens_clothes_page
            .open_first_available_product()
        )