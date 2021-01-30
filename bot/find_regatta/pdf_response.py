from fpdf import FPDF


def pdf_table(data: list):

    pdf = FPDF()
    pdf.add_page()

    for r in data:
        text = f'{r[0]} | {r[2]} | {r[1]}'
        pdf.set_font("Times", 'B', size=12)
        pdf.cell(10, 10, txt=text, ln=10)
        pdf.set_font("Times", size=12)
        pdf.cell(10, 10, r[3], ln=1)

    pdf.output('event_table.pdf')
