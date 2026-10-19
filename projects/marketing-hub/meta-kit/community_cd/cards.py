# Fixed "20 beginnings" card set (layout of divyanshu's version 2, Netflix removed).
# head = (black part, accent part): the biggest line, naming the move into contract drafting.
# body = the approved hook. Readers are the approved 20 in docs/COMMUNITY_HOOKS_CD_LEGALAI_20each_2026-10-19.md.
from ads import ADS

HEADS = {
 "01": ("Graduate as a", "Contract Drafting Lawyer"),
 "02": ("Become the Lawyer", "Startups Hire"),
 "03": ("Start Your Practice", "With Contracts"),
 "04": ("Become the Lawyer", "Businesses Call"),
 "05": ("Draft the Contract", "as the Lawyer"),
 "06": ("Be the Lawyer Clients", "See Before They Sign"),
 "07": ("Draft for Startups", "and UK Businesses"),
 "08": ("Come Back as a", "Contract Drafting Lawyer"),
 "09": ("Draft Contracts", "From Any City"),
 "10": ("Draft for India and", "the UK, From Abroad"),
 "11": ("Become the Lawyer Who", "Drafts HR Contracts"),
 "12": ("Become the Lawyer", "Behind the Deal Papers"),
 "13": ("Write the Contracts", "Businesses Sign"),
 "14": ("Draft the Contracts", "That Close Deals"),
 "15": ("Become the Lawyer", "You Trained to Be"),
 "16": ("From Reviewing Contracts", "to Drafting Them"),
 "17": ("Draft Founder and", "Investor Contracts"),
 "18": ("From Sale Deeds to", "Commercial Contracts"),
 "19": ("Become a Contract Drafting", "Lawyer in College"),
 "20": ("Come Back With", "Your Own Clients"),
}

CARDS = [dict(ad, head=HEADS[ad["id"]]) for ad in ADS]
