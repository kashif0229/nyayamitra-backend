# document_generator.py
from datetime import datetime

def generate_document(case_type: str, query: str, user_name: str = "[YOUR NAME]") -> str:
    """
    Generates appropriate legal document based on the case type
    """
    today = datetime.now().strftime("%d %B %Y")
    
    if case_type == "criminal_fir":
        return generate_fir(query, user_name, today)
    elif case_type == "rti":
        return generate_rti(query, user_name, today)
    elif case_type == "consumer_rights":
        return generate_consumer_complaint(query, user_name, today)
    elif case_type == "rent_housing":
        return generate_legal_notice(query, user_name, today)
    else:
        return generate_general_complaint(query, user_name, today)


def generate_fir(query: str, user_name: str, today: str) -> str:
    return f"""
FIRST INFORMATION REPORT (FIR) DRAFT
=====================================
Date: {today}
To,
The Station House Officer (SHO),
[NAME OF POLICE STATION],
[CITY, STATE]

Subject: FIR regarding [DESCRIBE INCIDENT IN ONE LINE]

Respected Sir/Madam,

I, {user_name}, resident of [YOUR FULL ADDRESS], wish to lodge an FIR regarding the following incident:

FACTS OF THE CASE:
{query}

Date of Incident: [DATE OF INCIDENT]
Place of Incident: [LOCATION WHERE IT HAPPENED]
Name of Accused (if known): [NAME / UNKNOWN]

I respectfully request that an FIR be registered under the appropriate sections of the Bharatiya Nyaya Sanhita (BNS), 2023, and necessary action be taken at the earliest.

I declare that the above facts are true to the best of my knowledge.

Yours faithfully,
{user_name}
Phone: [YOUR PHONE NUMBER]
Date: {today}
Signature: _______________

[AUTO-GENERATED DRAFT — Please review and fill in the bracketed fields before submission]
"""


def generate_rti(query: str, user_name: str, today: str) -> str:
    return f"""
RTI APPLICATION DRAFT
(Under Section 6 of the Right to Information Act, 2005)
=======================================================
Date: {today}
To,
The Public Information Officer (PIO),
[NAME OF GOVERNMENT DEPARTMENT / MINISTRY],
[ADDRESS]

Subject: Request for Information under RTI Act 2005

1. Full Name of Applicant: {user_name}
2. Address: [YOUR FULL ADDRESS]
3. Phone Number: [PHONE NUMBER]
4. Email: [EMAIL ADDRESS]

INFORMATION REQUESTED:
I, {user_name}, a citizen of India, wish to obtain the following information under Section 6 of the RTI Act, 2005:

{query}

Specifically, I request:
a) [SPECIFIC INFORMATION POINT 1]
b) [SPECIFIC INFORMATION POINT 2]
c) Certified copies of relevant documents, if any.

Application Fee: Rs. 10/- (Attached as Postal Order / DD / Cash)

If the information requested is not available with your department, I request you to transfer this application to the concerned PIO under Section 6(3) of the RTI Act within 5 days.

Yours sincerely,
{user_name}
Date: {today}
Signature: _______________

[AUTO-GENERATED DRAFT — Fill in bracketed fields and attach Rs. 10 fee]
"""


def generate_consumer_complaint(query: str, user_name: str, today: str) -> str:
    return f"""
CONSUMER COMPLAINT DRAFT
(Under the Consumer Protection Act, 2019)
=========================================
Date: {today}
To,
The District Consumer Disputes Redressal Commission,
[DISTRICT NAME], [STATE]

COMPLAINANT: {user_name}
Address: [YOUR FULL ADDRESS]
Phone: [PHONE NUMBER]

OPPOSITE PARTY (OP):
Name: [COMPANY / SELLER NAME]
Address: [COMPANY ADDRESS]
Phone: [COMPANY PHONE]

COMPLAINT:
I, {user_name}, am filing this complaint against [COMPANY NAME] for the following reason:

FACTS:
{query}

Date of Purchase/Service: [DATE]
Amount Paid: Rs. [AMOUNT]
Mode of Payment: [CASH / CARD / UPI]
Order/Invoice Number: [ORDER NO.]

DEFICIENCY/UNFAIR PRACTICE:
[DESCRIBE WHAT WENT WRONG CLEARLY]

RELIEF SOUGHT:
1. Refund/Replacement of the product/service worth Rs. [AMOUNT]
2. Compensation for mental agony: Rs. [AMOUNT]
3. Litigation costs: Rs. [AMOUNT]

DECLARATION: I declare that all facts stated above are true to the best of my knowledge.

{user_name}
Date: {today}
Signature: _______________

[AUTO-GENERATED DRAFT — Attach all bills, receipts, and communication proof]
"""


def generate_legal_notice(query: str, user_name: str, today: str) -> str:
    return f"""
LEGAL NOTICE
============
Date: {today}

From: {user_name}
[YOUR ADDRESS]
[PHONE NUMBER]

To: [LANDLORD'S FULL NAME]
[LANDLORD'S ADDRESS]

Subject: Legal Notice for Illegal Eviction / Dispute

Dear Sir/Madam,

Under instructions from my client, {user_name}, I hereby serve this Legal Notice upon you:

FACTS:
{query}

LEGAL POSITION:
As per the Transfer of Property Act, 1882 (Section 106) and the applicable State Rent Control Act, 
no tenant can be evicted without:
1. A proper written notice (minimum 15 days for monthly tenancy)
2. A valid decree from the Rent Control Court

Your actions as described above are in violation of the above laws and constitute an illegal eviction.

DEMAND:
You are hereby called upon to:
1. Immediately restore possession of the premises to my client, OR
2. Provide a valid legal eviction notice within 7 days

NOTICE: Failure to comply within 7 days shall compel my client to initiate appropriate legal proceedings, including filing a complaint with the Rent Controller and seeking damages + compensation.

{user_name}
Date: {today}
Signature: _______________

[AUTO-GENERATED DRAFT — Review with a lawyer before sending]
"""


def generate_general_complaint(query: str, user_name: str, today: str) -> str:
    return f"""
GENERAL LEGAL COMPLAINT DRAFT
==============================
Date: {today}
To,
The Concerned Authority,
[AUTHORITY NAME AND ADDRESS]

Subject: Complaint regarding legal matter

I, {user_name}, resident of [ADDRESS], wish to bring the following matter to your attention:

MATTER:
{query}

I request you to kindly look into this matter and take appropriate action as per the law.

Yours sincerely,
{user_name}
Date: {today}
Signature: _______________

[AUTO-GENERATED DRAFT — Fill in details and consult a lawyer if needed]
"""