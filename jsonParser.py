import json

def parse_json_to_2d_time_array(json_data):
    try:
        # Extract the 'start' and 'end' times
        time_values_2d = [[edit['start'], edit['end']] for edit in json_data]

        return time_values_2d.reverse()

    except KeyError as e:
        print(f"Error: Missing key in JSON structure - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")