import json


def parse_json():
    json_string = '{"name": "Rustem", "age": 18, "city": "Almaty"}'
    
    data = json.loads(json_string)
    
    print("Parsed JSON:")
    print(data)
    print("Name:", data["name"])
    print("Age:", data["age"])


#
def convert_to_json():
    python_dict = {
        "name": "Rustem",
        "age": 18,
        "is_student": True,
        "skills": ["Python", "SQL"]
    }
    
    json_data = json.dumps(python_dict, indent=4)
    
    print("\nConverted to JSON:")
    print(json_data)



def write_json_file():
    data = {
        "name": "Rustem",
        "age": 18,
        "city": "Almaty"
    }
    
    with open("output.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print("\nJSON written to output.json")



def read_json_file():
    try:
        with open("output.json", "r") as file:
            data = json.load(file)
        
        print("\nRead from file:")
        print(data)
    
    except FileNotFoundError:
        print("\nFile not found. Run write_json_file() first.")



def work_with_sample():
    try:
        with open("sample-data.json", "r") as file:
            data = json.load(file)
        
        print("\nSample Data:")
        
        
        if isinstance(data, list):
            for item in data:
                print(item)
        elif isinstance(data, dict):
            for key, value in data.items():
                print(key, ":", value)
    
    except FileNotFoundError:
        print("\nsample-data.json not found.")



if __name__ == "__main__":
    parse_json()
    convert_to_json()
    write_json_file()
    read_json_file()
    work_with_sample()