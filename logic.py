def calculate_bmi(weight_kg, height_m):
    """
    Calculates the Body Mass Index (BMI).

    Formula: weight (kg) / (height (m) ^ 2)

    :param weight_kg: Weight in kilograms.
    :param height_m: Height in meters.
    :return: The calculated BMI as a float, or None if height is zero.
    """
    if height_m <= 0:
        print("Error: Height must be greater than zero.")
        return None
    
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

def calculate_calories(weight_kg, height_cm, age, gender, activity_level):
    """
    Calculates the estimated daily calorie needs using the Harris-Benedict equation.

    :param weight_kg: Weight in kilograms.
    :param height_cm: Height in centimeters.
    :param age: Age in years.
    :param gender: 'male' or 'female'.
    :param activity_level: One of 'sedentary', 'light', 'moderate', 'active', 'very_active'.
    :return: The estimated daily calories as a float, or None on error.
    """
    activity_multipliers = {
        'sedentary': 1.2,       # little or no exercise
        'light': 1.375,         # light exercise/sports 1-3 days/week
        'moderate': 1.55,       # moderate exercise/sports 3-5 days/week
        'active': 1.725,        # hard exercise/sports 6-7 days a week
        'very_active': 1.9      # very hard exercise/sports & physical job
    }

    if gender.lower() not in ['male', 'female']:
        print("Error: Invalid gender. Please use 'male' or 'female'.")
        return None

    if activity_level.lower() not in activity_multipliers:
        print(f"Error: Invalid activity level. Choose from: {', '.join(activity_multipliers.keys())}")
        return None

    # Calculate Basal Metabolic Rate (BMR)
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:  # female
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

    # Calculate final daily calorie needs
    multiplier = activity_multipliers[activity_level.lower()]
    daily_calories = bmr * multiplier
    
    return daily_calories


if __name__ == '__main__':
    # --- Example Usage ---

    # --- BMI Calculation Example ---
    print("--- BMI Calculation ---")
    my_weight_kg = 70  # 70 kg
    my_height_m = 1.75 # 1.75 meters
    
    my_bmi = calculate_bmi(my_weight_kg, my_height_m)
    if my_bmi is not None:
        bmi_category = get_bmi_category(my_bmi)
        print(f"Weight: {my_weight_kg} kg, Height: {my_height_m} m")
        print(f"Your BMI is: {my_bmi:.2f}")
        print(f"This is considered: {bmi_category}")

    print("\n" + "="*30 + "\n")

    # --- Calorie Calculation Example ---
    print("--- Daily Calorie Needs Calculation ---")
    my_height_cm = 175 # 175 cm
    my_age = 30
    my_gender = 'male'
    my_activity = 'moderate'

    daily_cals = calculate_calories(my_weight_kg, my_height_cm, my_age, my_gender, my_activity)
    if daily_cals is not None:
        print(f"For a {my_age}-year-old {my_gender} weighing {my_weight_kg} kg with a '{my_activity}' activity level:")
        print(f"Estimated daily calorie needs are: {daily_cals:.2f} kcal")
