"""
Seed Criminal Data with Historical Information
"""
from database import update_criminal, get_criminal_by_name

CRIMINAL_DATA = {
    "Abu Salem": {
        "aliases": ["Abu", "Salem"],
        "crime": "Murder, Extortion, Arms Trafficking",
        "crime_details": "Involved in 1993 Mumbai bombings, multiple murder cases, extortion rackets",
        "years_in_prison": "Life imprisonment",
        "status": "Imprisoned",
        "nationality": "Indian",
        "location": "Taloja Central Jail, Mumbai",
        "description": "Notorious gangster and terrorist, part of D-Company"
    },
    "Chhota Rajan": {
        "aliases": ["Rajendra Nikhalje", "Rajan"],
        "crime": "Murder, Extortion, Organized Crime",
        "crime_details": "Leader of organized crime syndicate, multiple murder cases, rival of Dawood Ibrahim",
        "years_in_prison": "Life imprisonment",
        "status": "Imprisoned",
        "nationality": "Indian",
        "location": "Tihar Jail, Delhi",
        "description": "Former associate turned rival of Dawood Ibrahim"
    },
    "Dawood Ibrahim": {
        "aliases": ["D-Company", "Dawood Bhai"],
        "crime": "Terrorism, Murder, Drug Trafficking",
        "crime_details": "Mastermind of 1993 Mumbai bombings, international drug trafficking, organized crime",
        "years_in_prison": "Fugitive",
        "status": "Alive (Fugitive)",
        "nationality": "Indian",
        "location": "Karachi, Pakistan (Suspected)",
        "description": "India's most wanted criminal, heads D-Company"
    },
    "Haji Mastan": {
        "aliases": ["Mastan Mirza", "Bawa"],
        "crime": "Smuggling, Organized Crime",
        "crime_details": "Gold smuggling kingpin in 1960s-70s Mumbai",
        "years_in_prison": "Served time, later reformed",
        "status": "Dead",
        "nationality": "Indian",
        "location": "Mumbai (Deceased 1994)",
        "description": "Former smuggling don who later entered politics"
    },
    "Harshad Mehta": {
        "aliases": ["Big Bull", "Amitabh Bachchan of Stock Market"],
        "crime": "Securities Fraud, Banking Scam",
        "crime_details": "1992 securities scam worth Rs 5000 crore, manipulated stock market",
        "years_in_prison": "Died during trial",
        "status": "Dead",
        "nationality": "Indian",
        "location": "Mumbai (Deceased 2001)",
        "description": "Stockbroker involved in India's biggest securities scam"
    },
    "Lawrence Bishnoi": {
        "aliases": ["Lawrence", "Bishnoi"],
        "crime": "Murder, Extortion, Organized Crime",
        "crime_details": "Gang leader involved in multiple murders, extortion, and organized crime activities",
        "years_in_prison": "Imprisoned since 2014",
        "status": "Imprisoned",
        "nationality": "Indian",
        "location": "Tihar Jail, Delhi",
        "description": "Gangster with operations across North India"
    },
    "Muthappa": {
        "aliases": ["Muthappa Rai"],
        "crime": "Extortion, Organized Crime",
        "crime_details": "Underworld don in Bangalore, involved in extortion and real estate crimes",
        "years_in_prison": "Served time",
        "status": "Dead",
        "nationality": "Indian",
        "location": "Bangalore (Deceased 2020)",
        "description": "Former underworld don of Bangalore"
    },
    "Osama": {
        "aliases": ["Osama Bin Laden", "OBL"],
        "crime": "Terrorism, Mass Murder",
        "crime_details": "Founder of Al-Qaeda, mastermind of 9/11 attacks and multiple terrorist attacks worldwide",
        "years_in_prison": "Never imprisoned",
        "status": "Dead (Killed 2011)",
        "nationality": "Saudi Arabian",
        "location": "Abbottabad, Pakistan (Killed)",
        "description": "Terrorist leader responsible for thousands of deaths"
    },
    "Rehman Dakait": {
        "aliases": ["Rehman", "Dakait"],
        "crime": "Dacoity, Murder, Kidnapping",
        "crime_details": "Notorious dacoit operating in rural areas, multiple cases of robbery and murder",
        "years_in_prison": "Unknown",
        "status": "Unknown",
        "nationality": "Indian",
        "location": "Unknown",
        "description": "Dacoit with criminal activities in rural regions"
    },
    "Veerappan": {
        "aliases": ["Koose Muniswamy Veerappan", "Jungle King"],
        "crime": "Poaching, Kidnapping, Murder",
        "crime_details": "Sandalwood smuggler and ivory poacher, killed over 120 people, kidnapped multiple high-profile individuals",
        "years_in_prison": "Never imprisoned",
        "status": "Dead (Killed 2004)",
        "nationality": "Indian",
        "location": "Tamil Nadu-Karnataka border (Killed)",
        "description": "Notorious bandit and poacher who evaded capture for decades"
    },
    "Vijay Mallya": {
        "aliases": ["King of Good Times"],
        "crime": "Financial Fraud, Money Laundering",
        "crime_details": "Defaulted on loans worth Rs 9000 crore, fled India to avoid prosecution",
        "years_in_prison": "Fugitive",
        "status": "Alive (Fugitive)",
        "nationality": "Indian",
        "location": "London, UK",
        "description": "Former liquor baron and airline owner, economic offender"
    },
    "Vikas Dubey": {
        "aliases": ["Vikas", "Dubey"],
        "crime": "Murder, Extortion, Organized Crime",
        "crime_details": "Gangster involved in multiple murders including 8 policemen in Kanpur ambush",
        "years_in_prison": "Never imprisoned",
        "status": "Dead (Killed 2020)",
        "nationality": "Indian",
        "location": "Uttar Pradesh (Killed in encounter)",
        "description": "Gangster with political connections, killed in police encounter"
    }
}

def seed_data():
    """Update criminal records with detailed information"""
    updated = 0
    not_found = 0
    
    print("Seeding criminal data...")
    
    for name, data in CRIMINAL_DATA.items():
        criminal = get_criminal_by_name(name)
        
        if criminal:
            update_criminal(name, data)
            print(f"Updated: {name}")
            updated += 1
        else:
            print(f"Not found in database: {name}")
            not_found += 1
    
    print(f"\n=== Seeding Complete ===")
    print(f"Updated: {updated}")
    print(f"Not found: {not_found}")

if __name__ == "__main__":
    seed_data()
