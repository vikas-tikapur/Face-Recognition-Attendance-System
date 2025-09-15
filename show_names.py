import pickle  # Library to load/save Python objects in binary format

# ---------------- Load Data ----------------
# Load the data from the 'encodings.p' file
with open('encodings.p', 'rb') as f:
    data = pickle.load(f)  # Deserialize the pickled data

print("Raw data loaded from encodings.p:")
print(data)  # Print the entire raw data to inspect its structure

# ---------------- Check Data Structure ----------------
# Case 1: If data is a dictionary containing 'names' key
if isinstance(data, dict) and 'names' in data:
    print("\n Registered Names:")
    print(data['names'])  # Print the list of registered names

# Case 2: If data is a tuple like (encodings, names)
elif isinstance(data, tuple) and len(data) == 2 and isinstance(data[1], list):
    print("\n Registered Names from tuple:")
    print(data[1])  # Print the names list from tuple

# Case 3: If data format is not recognized
else:
    print("\n Could not find 'names'. Data structure is not recognized.")
