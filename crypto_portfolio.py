#!/usr/bin/env python3
"""
Crypto Portfolio Tracker
Track your crypto holdings with real-time prices
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import requests

class CryptoPortfolio:
    def __init__(self, filename='portfolio.json'):
        self.filename = filename
        self.portfolio = self.load_portfolio()
        self.api_base = 'https://api.coingecko.com/api/v3'
    
    def load_portfolio(self) -> Dict:
        """Load portfolio from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {'holdings': [], 'transactions': []}
    
    def save_portfolio(self):
        """Save portfolio to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.portfolio, f, indent=2)
    
    def get_price(self, coin_id: str) -> Dict:
        """Fetch current price from CoinGecko"""
        try:
            url = f"{self.api_base}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get(coin_id, {})
        except Exception as e:
            print(f"❌ Error fetching price for {coin_id}: {e}")
            return {}
    
    def search_coin(self, query: str) -> List[Dict]:
        """Search for a coin by name or symbol"""
        try:
            url = f"{self.api_base}/search"
            params = {'query': query}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('coins', [])[:5]
        except Exception as e:
            print(f"❌ Error searching: {e}")
            return []
    
    def add_holding(self, coin_id: str, coin_name: str, symbol: str, 
                    amount: float, buy_price: float):
        """Add a new holding to portfolio"""
        holding = {
            'coin_id': coin_id,
            'coin_name': coin_name,
            'symbol': symbol.upper(),
            'amount': amount,
            'buy_price': buy_price,
            'date_added': datetime.now().isoformat()
        }
        self.portfolio['holdings'].append(holding)
        
        # Record transaction
        transaction = {
            'type': 'buy',
            'coin_id': coin_id,
            'amount': amount,
            'price': buy_price,
            'date': datetime.now().isoformat()
        }
        self.portfolio['transactions'].append(transaction)
        
        self.save_portfolio()
        print(f"✅ Added {amount} {symbol.upper()} at ${buy_price}")
    
    def remove_holding(self, index: int):
        """Remove a holding from portfolio"""
        if 0 <= index < len(self.portfolio['holdings']):
            removed = self.portfolio['holdings'].pop(index)
            self.save_portfolio()
            print(f"✅ Removed {removed['symbol']}")
        else:
            print("❌ Invalid index")
    
    def calculate_portfolio_value(self) -> Dict:
        """Calculate total portfolio value and stats"""
        total_value = 0
        total_invested = 0
        holdings_data = []
        
        for holding in self.portfolio['holdings']:
            price_data = self.get_price(holding['coin_id'])
            
            if not price_data:
                continue
            
            current_price = price_data.get('usd', 0)
            change_24h = price_data.get('usd_24h_change', 0)
            
            current_value = holding['amount'] * current_price
            invested = holding['amount'] * holding['buy_price']
            profit_loss = current_value - invested
            profit_loss_pct = (profit_loss / invested * 100) if invested > 0 else 0
            
            total_value += current_value
            total_invested += invested
            
            holdings_data.append({
                'symbol': holding['symbol'],
                'coin_name': holding['coin_name'],
                'amount': holding['amount'],
                'buy_price': holding['buy_price'],
                'current_price': current_price,
                'current_value': current_value,
                'invested': invested,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'change_24h': change_24h
            })
        
        total_profit_loss = total_value - total_invested
        total_profit_loss_pct = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        return {
            'total_value': total_value,
            'total_invested': total_invested,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_pct': total_profit_loss_pct,
            'holdings': holdings_data
        }
    
    def display_portfolio(self):
        """Display portfolio in a formatted table"""
        if not self.portfolio['holdings']:
            print("\n📊 Your portfolio is empty. Add some holdings to get started!\n")
            return
        
        print("\n" + "="*100)
        print("💼 CRYPTO PORTFOLIO TRACKER")
        print("="*100)
        
        stats = self.calculate_portfolio_value()
        
        # Display individual holdings
        print(f"\n{'#':<3} {'Symbol':<8} {'Amount':<15} {'Buy Price':<12} {'Current':<12} {'Value':<12} {'P/L':<15} {'24h':<10}")
        print("-"*100)
        
        for i, holding in enumerate(stats['holdings'], 1):
            pl_color = '🟢' if holding['profit_loss'] >= 0 else '🔴'
            change_color = '📈' if holding['change_24h'] >= 0 else '📉'
            
            print(f"{i:<3} {holding['symbol']:<8} {holding['amount']:<15.4f} "
                  f"${holding['buy_price']:<11.2f} ${holding['current_price']:<11.2f} "
                  f"${holding['current_value']:<11.2f} "
                  f"{pl_color} ${holding['profit_loss']:>7.2f} ({holding['profit_loss_pct']:>6.2f}%) "
                  f"{change_color} {holding['change_24h']:>6.2f}%")
        
        # Display totals
        print("-"*100)
        total_color = '🟢' if stats['total_profit_loss'] >= 0 else '🔴'
        print(f"\n{'TOTAL PORTFOLIO VALUE:':<40} ${stats['total_value']:,.2f}")
        print(f"{'Total Invested:':<40} ${stats['total_invested']:,.2f}")
        print(f"{'Total Profit/Loss:':<40} {total_color} ${stats['total_profit_loss']:,.2f} ({stats['total_profit_loss_pct']:.2f}%)")
        print("="*100 + "\n")

def main():
    tracker = CryptoPortfolio()
    
    while True:
        print("\n🔷 Crypto Portfolio Tracker")
        print("1. View Portfolio")
        print("2. Add Holding")
        print("3. Remove Holding")
        print("4. Search Coin")
        print("5. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            tracker.display_portfolio()
        
        elif choice == '2':
            query = input("Enter coin name or symbol: ").strip()
            results = tracker.search_coin(query)
            
            if not results:
                print("❌ No coins found")
                continue
            
            print("\nSearch Results:")
            for i, coin in enumerate(results, 1):
                print(f"{i}. {coin['name']} ({coin['symbol'].upper()}) - ID: {coin['id']}")
            
            try:
                coin_idx = int(input("\nSelect coin (number): ")) - 1
                if 0 <= coin_idx < len(results):
                    selected = results[coin_idx]
                    amount = float(input("Enter amount: "))
                    buy_price = float(input("Enter buy price (USD): "))
                    
                    tracker.add_holding(
                        selected['id'],
                        selected['name'],
                        selected['symbol'],
                        amount,
                        buy_price
                    )
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == '3':
            tracker.display_portfolio()
            try:
                index = int(input("Enter holding number to remove: ")) - 1
                tracker.remove_holding(index)
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == '4':
            query = input("Search for coin: ").strip()
            results = tracker.search_coin(query)
            
            if results:
                print("\nSearch Results:")
                for coin in results:
                    print(f"• {coin['name']} ({coin['symbol'].upper()}) - ID: {coin['id']}")
            else:
                print("❌ No results found")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == '__main__':
    main()
