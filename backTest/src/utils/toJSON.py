import sys, json

# from backTest import run


#Read data from stdin
def read_input():
    input= sys.stdin.readlines()
    jsonString = ""
    for line in input:
       jsonString += line
    #Delete empty space at the end of the string
    jsonString = jsonString[:-1]
    return json.loads(jsonString)

def main():

    
    test = read_input()

    # Run the backtest with provided parameters and

    #Example backtest data structure
    bt = {
        "id": "test",
        "name": "test",
        "start": "2017-01-01",
        "end": "2017-01-01",
        "strategy": "test",
        "strategy_params": {
            "test": "test"
        },
        "data": {
            "test": "test"
        },
        "backtest": {
            "test": "test"
        },
        "results": {
            "test": "test"
        },
        "data": test
    }

    print(json.dumps(bt))

    #write into a test.txt file
    with open('test.txt', 'w') as outfile:
        outfile.write(json.dumps(bt))

# Start process
if __name__ == '__main__':
    main()