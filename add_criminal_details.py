"""
Add detailed criminal information to database
"""
from database import update_criminal

criminals_info = {
    "Dawood ibrahim": {
        "aliases": ["Dawood Ibrahim Kaskar", "D-Company Boss"],
        "crime": "Organized Crime, Terrorism, Murder",
        "crime_details": "Mastermind of 1993 Mumbai bombings, drug trafficking, extortion, murder. Leader of D-Company organized crime syndicate.",
        "years_in_prison": "Never captured",
        "status": "Most Wanted - Fugitive",
        "nationality": "Indian",
        "location": "Karachi, Pakistan (suspected)",
        "description": "India's most wanted criminal. Designated global terrorist by India and USA. Reward of ₹25 crore for information."
    },
    "Lawrence bishnoi": {
        "aliases": ["Lawrence Bishnoi Gang Leader"],
        "crime": "Murder, Extortion, Organized Crime",
        "crime_details": "Leader of Bishnoi gang involved in multiple murders including Sidhu Moose Wala. Extortion, contract killings, organized crime across North India.",
        "years_in_prison": "Currently imprisoned since 2014",
        "status": "Imprisoned - High Security",
        "nationality": "Indian",
        "location": "Tihar Jail, Delhi",
        "description": "Notorious gangster operating from jail. Involved in 700+ criminal cases across multiple states."
    },
    "osama bin laden": {
        "aliases": ["Osama bin Mohammed bin Awad bin Laden", "OBL"],
        "crime": "Terrorism, Mass Murder",
        "crime_details": "Founder of al-Qaeda. Mastermind of September 11, 2001 attacks killing 2,977 people. Multiple terrorist attacks worldwide.",
        "years_in_prison": "Never imprisoned",
        "status": "Deceased (Killed 2011)",
        "nationality": "Saudi Arabian",
        "location": "Killed in Abbottabad, Pakistan",
        "description": "World's most wanted terrorist until death. Responsible for thousands of deaths in terrorist attacks globally."
    },
    "vijay mallya": {
        "aliases": ["King of Good Times", "Liquor Baron"],
        "crime": "Financial Fraud, Money Laundering",
        "crime_details": "Defaulted on loans worth ₹9,000 crore from Indian banks. Money laundering, financial irregularities in Kingfisher Airlines.",
        "years_in_prison": "Extradition pending",
        "status": "Fugitive in UK",
        "nationality": "Indian",
        "location": "London, United Kingdom",
        "description": "Former billionaire businessman. Fled India in 2016. Fighting extradition from UK since 2017."
    }
}

def add_criminal_details():
    """Add detailed information for all criminals"""
    print("Adding detailed criminal information...\n")
    
    for name, info in criminals_info.items():
        try:
            update_criminal(name, info)
            print(f"Updated: {name}")
        except Exception as e:
            print(f"Error updating {name}: {e}")
    
    print("\nAll criminal details added successfully!")

if __name__ == "__main__":
    add_criminal_details()
