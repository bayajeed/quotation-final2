import os
import io
from fpdf import FPDF
from django.conf import settings
from .utils import number_to_words_indian


# ===========================================
# Custom PDF Class (inherits from FPDF)
# ===========================================
class PDF(FPDF):
    def header(self):
        """
        ✅ Header অংশে:
        - Logo বসানো হয়েছে বাম পাশে
        - Company information ডান পাশে
        - নিচে একটা লাইন দেওয়া হয়েছে header আলাদা বোঝানোর জন্য
        """

        # Light gray background box (header background)
        self.set_fill_color(245, 245, 245)
        self.rect(10, 5, 190, 20, 'DF')  # x, y, width, height, fill flag, # FD = Fill and Draw , Fill only = F , Draw only = D, no fill or draw = empty

        # --- Logo ---
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'assets/images/uniko_logo.png')
        self.image(logo_path, 12, 6, 18)  # (x=12, y=4, width=18)

        # --- Company Info ---
        self.set_xy(35, 7)  # Set text cursor position
        self.set_font('Arial', 'B', 16)
        self.cell(0, 6, 'Uniko Power Engineering Ltd.', ln=1)

        self.set_x(35)
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'House #18, Lane #15, Block C, Mirpur #10, Dhaka', ln=1)

        self.set_x(35)
        self.cell(0, 5, 'Phone: 01711 183 455 | Email: unikopower@gmail.com', ln=1)

        # --- নিচে লাইন ---
        # self.set_line_width(0.5)
        # self.line(10, 24, 200, 24) # x1, y1, x2, y2
        # self.ln(10)  # Line break / spacing

    def add_page(self, orientation='', format='', same=False):
        """
        ✅ প্রতিবার নতুন পেজ যুক্ত হলে কনটেন্টের শুরুর পজিশন ঠিক করে।
        প্রথম পেজে থাকবে Y=28, বাকিগুলোতে Y=35।
        """
        super().add_page(orientation, format, same)
        if self.page_no() > 1:
            self.set_y(28)
        else:
            self.set_y(28)

    def footer(self):
        """
        Footer অংশে:
        - পেজ নাম্বার দেখাবে "Page 1/3" এইরকমভাবে
        """
        self.set_y(-10)  # 15mm উপরে থেকে শুরু হবে
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')


# ===========================================
# Function: generate_quotation_pdf
# Purpose: Generate PDF file dynamically from quotation data
# ===========================================
def generate_quotation_pdf(quotation):
    # Create PDF instance
    pdf = PDF()
    pdf.alias_nb_pages()  # Footer-এ {nb} ব্যবহার করার জন্য প্রয়োজন
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Times', '', 12)

    # ----------------------------
    # 🧍‍♂️ Customer / Quotation Info
    # ----------------------------
    pdf.set_y(28)  # Header থেকে নিচে নামানো হলো
    pdf.set_font('Times', 'B', 12)
    line_height = 1 # Line height for the info rows

    # এক লাইনে সব info: Name | Project | Ref | Date
    pdf.cell(50, line_height, f'Name: {quotation.client_name}', border=0)
    pdf.cell(50, line_height, f'Project: {quotation.title}', border=0)
    pdf.cell(45, line_height, f'Ref: Uniko/Sub/120{quotation.pk}', border=0)
    pdf.cell(45, line_height, f'Date: {quotation.created_at.strftime("%d %b %Y")}', ln=1, border=0)

    # Extra gap বাদ দিতে ছোট ln ব্যবহার করা হয়েছে
    pdf.ln(4)

    # ----------------------------
    # 🧾 Table Header
    # ----------------------------
    pdf.set_fill_color(200, 220, 255)  # হালকা নীল ব্যাকগ্রাউন্ড
    pdf.set_font('Times', 'B', 12)

    # প্রতিটা কলাম define করা হচ্ছে: width, height, title, border, next, align, fill
    pdf.cell(10, 6, 'SL', 1, 0, 'C', 1)
    pdf.cell(85, 6, 'Description', 1, 0, 'C', 1)
    pdf.cell(20, 6, 'Qty', 1, 0, 'C', 1)
    pdf.cell(20, 6, 'Unit', 1, 0, 'C', 1)
    pdf.cell(27, 6, 'Unit Price', 1, 0, 'C', 1)
    pdf.cell(28, 6, 'Total Price', 1, 1, 'C', 1)

    # ----------------------------
    # 📋 Table Body (Item List)
    # ----------------------------
    sl = 1  # Serial number শুরু
    pdf.set_font('Times', '', 11)

    for group in quotation.groups.all():
        # --- Group Title ---
        pdf.set_font('Times', 'B', 12)
        pdf.cell(190, 6, group.name, 1, 1, 'L')
        pdf.set_font('Times', '', 11)

        # --- Items under this group ---
        for item in group.items.all():
            description = ''
            if item.description:
                description = item.description
            elif item.item:
                description = item.item.name

            unit_name = ''
            if item.unit:
                unit_name = item.unit.name
            elif item.item and item.item.unit:
                unit_name = item.item.unit.name

            pdf.cell(10, 5.5, str(sl), 1, 0, 'C')
            pdf.cell(85, 5.5, description, 1, 0, 'L')
            pdf.cell(20, 5.5, str(item.qty), 1, 0, 'R')
            pdf.cell(20, 5.5, unit_name, 1, 0, 'C')
            pdf.cell(27, 5.5, f'{item.unit_price:,.2f}', 1, 0, 'R')
            pdf.cell(28, 5.5, f'{item.total_price:,.2f}', 1, 1, 'R')
            sl += 1  # Serial increment

        # --- Subtotal (per group) ---
        pdf.set_font('Times', 'B', 11)
        pdf.cell(162, 5.5, 'Sub-Total', 1, 0, 'R')
        pdf.cell(28, 5.5, f'{group.subtotal():,.2f}', 1, 1, 'R')

    # ----------------------------
    # 💰 Grand Total
    # ----------------------------
    pdf.set_font('Times', 'B', 12)
    pdf.cell(162, 7, 'Grand Total', 1, 0, 'R', fill=True)
    pdf.cell(28, 7, f'{quotation.total_amount():,.2f}', 1, 1, 'R')

    pdf.ln(1) # Extra gap before total in words

    # ----------------------------
    # 🔤 Total in Words
    # ----------------------------
    total_in_words = number_to_words_indian(quotation.total_amount())
    total_in_words = total_in_words.replace('lakh', 'lac').replace('Lakhs', 'Lacs')
    pdf.set_font('Times', 'B', 12)
    pdf.cell(25, 10, 'In Words:', 0, 0)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 10, total_in_words, 0, 'L')

    # ----------------------------
    # 🧩 Generate and return as Bytes
    # ----------------------------
    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
