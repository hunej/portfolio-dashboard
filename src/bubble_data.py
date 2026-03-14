def generate_bubble_data(data):
    # Process the input data to generate bubble chart data
    bubble_data = []
    for item in data:
        bubble_data.append({
            'x': item['x_value'],
            'y': item['y_value'],
            'r': item['radius_value'],
            'label': item['label']
        })
    return bubble_data

def load_bubble_data_from_json(file_path):
    import json
    with open(file_path, 'r') as file:
        data = json.load(file)
    return generate_bubble_data(data)

def save_bubble_data_to_json(bubble_data, file_path):
    import json
    with open(file_path, 'w') as file:
        json.dump(bubble_data, file)