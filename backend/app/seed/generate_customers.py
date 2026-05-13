from faker import Faker

fake = Faker()

INDUSTRIES = [
    "Retail",
    "Healthcare",
    "Manufacturing",
    "Technology",
    "Logistics",
    "Finance",
    "Education",
    "Hospitality",
]

COUNTRIES_AND_CITIES = {
    "Qatar": ["Doha", "Al Wakrah", "Al Rayyan", "Lusail"],
    "UAE": ["Dubai", "Abu Dhabi", "Sharjah"],
    "Saudi Arabia": ["Riyadh", "Jeddah", "Dammam"],
    "Oman": ["Muscat", "Salalah"],
    "Kuwait": ["Kuwait City", "Hawalli"],
    "Bahrain": ["Manama", "Riffa"],
}

CUSTOMER_TIERS = ["Standard", "Premium", "Enterprise"]
ACCOUNT_STATUSES = ["Active", "Active", "Active", "At Risk", "Inactive"]


def generate_customers(count: int = 100) -> list[dict]:
    customers = []

    country_names = list(COUNTRIES_AND_CITIES.keys())

    for i in range(1, count + 1):
        country = fake.random_element(country_names)
        city = fake.random_element(COUNTRIES_AND_CITIES[country])

        customer = {
            "customer_code": f"CUST-{i:04d}",
            "customer_name": fake.company(),
            "industry": fake.random_element(INDUSTRIES),
            "country": country,
            "city": city,
            "customer_tier": fake.random_element(CUSTOMER_TIERS),
            "account_status": fake.random_element(ACCOUNT_STATUSES),
        }

        customers.append(customer)

    return customers