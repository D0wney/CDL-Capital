#!/usr/bin/python
import cgi, datetime,sys,LINK_HEADERS
import simplejson as json
from decimal import *
sys.path.insert(0, str(LINK_HEADERS.MODELS_LINK))
from users_class import Users
from transactions_class import Transactions
from owned_stocks_class import Owned_stocks
from company_class import Company

print "Content-Type: text/html\r\n\r\n"

#Get form data
form = cgi.FieldStorage()
if form.getvalue("username") != None:
    username = form.getvalue("username")
if form.getvalue("volume") != None:
    volume = int(form.getvalue("volume"))
if form.getvalue("company") != None:
    company = form.getvalue("company")
if form.getvalue("trans_type") != None:
    trans_type = form.getvalue("trans_type")
        
#test variables
#username="al356"
#company='tsla'
#volume=10
#trans_type='buy'
#trans_type='sell'

#Declare globals objects
u = Users()
u.populate(username)

o = Owned_stocks()
o.populate(username, company)

c=Company()
c.populate(company)

#Declare global variables
time = datetime.datetime.utcnow()
def calculate_price():
    ask_price = c.get_ask()
    final_price = Decimal(ask_price) * int(volume)
    return ask_price, final_price

def update_transactions(ask_price, final_price):
    t = Transactions()
    t.upload(username,time,trans_type,company,ask_price,volume,final_price)
    t.insert()

def calculate_portfolio(final_price):
    if trans_type == "buy":
        u.set_available_funds(Decimal(u.get_available_funds()) - Decimal(final_price))
        u.set_total_stock_values(Decimal(u.get_total_stock_values()) + Decimal(final_price))
    elif trans_type == "sell":
        u.set_available_funds(Decimal(u.get_available_funds()) + Decimal(final_price))
        u.set_total_stock_values(Decimal(u.get_total_stock_values()) - Decimal(final_price))
    u.set_total_portfolio(u.get_total_stock_values() + u.get_available_funds())

def update_owned_stocks(ask_price, final_price):
    if trans_type == "buy":
        if o.get_stock() != None:
            o.set_current_shares(o.get_current_shares() + volume)
            o.set_current_price(ask_price)
            o.set_total_worth(Decimal(o.get_current_shares()) * Decimal(o.get_current_price()))
        else:
            o.insert(company, volume, ask_price, final_price, username)
    elif trans_type == "sell":
        if o.get_current_shares() >= volume:
            o.set_current_shares(o.get_current_shares() - volume)
            o.set_current_price(ask_price)
            o.set_total_worth(Decimal(o.get_current_shares()) * Decimal(o.get_current_price()))
        #elif o.get_current_shares() == volume:
            #o.delete(company, username)
            
def main():
    ask_price, final_price = calculate_price()
    if trans_type == 'buy':  
        if final_price <= u.get_available_funds():
            update_transactions(ask_price, final_price)
            calculate_portfolio(final_price)
            update_owned_stocks(ask_price, final_price)
    elif trans_type == 'sell':
        if o.get_current_shares() >= volume:
	    update_transactions(ask_price, final_price)
            calculate_portfolio(final_price)
            update_owned_stocks(ask_price, final_price)
main()    
