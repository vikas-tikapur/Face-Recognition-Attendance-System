import pickle   # Module used to load and save Python objects in binary format

# Load the data from 'encodings.p' file (this file contains face encodings + names)
with open('encodings.p', 'rb') as f:
    data = pickle.load(f)  # Load the serialized (pickled) object


# Check if the loaded data is in correct format and print the registered names
if isinstance(data, dict) and 'names' in data:  # Ensure it's a dictionary and has 'names' key
    print("\n Registered Names:")
    unique_names = set(data['names'])  # Remove duplicates
    for name in unique_names:
        print(f"- {name}")   # Print each unique registered name
else:
    print("Error: Invalid data format in encodings.p")
