# classifier.py

# Keywords that indicate each category
CATEGORY_KEYWORDS = {
    "criminal_fir": [
        "fir", "police", "assault", "theft", "robbery", "murder", "beat",
        "attack", "stolen", "kidnap", "rape", "harassment", "threaten",
        "mara", "chori", "maar", "dhamki", "peeta"  # Hindi words too
    ],
    "consumer_rights": [
        "product", "defective", "refund", "company", "service", "fraud",
        "online", "amazon", "flipkart", "cheated", "quality", "warranty",
        "dhokha", "paisa wapas", "saman kharab"
    ],
    "rti": [
        "rti", "information", "government", "reply", "public", "authority",
        "application", "office", "department", "jankari", "adhikar"
    ],
    "labor_rights": [
        "salary", "job", "fired", "employer", "pf", "provident", "wages",
        "work", "office", "boss", "company", "terminated", "naukri",
        "tankhwah", "maalik", "kaam"
    ],
    "women_family": [
        "dowry", "domestic", "husband", "wife", "divorce", "maintenance",
        "custody", "child", "marriage", "abuse", "violence", "harassment",
        "dahej", "talak", "pati", "patni"
    ],
    "rent_housing": [
        "rent", "landlord", "tenant", "evict", "house", "flat", "deposit",
        "lease", "property", "accommodation", "ghar", "kiraya", "makan",
        "makaan malik", "nikal diya"
    ]
}

def classify_case(query: str) -> str:
    """
    Looks at the user's query and returns the most likely legal category
    """
    query_lower = query.lower()
    
    # Count keyword matches for each category
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        scores[category] = score
    
    # Return the category with the highest score
    best_category = max(scores, key=scores.get)
    
    # If no keywords matched at all, return "general"
    if scores[best_category] == 0:
        return "general"
    
    return best_category


def get_category_display_name(category: str) -> str:
    """Converts internal category name to display name"""
    names = {
        "criminal_fir": "Criminal / FIR",
        "consumer_rights": "Consumer Rights",
        "rti": "RTI (Right to Information)",
        "labor_rights": "Labor & Employment",
        "women_family": "Women & Family Law",
        "rent_housing": "Rent & Housing",
        "general": "General Legal Query"
    }
    return names.get(category, "General Legal Query")