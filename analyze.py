import re
import sys

# 2MB page size
PAGE_SIZE_2MB = 2 * 1024 * 1024

def find_optimal_pages(memory_accesses, threshold):
    """
    Find and align unique addresses from the memory access log based on a threshold.
    
    :param memory_accesses: List of memory access logs.
    :param threshold: Threshold address for filtering.
    :return: None
    """
    # Create a set to hold unique addresses
    unique_addresses = set()
    
    for access in memory_accesses:
        # Extract the hexadecimal address from the memory access log
        match = re.search(r'0x[0-9a-fA-F]+', access)
        if match:
            address = match.group(0)
            print(f"Found address: {address}")  # Debugging print
            unique_addresses.add(int(address, 16))  # Add as integer

    # Check if any addresses were found
    if not unique_addresses:
        print("No valid addresses found in memory access log.")
        return

    # Filter addresses based on the threshold
    optimal_addresses = [addr for addr in unique_addresses if addr > threshold]
    
    # Align each address to the 2MB boundary
    aligned_addresses = [addr - (addr % PAGE_SIZE_2MB) for addr in optimal_addresses]

    # Limit to 8 large pages
    aligned_addresses = aligned_addresses[:8]

    # Print out the aligned addresses for debugging purposes
    print(f"Unique aligned addresses (limited to 8): {aligned_addresses}")  # Debugging print

def generate_large_page_addresses(start, end, count):
    """
    Generate count aligned addresses for large pages between start and end.
    
    :param start: Start address (inclusive).
    :param end: End address (exclusive).
    :param count: Number of addresses to generate.
    :return: List of valid aligned addresses.
    """
    addresses = []
    
    # Align the start address to the nearest 2MB boundary
    start = (start + (2 * 1024 * 1024) - 1) & ~((2 * 1024 * 1024) - 1)

    for i in range(count):
        address = start + i * (2 * 1024 * 1024)  # Increment by 2MB
        if address < end:
            addresses.append(address)
        else:
            break
            
    return addresses

def main():
    # Check if the script received an argument for the threshold
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <threshold>")
        return

    # Get the threshold from the command line argument
    try:
        threshold = int(sys.argv[1])
    except ValueError:
        print("Threshold must be an integer.")
        return

    # Path to your log file
    log_file_path = "parsed_perf_data.txt"
    
    try:
        with open(log_file_path, "r", encoding='utf-8', errors='ignore') as log_file:
            memory_accesses = log_file.readlines()
        
        # Call the function to find optimal pages (no file write)
        find_optimal_pages(memory_accesses, threshold)
        
        # Now use the generate_large_page_addresses function
        start_address = 0x20000000  # Example starting address (in hex)
        end_address = 0x30000000    # Example ending address (in hex)
        count = 8                    # Number of addresses to generate

        generated_addresses = generate_large_page_addresses(start_address, end_address, count)

        # Write only the generated addresses to largepages.txt
        with open("largepages.txt", "w") as f:  # 'w' to overwrite the file
            for address in generated_addresses:
                f.write(f"{address}\n")
                print(f"Generated address: {hex(address)}")
        
    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

