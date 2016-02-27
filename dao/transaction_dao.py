#!/usr/bin/python

import sys, LINK_HEADERS
from decimal import *
sys.path.insert(0, str(LINK_HEADERS.DATABASE_LINK))
sys.path.insert(0, str(LINK_HEADERS.MODELS_LINK))
from database_class import DB
from transaction_model import Transaction
from owned_stock_model import Owned_stock
from user_stock_value_model import User_stock_value

class Transaction_dao:

     db = None

     def __init__(self):
         self.db = DB(LINK_HEADERS.DB_HOST, LINK_HEADERS.DB_USER, LINK_HEADERS.DB_PASSWORD, LINK_HEADERS.DB_NAME)                     
     def select_all(self, user):
          result = self.db.query("select * from transactions where user=('%s')"%(user)+";")
          if result:
               l = []
               for i in range(len(result)):
                    t = Transactions(result[i]['user'],result[i]['trans_date'],result[i]['stock'],result[i]['price'],result[i]['sold'],result[i]['order_id'],result[i]['profit'])
                    l.append(t)
               l.sort(key=lambda x: x.get_trans_date(), reverse=False)
               return l

     def select_all_active(self, user):
          result = self.db.query("select * from transactions where user=('%s') and sold='0'"%(user)+";")
          if result:
               l = []
               for i in range(len(result)):
                    t = Transactions(result[i]['user'],result[i]['trans_date'],result[i]['stock'],result[i]['price'],result[i]['sold'],result[i]['order_id'],result[i]['profit'])
                    l.append(t)
               l.sort(key=lambda x: x.get_trans_date(), reverse=False)
               return l

     def select_all_sold(self, user):
          result = self.db.query("select * from transactions where user=('%s') and sold='1'"%(user)+";")
          if result:
               l = []
               for i in range(len(result)):
                    t = Transactions(result[i]['user'],result[i]['trans_date'],result[i]['stock'],result[i]['price'],result[i]['sold'],result[i]['order_id'],result[i]['profit'])
                    l.append(t)
               l.sort(key=lambda x: x.get_trans_date(), reverse=False)
               return l

     def buy(self,user, trans_date, stock, volume, price):
          for i in range(volume):
               self.db.query("insert into transactions values ('%s','%s','%s',%f,'%s',%d,%f)"%(user, trans_date, stock, Decimal(price), 0, int(i), Decimal(0))+";")

     def sell(self, user, stock, volume, price):
          result = self.db.query("select * from transactions where user=('%s') and stock=('%s') and sold='0'"%(user, stock)+" ORDER BY trans_date ASC, order_id ASC LIMIT "+str(volume)+";")

          if result:
               if len(result) >= volume:
                    for i in range(len(result)):
                         profit = Decimal(price) - Decimal(result[i]['price'])
                         self.db.query("update transactions set sold='1', profit=('%s') where user=('%s') and stock=('%s') and trans_date=('%s') and order_id=(%d)"%(Decimal(profit), user, stock, result[i]['trans_date'], result[i]['order_id'])+";")

     def get_user_stock_list(self, user):
          result = self.db.query("select distinct stock from transactions where user=('%s')"%(user)+";")
          l=[]
          for i in range(len(result)):
              l.append(result[i]['stock'])
          return l
          
     def get_owned_stock_model(self, user, stock, price):
          volume_result= self.db.query("select count(*) from transactions where user=('%s') and stock=('%s') and sold='0'"%(user, stock)+";")
          volume = int(volume_result[0]['count(*)'])
          total_worth = volume * price
          profit_result = self.db.query("select sum(profit) from transactions where user=('%s') and stock=('%s')"%(user, stock)+";")
          profit = Decimal(profit_result[0]['sum(profit)'])
          o = Owned_stock(stock, volume, price, total_worth, profit)
          return o

     def get_user_stock_value_model(self, user):
          result1 = self.db.query("select sum(profit) from transactions where user=('%s')"%(user)+";")
          result2 = self.db.query("select sum(price) from transactions where user=('%s') and sold='0'"%(user)+";")
          profit = Decimal(result1[0]['sum(profit)'])
          total_stock_values = Decimal(result1[0]['sum(profit)']) + Decimal(result2[0]['sum(price)'])
          u = User_stock_value(user, profit, total_stock_values)
          return u