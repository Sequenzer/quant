## Order

^60f7ab

Type: class/object
Input:
- broker: The [[Broker]] object
- size: size of the Order
- type: type of the Order
##### Methods
- cancel: removes itself from the brokers order list

***
## Trade

^92b42a

Type: class/object
Input:
- broker: The [[Broker]] object
- size: size of the Trade
- price: The price of the Trade
- type: type of the Order
##### Methods
- cancel: places a reverse order at the [[Broker]] to be executed at the next Period

***

## Position

Type: class/object
Input:
- broker: The [[Broker]] object

##### Methods
- cancel: cancels all current active Trades