import os

def reverse_numbers(input_file):
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"The file {input_file} was not found.")
            return
        
        # Read the numbers from the input file
        with open(input_file, 'r') as file:
            numbers = file.read().splitlines()
        
        if not numbers:
            print(f"The file {input_file} is empty.")
            return

        # Reverse the list of numbers
        reversed_numbers = numbers[::-1]

        # Print the reversed numbers to the terminal
        for number in reversed_numbers:
            print(number)
    
    except Exception as e:
        print(f"An error occurred: {e}")


input_filename = 'reverse.txt'

reverse_numbers(input_filename)
