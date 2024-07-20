from trading_levelbook import Book
from trading_frame import TimeFrame, CountFrame, Tick, Trade, Candle

class MarketView:
    """
    MarketView is a view build with any source of trading data like Trade, Tick, Candle and Orders.
    It use the trading frame package to build the frames. It will use the trading levelbook package
    to build the orderbook.
    """
    def __init__(self, name: str):
        self.name       = name   # Give this market pair a name
        self.tape       = []     # Build the tape
        self.tape_limit = 1000   # Max trade in tape
        self.orderbook  = Book() # Build the orderbook
        self.frames     = {}     # Build frames (Timeframes, Countframe, etc.)

    def add_frame(self, periods_length: str | int, max_periods: int, frame_type: str = 'time', date_format: str = '%Y-%m-%dT%H:%M:%S.%fZ') -> None:
        if frame_type == 'time':
            self.frames[periods_length] = TimeFrame(periods_length, max_periods, date_format)

    def feed_frames(self, new_tape_entry: Trade | Tick) -> None:
        for frame in self.frames:
            self.frames[frame].feed(new_tape_entry)

    def feed_tape(self, new_tape_entry: Trade | Tick) -> None:
        self.tape.append(new_tape_entry)

        if len(self.tape) > self.tape_limit:
            self.tape.pop(0)

    def feed_candle(self, candle: Candle) -> None:
        for frame in self.frames:
            self.frames[frame].feed(candle)

    def feed(self, data, type: str = 'trade') -> None:
        if type == 'trade':
            new_entry = Trade(data[0], data[1], data[2], data[3])
        elif type == 'tick':
            new_entry = Tick(data[0], data[1], data[2], data[3], data[4])
        elif type == 'candle':
            new_entry = Candle(data[0], data[1], data[2], data[3], data[4], data[5])
        else:
            raise Exception('Bad tape feeding type')

        if type == 'trade' or type == 'tick':
            self.feed_tape(new_entry)
            self.feed_frames(new_entry)
        elif type == 'candle':
            self.feed_candle(new_entry)

    def feed_order(self, orders) -> None:
        # TODO
        pass
