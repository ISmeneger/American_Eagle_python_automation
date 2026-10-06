from ui.pages.mens_clothes_page import MensClothesPage


class ProductCatalogSteps:
    def __init__(self, driver):
        self.mens_clothes_page = MensClothesPage(driver)

    def open_first_available_mens_product(self) -> str:
        self.mens_clothes_page.move_to_men_menu()
        self.mens_clothes_page.click_view_all_categories()

        self.mens_clothes_page.close_popup_if_available()

        return (
            self.mens_clothes_page
            .open_first_available_product()
        )