from pycoingecko import CoinGeckoAPI
from langchain.tools import Tool
from typing import Optional, Dict, Any
import time

class CoinGeckoTools:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        # Map of common names to CoinGecko IDs
        self.coin_map = {
            'bitcoin': 'bitcoin',
            'btc': 'bitcoin',
            'ethereum': 'ethereum',
            'eth': 'ethereum',
            'polygon': 'matic-network',
            'matic': 'matic-network',
            'solana': 'solana',
            'sol': 'solana',
            'cardano': 'cardano',
            'ada': 'cardano'
        }

    def get_tools(self):
        return [
            Tool(
                name="get_trending_coins",
                func=self.get_trending_coins,
                description="Get current trending cryptocurrencies"
            ),
            Tool(
                name="get_coin_price",
                func=self.get_coin_price,
                description="Get price for a specific cryptocurrency"
            )
        ]

    def get_coin_id(self, query: str) -> str:
        """Convert common names to CoinGecko IDs"""
        query = query.lower().strip()
        return self.coin_map.get(query, query)

    def get_trending_coins(self) -> str:
        try:
            # Add retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    trending = self.cg.get_search_trending()
                    coins = trending.get('coins', [])
                    if not coins:
                        return "No trending coins found at the moment."
                    
                    response = "🔥 Trending cryptocurrencies:\n\n"
                    for coin in coins:
                        item = coin['item']
                        response += f"• {item['name']} ({item['symbol'].upper()})"
                        if item.get('market_cap_rank'):
                            response += f" - Rank #{item['market_cap_rank']}"
                        response += "\n"
                    return response
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(1)  # Wait before retrying
            
        except Exception as e:
            print(f"Error in get_trending_coins: {str(e)}")
            return "Sorry, I couldn't fetch trending coins at the moment. Try asking for a specific coin's price instead."

    def get_coin_price(self, coin_id: str) -> str:
        try:
            # Convert common names to CoinGecko IDs
            coin_id = self.get_coin_id(coin_id)
            
            data = self.cg.get_price(
                ids=coin_id, 
                vs_currencies='usd',
                include_24hr_change=True
            )
            
            if coin_id in data:
                price = data[coin_id]['usd']
                change_24h = data[coin_id].get('usd_24h_change', 0)
                
                response = f"💰 {coin_id.title()} price: ${price:,.2f} USD"
                if change_24h:
                    change_symbol = "📈" if change_24h > 0 else "📉"
                    response += f"\n{change_symbol} 24h change: {change_24h:.2f}%"
                return response
            
            return f"Could not find price for {coin_id}. Please check the coin name and try again."
            
        except Exception as e:
            print(f"Error in get_coin_price: {str(e)}")
            return f"Sorry, I couldn't fetch the price for {coin_id}. Please check the coin name and try again."

def coingecko():
    return CoinGeckoTools()