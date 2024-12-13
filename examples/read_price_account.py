import asyncio
from pythclient.pythclient import PythClient
from pythclient.utils import get_key

async def get_price_accounts():
    # Specify the Pythtest Oracle Program address
    program_key = "gSbePebfvPy7tRqimPoVecS2UsBvYv46ynrzWocc92s"
    
    # Use devnet configuration (adjust if needed)
    solana_network = "devnet"
    
    async with PythClient(
        first_mapping_account_key=get_key(solana_network, "mapping"),
        program_key=program_key
    ) as client:
        # Refresh all prices to ensure latest data
        await client.refresh_all_prices()
        
        # Get all products
        products = await client.get_products()
        
        # Extract price accounts
        price_accounts = []
        for product in products:
            prices = await product.get_prices()
            for price_type, price_info in prices.items():
                price_accounts.append({
                    'symbol': product.attrs.get('symbol'),
                    'price_account': price_info.key,
                    'price': price_info.aggregate_price,
                    'status': price_info.aggregate_price_status
                })
        
        return price_accounts

async def main():
    try:
        price_accounts = await get_price_accounts()
        print("Price Accounts:")
        for account in price_accounts:
            print(account)
    except Exception as e:
        print(f"Error retrieving price accounts: {e}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())