def process_data(input_data):
    # Placeholder function for processing input data
    processed_data = input_data  # Replace with actual processing logic
    return processed_data

def save_processed_data(output_file, data):
    with open(output_file, 'w') as file:
        file.write(data)

if __name__ == "__main__":
    input_data = "Sample data"  # Replace with actual data source
    processed_data = process_data(input_data)
    save_processed_data('output.txt', processed_data)