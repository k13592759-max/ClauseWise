"""Editorial explanations of fictional samples; never applied to uploaded files."""
RENTAL = {
 '2.': ('A fixed term, with no automatic renewal.', 'The tenancy runs from 1 October 2026 to 30 September 2027. Both parties must sign a written agreement to renew it. Do not assume that continuing to pay rent renews this document.'),
 '3.': ('Monthly rent plus an upfront deposit.', 'The tenant pays INR 20,000 monthly by the fifth and INR 60,000 before possession. Deductions are limited here to unpaid rent and documented damage beyond ordinary wear. This section gives 30 calendar days for returning the balance after possession is returned; section 7 instead gives 45 days.'),
 '4.': ('A fixed fee when rent is late.', 'If rent is still unpaid after the fifth, a single INR 500 fee applies for that month. This passage does not set a daily charge. It does not establish whether a charge is legally recoverable.'),
 '5.': ('Notice and an additional early-exit charge.', 'Either party can give 60 calendar days of written notice. If the tenant leaves before 31 March 2027, one month’s rent is also charged. The document does not say how to deliver notice or when it is received, so a final notice deadline needs clarification.'),
 '6.': ('Repair duties depend on the cause.', 'The tenant handles damage from misuse; the landlord handles structural repairs. Entry normally needs 24 hours’ notice, but emergencies are an exception. The agreement does not define an emergency here.'),
 '7.': ('Two different deposit-return periods.', 'This section gives 45 calendar days after possession is returned, subject to documented deductions. Section 3 gives 30 days. Ask the parties to resolve the difference in writing; this example does not decide which controls.'),
 '8.': ('The agreement names Indian law and Pune courts.', 'Those are the terms stated in the document. Their legal effect needs jurisdiction-specific advice. The absence of a described mediation process does not establish that mediation is unavailable.')
}
FREELANCE = {
 '2.': ('Payment is split into two instalments.', 'The client pays INR 40,000 on signing and INR 40,000 within 15 calendar days of delivery. The stated total is INR 80,000. No late fee is specified; do not invent one.'),
 '3.': ('Delivery depends on receiving client content.', 'The 30 November 2026 delivery date is conditional on content arriving by 1 November. Two revision rounds are included. Additional work needs a written price agreement. The clause does not specify a replacement deadline if content arrives late.'),
 '4.': ('Ownership transfers only after full payment.', 'The client receives ownership of final deliverables after paying in full. The freelancer keeps pre-existing tools. Clarify which items are final deliverables and what rights the client gets to embedded tools.'),
 '5.': ('Either side can terminate with notice.', 'Either party gives 14 calendar days of written notice. The client pays for completed work, but the value of partially completed work is not defined. Agree on valuation before relying on a cancellation estimate.'),
 '6.': ('Confidentiality continues after the work ends.', 'Both parties keep non-public business information confidential for two years after termination. Public information and legally required disclosure are exceptions. The term does not itself establish how a disclosure should be handled.')
}

def enrich(doc):
    library = FREELANCE if 'Freelancer' in doc['name'] else RENTAL
    revised = 'revision' in doc['name']
    for clause in doc['clauses']:
        key = clause['heading'].split(' ')[0]
        if key not in library: continue
        short, detailed = library[key]
        if revised:
            detailed = detailed.replace('20,000','23,000').replace('60,000','69,000').replace('60 calendar','90 calendar').replace('30 September 2027','31 August 2027')
            if key in ('3.','7.'):
                short='Deposit return periods are aligned.'
                detailed='Sections 3 and 7 both state 30 calendar days after possession is returned. Section 3 allows deductions for unpaid rent and documented damage beyond ordinary wear. The revised deposit is INR 69,000. Confirm the deduction records and when possession counts as returned.'
        clause['explanation']={'quick':short,'detailed':detailed,'beginner':detailed+' Read “must” as a stated duty and “if” as a condition. Whether the term applies to your situation needs more context.'}
        for f in doc['findings']:
            if f['source_id']==clause['id'] and f['id']!='deposit-conflict':
                f['explanation']=detailed
                f['evidence_status']='Interpretation'
