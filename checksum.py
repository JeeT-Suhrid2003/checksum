def calculate_checksum(message):
    ascii_values = [ord(char) for char in message]
    words = [(ascii_values[i] << 8) + ascii_values[i + 1] for i in range(0, len(ascii_values) - 1, 2)]
    if len(ascii_values) % 2 != 0:
        words.append(ascii_values[-1] << 8)
    checksum = sum(words)
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    return checksum

def verify_checksum(message, received_checksum):
    ascii_values = [ord(char) for char in message]
    words = [(ascii_values[i] << 8) + ascii_values[i + 1] for i in range(0, len(ascii_values) - 1, 2)]
    if len(ascii_values) % 2 != 0:
        words.append(ascii_values[-1] << 8)
    total = sum(words)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    total += received_checksum
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return total == 0xFFFF

original_message = "VITCCNCOURSE"
original_checksum = calculate_checksum(original_message)

print(f"Original Message: {original_message}")
print(f"Original Checksum: {hex(original_checksum)}")

is_valid_original = verify_checksum(original_message, original_checksum)
print("Checksum verification for original message passed:", is_valid_original)

modified_message = "VITCCMCOURSE"
print(f"\nModified Message: {modified_message}")

is_valid_modified = verify_checksum(modified_message, original_checksum)
print("Checksum verification for modified message passed:", is_valid_modified)

print(f"The new checksum for modified message should be: {hex(calculate_checksum(modified_message))}")
