###############################################
# INTRODUCTION
# Welcome to the order management case study/test!
#
# During this test, we will construct a basic order manager that:
# 1) Takes in periodic (every 1 min) portfolio updates, 
# i.e. intended changes to an existing portfolio of stocks
# 2) Translates these intended changes into actual orders actions
#    that will flow downstream to our trading systems and counterparties
#
###############################################

###############################################
# INSTRUCTIONS:
# 
# YOUR OUTPUT
# You will provide us with a single python file
# called 'solution.py' that implements a solution to
# the problem below.  You may break your code into 
# whatever functions, modules, or in any manner you'd
# like, and import them however you'd like within solution.py
# but solution.py must implement a:
#      if __name__ == "__main__": 
# ... section that is runnable and will assume its input lives
# in a subdirectory named input/portfolios and has the form:
# input/portfolios/portfolio.<HH:MM>.csv - see below for explanation.
# 
# NOTE: If you provide us with more than a single file (e.g. 
# modules or testing examples, please compress your solution
# directory into a single file using a standard tool (with a 
# standard file extension we will recognize like ".ZIP"
#
# PROVIDED INPUTS
# We have provided you with a few inputs:
# 
# 1. inputs/asset_table.csv
# This CSV can be used with the AssetTable class below
# (or on your own) to map securities between their 
# integer internal IDs and their stock symbols used
# in trading on external orders.
# 
# 2. tests/inputs/portfolios/portfolio.<HH:MM>.csv
# These CSVs provide an example input with portfolio detail for 30 minute
# periods from 9:30 -> 10, 10 -> 10:30, and 10:30 -> 11.
# 
# 3. tests/outputs/order_actions/order_actions.<HH:MM>.csv
# These CSVs provide test example output for 3 30-minute periods as above.
# 
# The files from (2) and (3) are provided to you as a basic test.
# Your solution, when run on the portfolios in (2) should generate the output in (3).
# These inputs are very basic, so they do not provide much, but hopefully will give you 
# a rough guide.
#
# The row order of your files DOES NOT MATTER.   We will test them, not rely on 
# output matches.
# 
# ************** YOUR TASK *************
# Your job will be to read the portfolios provided by a user and produce
# corresponding order_actions files.
# 
# Portfolios will be provided to your solution inside the subdirectory
# of your solution.py as:
# 
# /
# solution.py
# inputs/
#    portfolios/
#      portfolio.<HH:MM>.csv
# 
# Where HH/MM correspond to the HOUR/MINUTE - e.g. the 10 AM file will be portfolio.10:00.csv.
# You can assume you will receive 1 file for every 30 minute period from 9:30 AM to 4 PM.
# The portfolio at 9:30 AM will be your "starting" portfolio.
# 
# Your task will be to produce files named "order_actions.<HH:MM>.csv" 
# inside the "outputs" subdirectory created by your solution in whatever directory
# it is run - you can assume this directory will be writeable).  In other words after running
# your solution, the subdirectory including your solution should look like:
# 
# / 
# solution.py
# inputs/
#   portfolios/
#      portfolio.09:30.csv
#      portfolio.10:00.csv
#      ...
#.     portfolio.16:00.csv
# outputs/
#   order_actions/
#      order_action.10:00.csv
#      order_action.10:30.csv
#      ...
#      order_action.16:00.csv
#
# You should feel free to provide us with some example test input and output that you used to verify
# your solution.  If you do provide that, include it in a subdirectory named "examples" or 
# mark it in some other obvious way - including a comment in your code.
#
# You are not REQUIRED to handle malformed or otherwise invalid input, but it is certainly acceptable
# and even valuable if you do.
# 
# **************************************
# 
# MORE INFORMATION
# These order_actions will be provided by your solution in CSV form corresponding
# to order actions taken at 10, 10:30, etc. every 30 minutes until 4 PM.  
# These actions can be one of the following (see the Enum OrderAction)
# NEW_ORDER - create a new order
# MODIFY_ORDER - modify an existing order
# CANCEL_ORDER - cancel an existing order (equivalent to modifying its qty to 0)
# 
# The resulting orders will represent the orders required to change the
# portfolio from T-30M to T, for example the file "orders.10:00.csv" 
# will include the orders required to move from the portfolio 
# in file "portfolio.09:30.csv" to file "portfolio.10:00.csv".
#
# These order_actions files should be created using the ExternalOrderList.to_csv
# found within our provided code.
# 
# PLEASE NOTE - VERY IMPORTANT
# Your solution must take into account the orders you create in the previous period.  
# What this means is that if in moving from the portfolio at 9:30 AM to 10 AM, you 
# create an order for 10,000 shares in stock X, the orders you create to move from
# the portfolio at 10 AM to 10:30 AM must take into account that you have open orders 
# existing from the 10 AM orders - and either cancel or modify the open order as needed. 
# YOU SHOULD NEVER HAVE MORE THAN A SINGLE OPEN ORDER AT A GIVEN TIME FOR A GIVEN STOCK.
# 
# You can assume that orders are NEVER filled.  
# 
# EXAMPLE:
# For example, if our 10 AM portfolio (not including orders) is:
# AAPL (Apple Computer): +10,000 shares
# MSFT (Microsoft): -10,000 shares
# 
# ... and our 10:30 AM portfolio (not including orders) is:
# AAPL: +30,000 shares (id=1)
# MSFT: -10,000 shares (id=2)
# 
# ... and we have the following existing "open" orders from 10:00 AM (i.e. orders.10:00.csv) (i.e. they have not yet been filled, but exist in the market place)
# AAPL: +10,000 shares
# MSFT: +10,000 shares
#

# Then the correct behavior is to:
# AAPL: Modify our existing order in AAPL from +10,000 shares to +20,000 shares
# MSFT: Cancel existing open +10,000 share order
# 
# Thus the correct file would be (order_actions.10:30.csv):
# 1,AAPL,20000,B,2    # id=1, AAPL, 20000 shares, Buy, ActionType=2 (Modify)
# 2,MSFT,0,NA,1       # id=2, MSFT, shares are ignored, NA - since cancelling, ActionType=1 (Cancel)
# 
# 
# FINAL NOTE:
# We have provided you with some boiler plate code to help you.  In no way, shape, or form are you 
# required to use this code (though we think it will be helpful, for example, to quickly load the 
# input data we've provided).  You may modify this code in whatever way you'd like, for example, 
# to provide helper functions. 
#  
# IMPORTANT: THERE MAY BE ERRORS IN THE PROVIDED CODE.  Treat it like any 3rd party code - you 
# should be slightly wary when using it.  If you do find an error, you 
# should correct the error and note what you corrected with a comment prefix - # *BUG*
# 
############################################### 

###################
# PROVIDED CODE
###################
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

import attr
from enum import (
    Enum,
    IntEnum,
)
from pathlib import Path
import pandas as pd
import glob

INVALID_IDENTIFIER = -1
ORDER_ID = 0

def make_order_id() -> int:
    global ORDER_ID
    cur = ORDER_ID
    ORDER_ID += 1
    return cur

@attr.s(auto_attribs=True)
class Asset(object):
    id: int = INVALID_IDENTIFIER
    symbol: str = ""

@attr.s(auto_attribs=True)
class AssetTable(object):
    id_sym_map: Dict[int, str]
    _sym_id_map: Dict[str, int] = attr.ib(factory=dict)

    def __attrs_post_init__(self):
        self._sym_id_map = {}
        for k,v in self.id_sym_map.items():
            self._sym_id_map[v] = k
    
    @classmethod
    def from_dict(cls, d: Dict[int, str]) -> "AssetTable":
        return AssetTable(d)
            
    @classmethod
    def from_csv(cls, csv_path: Union[str, Path]) -> "AssetTable":
        asset_table_df = pd.read_csv(csv_path, names=['id','sym'])
        id_sym_map = {}
        for ind,row in asset_table_df.iterrows():
            id_sym_map[row['id']] = row['sym']
        return cls(id_sym_map)

    def lookup(self, val: Union[str, int]) -> Optional[Union[str, int]]:
        if isinstance(val, str):
            return self._sym_id_map.get(val, None)
        return self.id_sym_map.get(val, None)

@attr.s(auto_attribs=True)
class Holding(object):
    asset: Asset 
    qty: float

    def update(self, new_qty: float) -> float:
        update_qty = new_qty - self.qty
        self.qty = new_qty
        return update_qty

@attr.s(auto_attribs=True)
class Portfolio(object):
    asset_table: AssetTable
    holdings: List[Holding]
    _hldmap: Dict[int, Holding] = attr.ib(factory=dict)
    
    def __attrs_post_init__(self):
        for hldg in self.holdings:
            self._hldmap[hldg.asset.id] = hldg

    def lookup_holding(self, asset_id: int) -> Holding:
        return self._hldmap[asset_id]
    
    @classmethod
    def from_csv(
        cls, 
        csv_path: Union[str, Path],
        asset_table: AssetTable
    ) -> "Portfolio":
        _port = pd.read_csv(csv_path, names=['id', 'qty'])
        holdings = []
        for ind, row in _port.iterrows():
            sym = asset_table.lookup(row["id"])
            asset = Asset(row["id"], sym)
            holding = Holding(asset, row["qty"])
            holdings.append(holding)
        return Portfolio(asset_table, holdings)

# USE THIS ENUM WITH ExternalOrderAction.side
# - if buying, set side to B/Buy
# - if selling, but your current quantity INCLUDING OPEN ORDERS is >= 0, set side to SL/SellLong
# - if selling, but your current quantity is < 0, set side to SS/SellShort
# - if cancelling an order, set side to NS/NoSide
class Side(Enum):
    B = "B" # Buy
    SL = "SL" # SellLong
    SS = "SS" # SellShort
    NS = "NS" # NoSide
    
class OrderAction(IntEnum):
    NewOrder = 0
    CancelOrder = 1
    ModifyOrder = 2

# YOU WILL PRODUCE THESE
# NOTE: WHEN MODIFYING OR CANCELLING AN ORDER, THE ID PROVIDED MUST MATCH THE ORIGINAL ORDER ID WHEN 
# THE ORDER WAS CREATED (i.e. OrderAction.NewOrder).
# WHEN CREATING A NEW ORDER, CREATE A NEW ID USING make_order_id ABOVE
@attr.s(auto_attribs=True)
class ExternalOrderAction(object):
    id: int
    symbol: str   # YOU MUST TRANSLATE FROM THE PORTFOLIO INTEGER ID TO SYMBOL USING ASSET_TABLE BEFORE OUTPUTTING
    qty: float
    side: Side
    action: OrderAction
    
# YOUR ORDERS WILL BE READ BY THIS
@attr.s(auto_attribs=True)
class ExternalOrderList(object):
    order_list: List[ExternalOrderAction]
    
    @classmethod
    def from_csv(cls, csv_path: Union[str, Path]) -> "ExternalOrderList":
        df = pd.read_csv(csv_path, names=["id", "symbol", "qty", "side", "action"])
        order_list = []
        for ind, row in df.iterrows():
            order_list.append(
                ExternalOrderAction(
                    row["id"], row["symbol"], row["qty"], Side(row["side"]), OrderAction(int(row["action"]))
                )
            )
        return ExternalOrderList(order_list)
        
    def to_csv(self, csv_path: Union[str, Path]) -> None:
        ids = []
        symbols = []
        qtys = []
        sides = []
        actions = []
        for order in self.order_list:
            ids.append(order.id)
            symbols.append(order.symbol)
            qtys.append(order.qty)
            sides.append(order.side.value)
            actions.append(order.action.value)
        pd.DataFrame({"symbol": symbols, "qty": qtys, "sides": sides}).to_csv(csv_path, index=False, header=True)

def next_hh_mm(inp):
    hh = int(inp[0:2])
    mm = int(inp[2:])
    c,mm = divmod(mm+30,60)
    return f"{hh+c:02}{mm:02}"

if __name__ == "__main__":
    asset_table = AssetTable.from_csv("inputs/asset_table.csv")
    # read the portfolios
    files = sorted(glob.glob("tests/inputs/portfolios/portfolio.*.csv"))
    print(files)
    holdings = [] 
    holding_map = {}
    order_id_map = {}
    portfolio = Portfolio(asset_table,holdings)
    #print(portfolio)
    for f in files:        
        external_order_list = ExternalOrderList([])
        next_portfolio = Portfolio.from_csv(f,asset_table)
        for holding in next_portfolio.holdings:
            external_order = ExternalOrderAction(None, None, None, None, None)
          
            if holding.asset.id in holding_map:
                prev_holding = holding_map[holding.asset.id]
                # print(prev_holding, holding)
                delta_qty = abs(prev_holding.qty) - abs(holding.qty)
                
                if prev_holding.qty > 0 and holding.qty > 0 :
                    external_order.qty =  holding.qty - prev_holding.qty
                    if prev_holding.qty > holding.qty:
                        external_order.side = Side.SL                        
                    elif prev_holding.qty < holding.qty:
                        external_order.side = Side.B
                            
                external_order.id = order_id_map[holding.asset.id]
                external_order.symbol = holding.asset.symbol
                if delta_qty == 0:
                    external_order.side = Side.NS
                    external_order.action = OrderAction.CancelOrder
                    external_order.qty = holding.qty                    
                    
                elif delta_qty < 0:
                    external_order.qty = delta_qty * -1
                    external_order.side = Side.B
                    external_order.action = OrderAction.ModifyOrder

                else:
                    external_order.side = Side.SL
                    external_order.action = OrderAction.CancelOrder
                    external_order.qty = holding.qty
                
            else:   
                order_id_map[holding.asset.id] = make_order_id()
                if holding.qty > 0:
                    external_order.side = Side.B
                elif holding.qty == 0:
                    external_order.side = Side.NS
                else:
                    external_order.side = Side.SS
                external_order.action = OrderAction.NewOrder
                external_order.qty = holding.qty
                external_order.symbol = holding.asset.symbol                
                external_order.id = order_id_map[holding.asset.id] 
                portfolio.holdings.append(holding)
                holding_map[holding.asset.id] = holding
           
            external_order_list.order_list.append(external_order)
        
        external_order_list.to_csv("test.csv")
        print(external_order_list.order_list)

        # for new holdings create long order
