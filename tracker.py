import argparse
from db import Database
import logic

# Define a constant for the database file to ensure consistency
DB_FILE = "mydatabase.db"

def handle_register(args):
    """
    Handles the 'register' command to add a new user to the database.
    """
    print(f"Attempting to register user: {args.name} ({args.email})")
    with Database(DB_FILE) as db:  # The context manager handles connection and commit/close
        db.initialize_db()  # Ensures the 'users' table exists
        user_id = db.insert_record(args.name, args.email)
        if user_id:
            print(f"User '{args.name}' registered successfully with ID: {user_id}")

def handle_calculate(args):
    """
    Handles the 'calculate' command to compute and display health metrics.
    """
    print("\n--- Health Metrics Calculation ---")
    
    # 1. BMI Calculation
    bmi = logic.calculate_bmi(args.weight, args.height)
    if bmi is not None:
        bmi_category = logic.get_bmi_category(bmi)
        print(f"BMI: {bmi:.2f} ({bmi_category})")
    else:
        print("Could not calculate BMI. Please check your height and weight.")

    # 2. Calorie Calculation
    # The logic function requires height in cm, so we convert it from meters.
    height_cm = args.height * 100
    calories = logic.calculate_calories(args.weight, height_cm, args.age, args.gender, args.activity)
    if calories is not None:
        print(f"Estimated Daily Calorie Needs: {calories:.2f} kcal")
    else:
        print("Could not calculate calories. Please check your input values.")

def handle_list_users(args):
    """
    Handles the 'show-users' command to list all registered users.
    """
    print("\n--- Registered Users ---")
    with Database(DB_FILE) as db:  # The context manager handles connection and close
        users = db.fetch_all_records()
        if users:
            # Print a formatted header
            print(f"{'ID':<5} {'Name':<20} {'Email':<30}")
            print("-" * 55)
            for user in users:
                print(f"{user[0]:<5} {user[1]:<20} {user[2]:<30}")
        else:
            print("No users found in the database.")

def main():
    """
    Main function to set up and run the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="A simple command-line fitness tracker."
    )
    # Set a default function to print help if no command is provided
    parser.set_defaults(func=lambda args: parser.print_help())
    
    subparsers = parser.add_subparsers(help='Available commands')

    # --- Register command ---
    parser_register = subparsers.add_parser(
        'register', 
        help='Register a new user.',
        description='Adds a new user with a name and a unique email to the database.'
    )
    parser_register.add_argument('name', type=str, help='Name of the user.')
    parser_register.add_argument('email', type=str, help='Email address of the user.')
    parser_register.set_defaults(func=handle_register)

    # --- Calculate command ---
    parser_calculate = subparsers.add_parser(
        'calculate', 
        help='Calculate BMI and daily calorie needs.',
        description='Calculates BMI and estimated daily calorie needs based on user-provided data.'
    )
    parser_calculate.add_argument('--weight', type=float, required=True, help='Weight in kilograms (e.g., 70.5).')
    parser_calculate.add_argument('--height', type=float, required=True, help='Height in meters (e.g., 1.75).')
    parser_calculate.add_argument('--age', type=int, required=True, help='Age in years.')
    parser_calculate.add_argument('--gender', type=str, required=True, choices=['male', 'female'], help='Gender: "male" or "female".')
    parser_calculate.add_argument(
        '--activity', type=str, required=True, 
        choices=['sedentary', 'light', 'moderate', 'active', 'very_active'],
        help='Your daily activity level.'
    )
    parser_calculate.set_defaults(func=handle_calculate)

    # --- Show Users command ---
    parser_list = subparsers.add_parser(
        'show-users', 
        help='List all registered users.',
        description='Fetches and displays all users currently in the database.'
    )
    parser_list.set_defaults(func=handle_list_users)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
