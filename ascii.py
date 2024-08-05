# Licenced under the MIT Licence

import pyfiglet

# List of additional fonts available in pyfiglet
additional_fonts = [
    'banner', 'big', 'block', 'bubble', 'digital', 'ivrit', 'lean', 
    'mini', 'script', 'shadow', 'small', 'smscript', 'standard', 'term'
]

# Function to create ASCII art from text with a specified font
def create_ascii_art(text, font='standard'):
    try:
        # Check if the specified font is in the list of additional fonts
        if font.lower() in additional_fonts:
            ascii_art = pyfiglet.figlet_format(text, font=font)
        else:
            # Use 'standard' font if the specified font is not found
            print(f"Font '{font}' not found. Using 'standard' font.")
            ascii_art = pyfiglet.figlet_format(text, font='standard')
        return ascii_art
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to print each font's name using its own font style
def expressfont_command():
    print("Express Font Display:")
    for font in additional_fonts:
        ascii_name = create_ascii_art(font.upper(), font=font)
        print(f"{ascii_name}\n{font}\n")

# Function to print numbered list of available fonts to the user
def print_available_fonts():
    print("Available Fonts:")
    for i, font in enumerate(additional_fonts, 1):
        print(f"{i}. {font}")

# Function to handle the 'ascii' command
def handle_ascii_command(args):
    if args:
        user_input = ' '.join(args)
    else:
        user_input = input("Enter text to convert to ASCII art: ")

    font_choice = get_font_choice()  # Get user's font choice based on selection number

    ascii_art = create_ascii_art(user_input, font=font_choice)
    if ascii_art:
        print(ascii_art)

# Function to handle the 'fonts' command
def handle_fonts_command():
    print_available_fonts()

# Function to get user's font choice based on selection number
def get_font_choice():
    while True:
        try:
            font_num = int(input("Enter the number of the font you want (press Enter for standard): ").strip())
            if 1 <= font_num <= len(additional_fonts):
                return additional_fonts[font_num - 1]
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            return 'standard'  # Default to 'standard' font if user doesn't enter a number

# Main function to handle command input from the user
def main():
    print("Welcome to ASCII Art Generator!")
    print("Type 'help' to get a list of all commands and their purposes.")

    while True:
        command_line = input("\nEnter command: ").strip().lower()
        command_parts = command_line.split()

        if not command_parts:
            continue  # If no command entered, continue to next iteration

        command = command_parts[0]
        args = command_parts[1:]

        # Help list

        if command == 'help':
            print("\nList of commands:")
            print("ascii [text]:  converts the text to ASCII art")
            print("fonts:         shows the available fonts for ASCII art")
            print("expressfont:   displays each font's name using its own font style")
            print("exit:          exits the program")
            print("game:          gives the URL to a python game")

            # Processes help list

        elif command == 'ascii':
            handle_ascii_command(args)

        elif command == 'fonts':
            handle_fonts_command()

        elif command == 'expressfont':
            expressfont_command()

        elif command == 'ad':
            print("Advertisement: Go to https://github.com/Earth1283/Flappy-Bird-Python for my Python Flappy Bird game")

        elif command == 'game':
            print("Go to https://github.com/Earth1283/Flappy-Bird-Python for a python-powered flappy bird game!")

        elif command == 'exit':
            print("Bye mate.")
            break

        else:
            print("Huh? Can't undestand what you wrote. Type 'help' for list of commands.")

if __name__ == "__main__":
    main()
