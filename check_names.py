import pickle

# Load the data from encodings.p
with open('encodings.p', 'rb') as f:
    data = pickle.load(f)

# Check and print names
if isinstance(data, dict) and 'names' in data:
    print("\n Registered Names:")
    unique_names = set(data['names'])  # Remove duplicates
    for name in unique_names:
        print(f"- {name}")
else:
    print("⚠️ Error: Invalid data format in encodings.p")
