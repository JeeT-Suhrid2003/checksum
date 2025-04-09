def calculate_checksum(values, block_size):
    max_value = (1 << block_size) - 1
    converted_values = [(num + (1 << block_size)) % (1 << block_size) for num in values]
    
    checksum = sum(converted_values)
    while checksum > max_value:
        checksum = (checksum & max_value) + (checksum >> block_size)
    
    return (~checksum) & max_value

def verify_checksum(values, received_checksum, block_size):
    max_value = (1 << block_size) - 1  # Define max_value here
    converted_values = [(num + (1 << block_size)) % (1 << block_size) for num in values]
    
    # Sum data words and received checksum
    total = sum(converted_values) + received_checksum
    while total > max_value:
        total = (total & max_value) + (total >> block_size)
    
    # Debug output
    print("\nVerification Process:")
    print(f"Converted Data Values: {converted_values}")
    print(f"Sum of Data + Checksum: {total} (Expected: {max_value})")
    print("No error detected." if total == max_value else "Error detected!")

# Rest of the code (user_input_mode) remains unchanged
def user_input_mode():
    while True:
        print("1. Enter binary numbers")
        print("2. Enter decimal numbers")
        print("3. Verify checksum")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice in ["1", "2"]:
            block_size = int(input("Enter block size: "))
            num_blocks = int(input("Enter number of blocks: "))
            values = []
            
            for i in range(num_blocks):
                val = input(f"Enter Block {i+1} ({'binary' if choice == '1' else 'decimal'}): ")
                values.append(int(val, 2) if choice == "1" else int(val))
            
            checksum = calculate_checksum(values, block_size)
            print(f"Checksum (decimal): {checksum}")
            print(f"Checksum (binary): {format(checksum, f'0{block_size}b')}")
            
            error_index = int(input("Enter block index to introduce an error (1-based index, 0 to skip): ")) - 1
            if error_index >= 0:
                error_value = input(f"Enter new value for Block {error_index + 1}: ")
                values[error_index] = int(error_value, 2) if choice == "1" else int(error_value)
                print("\nRecalculating checksum at receiver:")
                verify_checksum(values, checksum, block_size)
        
        elif choice == "3":
            block_size = int(input("Enter block size: "))
            num_blocks = int(input("Enter number of blocks: "))
            values = [int(input(f"Enter Block {i+1} (decimal): ")) for i in range(num_blocks)]
            received_checksum = int(input("Enter received checksum (decimal): "))
            verify_checksum(values, received_checksum, block_size)
        
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    user_input_mode()
