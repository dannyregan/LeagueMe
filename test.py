import datetime
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter

def downloadPdf(data, teamName):
    filename = f"{teamName}-schedule.pdf"

    print(data)

    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    formatted_data = [
        tuple(item.strftime("%Y-%m-%d %H:%M") if isinstance(item, datetime.datetime) else item for item in row)
        for row in data
    ]

    headers = ['Home', 'Away', 'Date', 'Result', 'Type']
    formatted_and_headers = [headers] + formatted_data

    table = Table(formatted_and_headers)

    elems = []
    elems.append(table)

    pdf.build(elems)

downloadPdf(data, 'Legends')