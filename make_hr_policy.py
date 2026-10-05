"""Builds HR_Policy.pdf: a 12-page FICTIONAL employee handbook used as the sample
document for the "Build with me" series. Leave rules sit on page 4 (matches reel #31).
The company, people and numbers are invented."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

COMPANY = "Bluepeak Example Ltd"

PAGES = [
    ("Employee Handbook", [
        f"Welcome to {COMPANY}. This handbook explains how we work together, what you can expect from us, and what we expect from you.",
        "It covers working hours, pay, leave, remote work, expenses, travel, conduct, IT security and who to contact with questions.",
        "This handbook applies to all full-time employees. Part-time employees receive the same benefits on a pro-rata basis unless stated otherwise.",
        "Policy version 3.2, effective 1 January 2026. If anything here is unclear, ask the People Team before acting.",
    ]),
    ("1. Working Hours", [
        "Our standard working week is 40 hours, Monday to Friday. Core hours are 10:00 to 16:00, when everyone should be available for meetings.",
        "Outside core hours you may start and finish when it suits you, as long as you agree your pattern with your manager.",
        "Lunch breaks are 60 minutes and are not counted as working time.",
        "Overtime must be approved in advance by your manager. Approved overtime is paid at 1.5 times your normal hourly rate, or taken as time off in lieu.",
    ]),
    ("2. Pay and Benefits", [
        "Salaries are paid monthly, on the last working day of each month, directly into your bank account.",
        "Pay is reviewed once a year in April. Reviews take into account performance, market rates and company results.",
        "All employees join the company health plan from their first day. Your spouse and children can be added at no extra cost.",
        "We contribute 5% of your base salary to the company pension scheme each month.",
    ]),
    ("3. Annual Leave", [
        "Every full-time employee gets 24 days of paid annual leave each calendar year, plus public holidays.",
        "Leave builds up at 2 days per month worked. In your first year, leave is calculated from your start date.",
        "Book leave through the HR portal at least two weeks in advance. Requests of more than 10 consecutive days need approval from your department head.",
        "You may carry over up to 5 unused days into the next year. Carried-over days must be used by 31 March, or they are lost.",
        "After 5 years of service you receive 2 extra days of annual leave each year.",
    ]),
    ("4. Sick Leave", [
        "You are entitled to 10 days of paid sick leave each year.",
        "Tell your manager before 10:00 on the first day you are unable to work.",
        "For absences longer than 3 consecutive working days, please provide a doctor's note.",
        "Unused sick leave does not carry over into the next year.",
    ]),
    ("5. Parental Leave", [
        "Birth mothers receive 16 weeks of fully paid maternity leave.",
        "Fathers and partners receive 4 weeks of fully paid parental leave, to be taken within the first 6 months after the birth or adoption.",
        "Adoptive parents receive the same leave as birth parents.",
        "Please tell the People Team at least 8 weeks before your leave is due to start.",
    ]),
    ("6. Remote Work", [
        "You may work from home up to 3 days per week, with your manager's agreement.",
        "Every employee receives a one-time home-office allowance of 300 US dollars to buy a chair, desk or monitor.",
        "When working remotely you must use the company VPN and keep company data on company devices only.",
        "Working from another country for more than 2 weeks requires approval from the People Team, for tax reasons.",
    ]),
    ("7. Expenses", [
        "Business expenses are reimbursed when they are necessary, reasonable and approved.",
        "Expense claims must be filed within 30 days through the finance portal, with receipts attached.",
        "Meals while travelling are covered up to 50 US dollars per day.",
        "Parking is free for staff in Block B. Parking fines are not reimbursed.",
    ]),
    ("8. Travel", [
        "Book all business travel through the company travel desk.",
        "Economy class is standard for flights under 6 hours. Business class may be approved for longer flights.",
        "Hotels should not exceed 180 US dollars per night unless approved by your department head.",
        "Travel insurance is provided automatically for all business trips.",
    ]),
    ("9. Code of Conduct", [
        "Treat colleagues, customers and partners with respect. Harassment and discrimination of any kind are not tolerated.",
        "Declare any gift worth more than 50 US dollars to your manager.",
        "Avoid conflicts of interest. If you have a side business that could compete with ours, tell the People Team.",
        "Concerns can be raised confidentially through the ethics hotline.",
    ]),
    ("10. IT and Security", [
        "Use a password manager and enable two-factor authentication on all work accounts.",
        "Never share your password, even with IT staff.",
        "Report lost laptops or phones to the IT Helpdesk within 24 hours.",
        "Do not paste confidential company data into public AI tools. Use the approved internal assistant instead.",
    ]),
    ("11. Contacts", [
        "People Team: people@bluepeak.example, for leave, pay, benefits and policy questions.",
        "IT Helpdesk: extension 4000, for laptops, accounts and security.",
        "Finance: finance@bluepeak.example, for expenses and payroll.",
        "Ethics hotline: available 24 hours a day, 7 days a week. Reports can be anonymous.",
    ]),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillGray(0.4)
    canvas.drawString(20 * mm, 12 * mm, f"{COMPANY} (fictional example for a tutorial)")
    canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def main():
    h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=22, leading=28, spaceAfter=14)
    b = ParagraphStyle("b", fontName="Helvetica", fontSize=12, leading=18, spaceAfter=10)
    story = []
    for i, (title, paras) in enumerate(PAGES):
        story.append(Paragraph(title, h))
        story.append(Spacer(1, 4))
        for p in paras:
            story.append(Paragraph(p, b))
        if i < len(PAGES) - 1:
            story.append(PageBreak())
    doc = SimpleDocTemplate("HR_Policy.pdf", pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=25 * mm, bottomMargin=25 * mm)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    main()
