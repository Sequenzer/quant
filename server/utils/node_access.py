import sys, json
import pandas as pd
import sys,os
sys.path.append(os.path.realpath('..'))

# from run_module import run

from pathlib import Path





from backTest.src.strategies.aligartor_indicator import AligatorIndicator
from backTest.src.run_module import run

# print("Directory Path:", Path().absolute())


#Read data from stdin
def read_input():
    input= sys.stdin.readlines()
    jsonString = ""
    for line in input:
       jsonString += line
    #Delete empty space at the end of the string
    jsonString = jsonString[:-1]
    return json.loads(jsonString)

def list_to_df(data_list):
    df = pd.DataFrame(data_list)
    df = df.drop(['_id','stock','__v'], axis=1)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume' ,"adjclose"]
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    df.index = pd.to_datetime(df.index)
    return df


def main():

    
    input =  sys.stdin.readlines()
    data = list_to_df(input)
    # bt_trades= run(data=data)
    
    print(json.dumps((data.head().to_json())))


    #bt_trades= run(data=)

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
        "data": input
    }

    # print(json.dumps(bt))

    # print(json.dumps(data.head().to_json()))

    #write into a test.txt file
    # with open('df.txt', 'w') as outfile:
    #      outfile.write()

# Start process
if __name__ == '__main__':
    main()