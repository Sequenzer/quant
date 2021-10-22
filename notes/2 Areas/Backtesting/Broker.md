# Broker

Type: class/object
Input:
- data: underlying Dataset in  [[Definitions#^1e3180| OHLC]]  Format.
- ordersr: a List of [[Minor Classes#^60f7ab|Orders]]
- trades: a List of [[Minor Classes#^92b42a|Trades]]
- cash: current cash value


### Idea

The Brokers accepts new [[Minor Classes#^60f7ab|Orders]] and proccessed them into [[Minor Classes#^92b42a|Trades]].

### Methods

init: Initialises the object
next: runs everything it has to do in the current Period
new_order: accepts a new order of specific type and size
process_order: processes all orders by opening new trades of the same size
open_trade: opens a new active Trade
close_trade: closes an active Trade into a closed one