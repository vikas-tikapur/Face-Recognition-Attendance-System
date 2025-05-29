import pickle

# Load the data from the file
with open('encodings.p', 'rb') as f:
    data = pickle.load(f)

print("Raw data loaded from encodings.p:")
print(data)

# If data is a dictionary with 'names' key
if isinstance(data, dict) and 'names' in data:
    print("\n Registered Names:")
    print(data['names'])

# If data is a tuple like (encodings, names)
elif isinstance(data, tuple) and len(data) == 2 and isinstance(data[1], list):
    print("\n Registered Names from tuple:")
    print(data[1])

else:
    print("\n Could not find 'names'. Data structure is not recognized.")
