import json
from airtable import Airtable


def main():

    base_key = get_input("Please enter the key for the base. (This can be found by going to https://airtable.com/api"
                         ", selecting the base you want to convert to JSON and copying the bit in the url "
                         "that looks like 'app' followed by some letters and numbers.): ")

    table_name = get_input("Now please enter the name of the table within that base which you want to convert to"
                           " JSON: ")

    key = read_api_key()

    if key == "0" or key == "1":
        if key == "0":
            print("No API Key in api_key.txt")
        elif key == "1":
            print("api_key.txt Doesn't exist and shall be created.")
        new_api_key = get_input("Please Enter your API Key: ")
        with open('api_key.txt', 'w') as keyfile:
            keyfile.write(new_api_key)
        key = new_api_key
        # print("\n")
    try:
        at = Airtable(base_key, table_name, api_key=key)
    except ValueError as e:
        print(e)
        print("Make sure no typos were made and that the API key is correct and hen try again.")
        return

    data = at.get_all()

    result = {}
    i = -1

    for single_data in data:
        i += 1

        sorting_dict = {}
        sorting_dict["id"] = single_data["id"]

        for key, value in sorted(data[i]["fields"].items()):
            sorting_dict[key] = value

        result[data[i]["fields"]["name"]] = sorting_dict

    # print(result)
    with open('{}.json'.format(table_name), 'w') as outfile:
        json.dump(result, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def read_api_key():
    """
    Read API key from file or return 0
    """
    try:
        with open('api_key.txt', 'r') as keyfile:
            key = keyfile.readline()
            if key == "" or key == " ":
                return "0"
            return key
    except Exception:
        return "1"


def get_input(question):
    """
    Ask the user question until they give an answer.
    """
    has_answer = False
    while not has_answer:
        print("\n\n{}".format(question))
        reply = input()
        if reply == "" or reply == " ":
            print("Reply is empty")
        else:
            has_answer = True
            return reply

    return "ERROR"  # Should never get to this code

main()
print("\nEnd of Script")
