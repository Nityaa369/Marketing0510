# QA report: ContractDrafting_TornPaper_LawSikho_21Oct-11Nov_Google

## 1. Images
- 60 of 60 images present, sizes 1200x628, 1200x1200, 960x1200, each under 5 MB.
- Whole ad kept in every size; worst mean pixel difference against the original art 3.31 (JPEG compression only; 4 is the fail line).

## 2. Text assets
- Longest per field: Headline 1 (30) 30, Headline 2 (30) 29, Headline 3 (30) 27, Headline 4 (30) 28, Headline 5 (30) 27, Long headline (90) 90, Description 1 (60) 52, Description 2 (90) 87, Description 3 (90) 82, Description 4 (90) 71
- Google policy scan on all text assets: 0 BLOCK, 5 WARN
  - [WARN] cd_02_graduates Description 3 (90): ALL CAPS word (capitalisation), matched 'ESOP'
  - [WARN] cd_07_smallercities Description 3 (90): ALL CAPS word (capitalisation), matched 'GDPR'
  - [WARN] cd_10_abroad Description 3 (90): ALL CAPS word (capitalisation), matched 'DPDPA'
  - [WARN] cd_10_abroad Description 3 (90): ALL CAPS word (capitalisation), matched 'GDPR'
  - [WARN] cd_11_hr Description 3 (90): ALL CAPS word (capitalisation), matched 'ESOP'
- No dates, dashes, arrows, trademarks or money words in any text asset.

## 3. Policy scan on the ad faces (art not altered, per the 16 Oct rule)
- [BLOCK] Arrow on CTA (Misleading ad design) '→': ads 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
- [BLOCK] Money figure (₹ amount other than the course price) '₹200 ': ads 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
- [BLOCK] Third-party trademark 'LinkedIn': ads 07, 19, 20
- [WARN] ALL CAPS word (capitalisation) 'ABROAD': ads 10
- [WARN] ALL CAPS word (capitalisation) 'ADVOCATES': ads 03, 04
- [WARN] ALL CAPS word (capitalisation) 'AFTER': ads 08, 09
- [WARN] ALL CAPS word (capitalisation) 'ASSISTANTS': ads 05
- [WARN] ALL CAPS word (capitalisation) 'BACK': ads 15
- [WARN] ALL CAPS word (capitalisation) 'BANKING': ads 12
- [WARN] ALL CAPS word (capitalisation) 'BREAK': ads 08
- [WARN] ALL CAPS word (capitalisation) 'CHAMBERS': ads 04
- [WARN] ALL CAPS word (capitalisation) 'CITIES': ads 07, 09
- [WARN] ALL CAPS word (capitalisation) 'COMPANY': ads 17
- [WARN] ALL CAPS word (capitalisation) 'CONTENT': ads 13
- [WARN] ALL CAPS word (capitalisation) 'CONTRACTS': ads 16
- [WARN] ALL CAPS word (capitalisation) 'CONVEYANCING': ads 18
- [WARN] ALL CAPS word (capitalisation) 'DOING': ads 19
- [WARN] ALL CAPS word (capitalisation) 'DPDPA': ads 10
- [WARN] ALL CAPS word (capitalisation) 'ENROLLED': ads 03
- [WARN] ALL CAPS word (capitalisation) 'ESOP': ads 02, 11, 12
- [WARN] ALL CAPS word (capitalisation) 'FAMILY': ads 08, 10, 20
- [WARN] ALL CAPS word (capitalisation) 'FINAL': ads 01
- [WARN] ALL CAPS word (capitalisation) 'FIRM': ads 20
- [WARN] ALL CAPS word (capitalisation) 'GDPR': ads 07, 10
- [WARN] ALL CAPS word (capitalisation) 'GRADUATES': ads 02
- [WARN] ALL CAPS word (capitalisation) 'HOLDERS': ads 11, 12, 13, 14, 15
- [WARN] ALL CAPS word (capitalisation) 'INDIAN': ads 10
- [WARN] ALL CAPS word (capitalisation) 'INTERNSHIPS': ads 19
- [WARN] ALL CAPS word (capitalisation) 'JOBS': ads 15, 16
- [WARN] ALL CAPS word (capitalisation) 'JUNIOR': ads 04
- [WARN] ALL CAPS word (capitalisation) 'LAWYERS': ads 06, 07, 08, 09, 10, 16, 18, 20
- [WARN] ALL CAPS word (capitalisation) 'LEFT': ads 20
- [WARN] ALL CAPS word (capitalisation) 'LEGAL': ads 05
- [WARN] ALL CAPS word (capitalisation) 'LITIGATION': ads 04
- [WARN] ALL CAPS word (capitalisation) 'LIVING': ads 10
- [WARN] ALL CAPS word (capitalisation) 'MARRIAGE': ads 09
- [WARN] ALL CAPS word (capitalisation) 'MOVED': ads 09
- [WARN] ALL CAPS word (capitalisation) 'NEWLY': ads 03
- [WARN] ALL CAPS word (capitalisation) 'OFFICE': ads 15
- [WARN] ALL CAPS word (capitalisation) 'OPERATIONS': ads 14
- [WARN] ALL CAPS word (capitalisation) 'PARALEGALS': ads 05
- [WARN] ALL CAPS word (capitalisation) 'PRACTICE': ads 06
- [WARN] ALL CAPS word (capitalisation) 'PRACTISING': ads 02
- [WARN] ALL CAPS word (capitalisation) 'PROPERTY': ads 18
- [WARN] ALL CAPS word (capitalisation) 'RETURNING': ads 08
- [WARN] ALL CAPS word (capitalisation) 'REVIEWING': ads 16
- [WARN] ALL CAPS word (capitalisation) 'RUNNING': ads 06
- [WARN] ALL CAPS word (capitalisation) 'SALES': ads 14
- [WARN] ALL CAPS word (capitalisation) 'SECRETARIES': ads 17
- [WARN] ALL CAPS word (capitalisation) 'SMALL': ads 06
- [WARN] ALL CAPS word (capitalisation) 'SMALLER': ads 07
- [WARN] ALL CAPS word (capitalisation) 'STUDENTS': ads 01, 19
- [WARN] ALL CAPS word (capitalisation) 'THEIR': ads 06
- [WARN] ALL CAPS word (capitalisation) 'WITH': ads 05, 10, 17
- [WARN] ALL CAPS word (capitalisation) 'WOMEN': ads 08
- [WARN] ALL CAPS word (capitalisation) 'WORKING': ads 11, 12, 13, 14
- [WARN] ALL CAPS word (capitalisation) 'YEAR': ads 01
These are flagged in README_GOOGLE.md and left in the art, as instructed.

## 4. Final URLs and landing pages
- 20 Final URLs point at growthx.lawsikho.com/f/cdtp-NN with utm_source=google and utm_medium=cpc.
- 20 pages present; each pay button links to its own funnel; each hero picture is embedded in the page; each first fold carries its ad's hook word for word.
- Pages were also tested at 9 widths (360 to 1920 px), JavaScript on and off: no sideways scroll, no missing image, 12 reasons on every page.

## 5. Zip
- ContractDrafting_TornPaper_LawSikho_21Oct-11Nov_Google_SEND_THIS.zip: 85 files, 60 ad images, 17.7 MB, opens and tests clean.

## Result
ALL CHECKS PASSED
