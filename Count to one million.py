def write_numbers_to_file(filename, count):
    with open(filename, 'w') as file:
        for number in range(1, count + 1):
            file.write(f"{number}\n")

if __name__ == "__main__":
    count = int(input("Enter the number to count to: "))
    write_numbers_to_file('numbers.txt', count)
