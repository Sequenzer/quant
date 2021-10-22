# Backtest

Type: class/object
Input:
- data: underlying Dataset in  [[Definitions#^1e3180| OHLC]]  Format.
- broker: a [[Broker]] object
- strategy: a [[Strategy]] object


### Idea

The Backtest Object Manages the walk threw the dataset and calls the [[Broker]]to process the !!orders at the beginning of a Period and the [[Strategy]] after to get new orders for the next period.

### Methods

init: Initialises the object
run: runs the [[Strategy]] over the Data





