ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,       # little or no exercise
    'light': 1.375,         # light exercise/sports 1-3 days/week
    'moderate': 1.55,       # moderate exercise/sports 3-5 days/week
    'active': 1.725,        # hard exercise/sports 6-7 days a week
    'very_active': 1.9      # very hard exercise/sports & physical job
}

def calculate_bmi(weight_kg, height_m):
    """
    Calculates the Body Mass Index (BMI).

    Formula: weight (kg) / (height (m) ^ 2)

    :param weight_kg: Weight in kilograms.
    :param height_m: Height in meters.
    :return: The calculated BMI as a float, or None if height is zero.
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")

    bmi = weight_kg / (height_m ** 2)
    return bmi

def get_bmi_category(bmi):
    """
    Determines the BMI category based on the BMI value.

    :param bmi: The BMI value.
    :return: A string representing the BMI category.
    """
    if bmi is None:
        return "N/A"
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def calculate_calories(weight_kg, height_m, age, gender, activity_level):
    """
    Calculates the estimated daily calorie needs using the Harris-Benedict equation.

    :param weight_kg: Weight in kilograms.
    :param height_m: Height in meters.
    :param age: Age in years.
    :param gender: 'male' or 'female'.
    :param activity_level: One of 'sedentary', 'light', 'moderate', 'active', 'very_active'.
    :return: The estimated daily calories as a float, or None on error.
    """
    if gender.lower() not in ['male', 'female']:
        raise ValueError("Invalid gender. Please use 'male' or 'female'.")

    if activity_level.lower() not in ACTIVITY_MULTIPLIERS:
        raise ValueError(
            f"Invalid activity level. Choose from: {', '.join(ACTIVITY_MULTIPLIERS.keys())}"
        )

    # The Harris-Benedict formula uses height in cm.
    height_cm = height_m * 100

    # Calculate Basal Metabolic Rate (BMR)
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:  # female
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

    # Calculate final daily calorie needs
    multiplier = ACTIVITY_MULTIPLIERS[activity_level.lower()]
    daily_calories = bmr * multiplier
    
    return daily_calories

