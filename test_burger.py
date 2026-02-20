import pytest
from mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import (
    INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
)


class TestBurger:

    def test_burger_initial(self):
        burger = Burger()
        assert burger.bun is None
        assert burger.ingredients == []

    def test_bund(self):
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_1_ingregient(self):
        """Проверяем добавление первого ингредиента в пустой бургер"""
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    def test_add_ingredients(self):
        """Проверяем добавление нескольких ингредиентов."""
        burger = Burger()
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient1
        assert burger.ingredients[1] == mock_ingredient2

    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()
        mock_ingredient3 = Mock()
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        burger.remove_ingredient(1)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient1
        assert burger.ingredients[1] == mock_ingredient3

    def test_remove_ingredient_with_error_index(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        with pytest.raises(IndexError):
            burger.remove_ingredient(5)

    def test_move_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()
        mock_ingredient3 = Mock()
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        burger.move_ingredient(0, 2)
        assert burger.ingredients[0] == mock_ingredient2
        assert burger.ingredients[1] == mock_ingredient3
        assert burger.ingredients[2] == mock_ingredient1

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_total", [
        (100, [], 200),
        (100, [50], 250),
        (200, [100, 150], 650),
        (150, [50, 75, 100], 525),
        (300, [200, 250, 300, 350], 1700),
    ])
    def test_get_price_mock_on(self, bun_price, ingredient_prices, expected_total):
        burger = Burger()
        # Мок булочки
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        assert burger.get_price() == expected_total

    def test_get_price_with_real_ingredients(self):
        burger = Burger()
        bun = Bun("black bun", 100)
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 50)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 75)
        burger.set_buns(bun)
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        assert burger.get_price() == 325

    def test_get_receipt_mock_on(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "red bun"
        mock_bun.get_price.return_value = 300
        burger.set_buns(mock_bun)
        mock_sauce = Mock()
        mock_sauce.get_type.return_value = "SAUCE"
        mock_sauce.get_name.return_value = "chili sauce"
        mock_sauce.get_price.return_value = 300
        mock_filling = Mock()
        mock_filling.get_type.return_value = "FILLING"
        mock_filling.get_name.return_value = "dinosaur"
        mock_filling.get_price.return_value = 200
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        receipt = burger.get_receipt()
        expected_receipt = (
            "(==== red bun ====)\n"
            "= sauce chili sauce =\n"
            "= filling dinosaur =\n"
            "(==== red bun ====)\n"
            "\n"
            "Price: 1100"
        )
        assert receipt == expected_receipt

    def test_get_receipt_with_real_ingredients(self):
        burger = Burger()
        bun = Bun("white bun", 200)
        sauce = Ingredient(INGREDIENT_TYPE_SAUCE, "sour cream", 200)
        filling = Ingredient(INGREDIENT_TYPE_FILLING, "sausage", 300)
        burger.set_buns(bun)
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)
        receipt = burger.get_receipt()
        expected_receipt = (
            "(==== white bun ====)\n"
            "= sauce sour cream =\n"
            "= filling sausage =\n"
            "(==== white bun ====)\n"
            "\n"
            "Price: 900"
        )
        assert receipt == expected_receipt

    def test_get_price_after_add_ingredients(self):
        """Проверяем расчёт цены после добавления нескольких ингредиентов."""
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        mock_ingredient1 = Mock()
        mock_ingredient1.get_price.return_value = 50
        mock_ingredient2 = Mock()
        mock_ingredient2.get_price.return_value = 75
        mock_ingredient3 = Mock()
        mock_ingredient3.get_price.return_value = 60
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        assert burger.get_price() == 385  # 100*2 + 50 + 75 + 60

    def test_move_ingredient_changes_order(self):
        """Проверяем, что перемещение ингредиента меняет порядок."""
        burger = Burger()
        mock_ingredient1 = Mock()
        mock_ingredient1.get_name.return_value = "hot sauce"
        mock_ingredient1.get_type.return_value = "SAUCE"
        mock_ingredient2 = Mock()
        mock_ingredient2.get_name.return_value = "cutlet"
        mock_ingredient2.get_type.return_value = "FILLING"
        mock_ingredient3 = Mock()
        mock_ingredient3.get_name.return_value = "sour cream"
        mock_ingredient3.get_type.return_value = "SAUCE"
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        burger.move_ingredient(0, 2)
        # Проверяем новый порядок
        assert burger.ingredients[0] == mock_ingredient2
        assert burger.ingredients[1] == mock_ingredient3
        assert burger.ingredients[2] == mock_ingredient1

    def test_get_receipt_after_remove_ingredients(self):
        """Проверяем формирование чека после удаления ингредиента."""
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 100
        mock_bun.get_name.return_value = "black bun"
        burger.set_buns(mock_bun)
        mock_ingredient1 = Mock()
        mock_ingredient1.get_price.return_value = 50
        mock_ingredient1.get_type.return_value = "SAUCE"
        mock_ingredient1.get_name.return_value = "hot sauce"
        mock_ingredient2 = Mock()
        mock_ingredient2.get_price.return_value = 75
        mock_ingredient2.get_type.return_value = "FILLING"
        mock_ingredient2.get_name.return_value = "cutlet"
        mock_ingredient3 = Mock()
        mock_ingredient3.get_price.return_value = 60
        mock_ingredient3.get_type.return_value = "SAUCE"
        mock_ingredient3.get_name.return_value = "sour cream"
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)
        burger.remove_ingredient(0)  # Удаляем первый ингредиент
        receipt = burger.get_receipt()
        expected_receipt = (
            "(==== black bun ====)\n"
            "= filling cutlet =\n"
            "= sauce sour cream =\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 335"  # 100*2 + 75 + 60
        )
        assert receipt == expected_receipt
