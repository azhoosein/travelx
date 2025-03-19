import re

def extract_imeis(input_text):
    """Extract IMEI numbers from the given text."""
    # Define a regex pattern to match IMEI numbers (15 digits long)
    imei_pattern = r'\b\d{15}\b'
    
    # Find all matches in the text
    imeis = re.findall(imei_pattern, input_text)
    
    # Debugging output: print the IMEIs found
    print(f"Found IMEIs: {imeis}")
    
    return imeis

def save_imeis_to_file(imeis, filename):
    """Save the extracted IMEI numbers to a file."""
    try:
        with open(filename, 'w') as file:
            for imei in imeis:
                file.write(f"{imei}\n")
        print(f"IMEIs have been saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def main():
    # Sample input text (this could come from any source, like clipboard or file)
    input_text = """
    353914107150802
    Mobile Brand: Apple  Mobile Model: iPhone 11 Pro Max

    353915102433226
    Mobile Brand: Apple  Mobile Model: iPhone 11 Pro Max

    353953102476564
    Mobile Brand: Apple  Mobile Model: iPhone 11 Pro Max

    352849116405899
    Mobile Brand: Apple  Mobile Model: iPhone 11 Pro Max

    353902104694294
    Mobile Brand: Apple  Mobile Model: iPhone 11 Pro Max
    """
    
    # Extract IMEI numbers
    imeis = extract_imeis(input_text)
    
    # Save IMEIs to a file
    save_imeis_to_file(imeis, 'imeis.txt')

if __name__ == "__main__":
    main()
