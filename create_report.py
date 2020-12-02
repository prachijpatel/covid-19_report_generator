from fpdf import FPDF
import pandas as pd
from datetime import date, timedelta
from create_map import map_create
from create_total_csv import get_total, graph, grab_total, get_diff
from create_csv import get_data
import smtplib
import os
import imghdr
from email.message import EmailMessage

WIDTH = 210
HEIGHT = 297

get_data()

confirmed_t = pd.read_csv("./data/confirmed_t.csv")
map_create(confirmed_t, "Confirmed", "Blues")
confirmed = get_total(confirmed_t, "confirmed")

deceased_t = pd.read_csv("./data/deceased_t.csv")
map_create(deceased_t, "Deceased", "Reds")
deceased = get_total(deceased_t, "deceased")

recovered_t = pd.read_csv("./data/recovered_t.csv")
map_create(recovered_t, "Recovered", "Greens")
recovered = get_total(recovered_t, "recovered")

graph(confirmed, "Confirmed", "b")
graph(deceased, "Deceased", "r")
graph(recovered, "Recovered", "g")


pdf = FPDF()
# first page
pdf.add_page()
pdf.set_font("Arial", "B""I", size=30)

pdf.cell(200, 10, txt="COVID - 19 Analysis Report",
         ln=1, align='C')
pdf.set_font("Arial", "B", size=20)
pdf.cell(200, 10, txt="Prachi j Patel",
         ln=2, align='C')

pdf.ln(10)
pdf.set_font("Arial", "U", size=23)
# def add_txt():
pdf.cell(200, 10, txt="COVID-19 information till {}".format(
    (date.today()-timedelta(days=1)).strftime("%B %d,%Y")),
    ln=2, align='C')

pdf.ln(10)
names = ["confirmed", "recovered"]
for i in names:
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt="Total {} Cases".format(i),
             ln=2)
    pdf.set_font("Arial", "B", size=20)
    if i == "confirmed":
        pdf.cell(200, 10, txt="{:,}".format(grab_total(confirmed_t)),
                 ln=3)
    if i == "recovered":
        pdf.cell(200, 10, txt="{:,}".format(grab_total(recovered_t)),
                 ln=3)

    pdf.ln(5)
pdf.set_font("Arial", size=20)
pdf.cell(200, 10, txt="Total Deaths",
         ln=2)
pdf.set_font("Arial", "B", size=20)
pdf.cell(200, 10, txt="{:,}".format(grab_total(deceased_t)),
         ln=3)
pdf.ln(10)
pdf.set_font("Arial", size=20)
pdf.cell(200, 10, txt="So we can say that, the total active cases in India are,",
         ln=2)


pdf.set_font("Arial", "B", size=20)
pdf.cell(200, 10, txt="{:,}".format(grab_total(confirmed_t)-grab_total(recovered_t)),
         ln=3)

pdf.ln(20)
pdf.set_font("Arial", "U", size=23)
pdf.cell(200, 10, txt="COVID-19 rise on {}".format(
    (date.today()-timedelta(days=1)).strftime("%B %d,%Y")),
    ln=2, align='C')
pdf.ln(10)
pdf.set_font("Arial", size=20)
pdf.cell(200, 10, txt="Rise in Confirmed Cases",
         ln=2)


pdf.set_font("Arial", "B", size=20)
pdf.cell(200, 10, txt="{:,}".format(get_diff(confirmed_t)),
         ln=3)

pdf.ln(5)
pdf.set_font("Arial", size=20)
pdf.cell(200, 10, txt="Rise in Recovered Cases",
         ln=2)


pdf.set_font("Arial", "B", size=20)
pdf.cell(200, 10, txt="{:,}".format(get_diff(recovered_t)),
         ln=3)

pdf.ln(5)
pdf.set_font("Arial", size=20)
pdf.cell(200, 10, txt="Rise in Deaths",
         ln=2)


pdf.set_font("Arial", "B", size=20)
pdf.cell(200, 10, txt="{:,}".format(get_diff(deceased_t)),
         ln=3)


pdf.add_page()
pdf.image("./images/Confirmed_graph.png", 5, 5, WIDTH - 20)

pdf.image("./images/Confirmed.png", 5, 140, WIDTH-20)


pdf.add_page()
pdf.image("./images/Recovered_graph.png", 5, 5, WIDTH - 20)

pdf.image("./images/Recovered.png", 5, 140, WIDTH-20)


pdf.add_page()
pdf.image("./images/Deceased_graph.png", 5, 5, WIDTH - 20)

pdf.image("./images/Deceased.png", 5, 140, WIDTH-20)
print("Hello")
pdf.output("report.pdf", 'F')

EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
# EMAIL_USER = 'pachi.jpatel1@gmail.com'
# EMAIL_PASSWORD = 'gyaeltuvdkbiuwid'
print(EMAIL_USER, EMAIL_PASSWORD)
contacts = ['prachi.jpatel23@gmail.com', 'prachi.jpatel11@gmail.com']

msg = EmailMessage()
msg['Subject'] = "Covid-19 report"
msg["From"] = 'prachi.jpatel1@gmail.com'
msg["To"] = contacts
msg.set_content("The current information of covid.")
msg.add_alternative("""\
<!DOCTYPE html>
<html>

<body>
    <h3>Current information of COVID-19</h3>
</body>

</html>
""", subtype='html')
with open("report.pdf", 'rb') as f:
    file_data = f.read()
    file_name = f.name


msg.add_attachment(file_data, maintype='application',
                   subtype='octet-stream', filename=file_name)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

    smtp.login(EMAIL_USER, EMAIL_PASSWORD)
    smtp.send_message(msg)
