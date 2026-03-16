class MarketAgent:
    def estimate_market_value(self, carbon_credits):
        price_per_credit_usd = 10
        total_value = round(carbon_credits * price_per_credit_usd, 2)

        if carbon_credits >= 50:
            buyer_type = "Large enterprise buyer"
        elif carbon_credits >= 10:
            buyer_type = "Mid-size ESG buyer"
        else:
            buyer_type = "Small offset buyer"

        return {
            "price_per_credit_usd": price_per_credit_usd,
            "total_value_usd": total_value,
            "buyer_type": buyer_type,
            "market_status": "Ready for listing"
        }