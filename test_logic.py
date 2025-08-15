import pytest
from . import logic

def test_calculate_bmi():
    """Tests the BMI calculation with valid data."""
    assert logic.calculate_bmi(weight_kg=70, height_m=1.75) == pytest.approx(22.86, 0.01)

def test_calculate_bmi_zero_height():
    """Tests that calculating BMI with zero height raises a ValueError."""
    with pytest.raises(ValueError, match="Height must be greater than zero."):
        logic.calculate_bmi(weight_kg=70, height_m=0)

def test_get_bmi_category():
    """Tests the BMI categorization logic."""
    assert logic.get_bmi_category(18.4) == "Underweight"
    assert logic.get_bmi_category(22.0) == "Normal weight"
    assert logic.get_bmi_category(27.0) == "Overweight"
    assert logic.get_bmi_category(31.0) == "Obesity"

def test_calculate_calories():
    """Tests the calorie calculation with a valid set of inputs."""
    calories = logic.calculate_calories(
        weight_kg=70,
        height_m=1.75,
        age=30,
        gender='male',
        activity_level='moderate'
    )
    assert calories == pytest.approx(2695.35, 0.01)

def test_calculate_calories_invalid_gender():
    """Tests that calorie calculation raises a ValueError for an invalid gender."""
    with pytest.raises(ValueError, match="Invalid gender"):
        logic.calculate_calories(70, 1.75, 30, 'unknown', 'moderate')

def test_calculate_calories_invalid_activity():
    """Tests that calorie calculation raises a ValueError for an invalid activity level."""
    with pytest.raises(ValueError, match="Invalid activity level"):
        logic.calculate_calories(70, 1.75, 30, 'male', 'none')