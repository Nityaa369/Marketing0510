import csv,json
D2="Tech law is the legal work tech companies need: contracts, privacy, compliance, disputes."
P=[
("tlc1_01_hr","LLB holders working in HR","Move from HR into tech law","LLB holders in HR: move into tech law with 3 live evenings for ₹10","Draft a software development agreement with us. ₹10 incl. GST, refundable."),
("tlc1_02_banking","LLB holders in banking","Take banking into fintech law","LLB holders in banking: learn the tech law behind fintech in 3 live evenings for ₹10","See how tech companies run on payments. ₹10 incl. GST, refundable."),
("tlc1_03_content","LLB holders in content","Draft content contracts","LLB holders in content: learn to draft the contracts behind content in 3 live evenings","Review a startup's terms with us. ₹10 incl. GST, refundable."),
("tlc1_04_sales_ops","LLB holders in sales and operations","Tech law behind every deal","LLB holders in sales and operations: learn the tech law behind the deal for ₹10","Draft an agreement and review vendor terms. ₹10 incl. GST, refundable."),
("tlc1_05_back_from_break","Lawyers back from a practice break","Come back as a tech lawyer","Lawyers back from a practice break: come back through tech law, 3 live evenings for ₹10","Draft and review real documents with us, from home. ₹10 incl. GST, refundable."),
("tlc1_06_moved_city","Lawyers who moved to a new city","Practise tech law anywhere","Lawyers in a new city: learn tech law online in 3 live evenings for ₹10","Draft contracts and review privacy terms, online. ₹10 incl. GST, refundable."),
("tlc1_07_abroad","Indian lawyers living abroad","Tech law from where you are","Indian lawyers abroad: learn tech law online in 3 live evenings for ₹10","A legal education programme, not an immigration or visa service. ₹10 incl. GST."),
("tlc1_08_bpo_back_office","LLB holders in BPO and back-office roles","Back office to tech law","LLB holders in BPO and back office: move into tech law in 3 live evenings for ₹10","Draft real clauses with us. No court time needed. ₹10 incl. GST, refundable."),
("tlc1_09_returning","Lawyers returning after a career break","Return through tech law","Lawyers returning after a career break: refresh your skills in tech law for ₹10","Refresh your skills and draft real documents. ₹10 incl. GST, refundable."),
("tlc1_10_left_firm","Lawyers who left a law firm","Draft for tech companies","Lawyers who left a law firm: draft for tech companies in 3 live evenings for ₹10","Draft a software agreement and review privacy policies. ₹10 incl. GST, refundable."),
]
rows=[]
for s,aud,h1,long,d1 in P:
    h2="Tech law bootcamp for ₹10";h3="3 live evenings, 24 to 26 Oct"
    for t,l in ((h1,30),(h2,30),(h3,30),(long,90),(d1,90),(D2,90)): assert len(t)<=l,(s,len(t),t)
    n=s.split('_')[1]
    rows.append({"Ad":s,"Audience":aud,"Headline 1 (30)":h1,"Headline 2 (30)":h2,"Headline 3 (30)":h3,"Long headline (90)":long,"Description 1 (90)":d1,"Description 2 (90)":D2,"Business name":"LawSikho","Call to action":"Sign up",
      "Final URL":f"https://growthx.lawsikho.com/f/tlc1-{n}?utm_source=google&utm_medium=cpc&utm_campaign=tl_c1_proven_readers&utm_content=tlc1-{n}",
      "Images":f"Tech_Law_C1_Google/<group>/{s}/ (12 files)"})
with open('GOOGLE_COPY_C1.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
json.dump({"rows":rows},open('/tmp/scan.json','w'),ensure_ascii=False)
print("lengths ok")
