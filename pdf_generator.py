"""
HEM Product Catalogue - PDF & Excel Generator
EXACT COPY of user's working PDF/Excel generation logic.
DO NOT MODIFY the HTML output or styling in this file.
"""
import os
import io
import gc
import platform
import subprocess
import logging

import pandas as pd
import pdfkit
import streamlit as st

from config import BASE_DIR, LOGO_PATH, STORY_IMG_1_PATH, COVER_IMG_PATH, WATERMARK_IMG_PATH
from config import COVER_IMAGE_URL, JOURNEY_IMAGE_URL
from cloudinary_client import get_image_as_base64_str
from data_loader import create_safe_id

logger = logging.getLogger(__name__)

# --- WeasyPrint optional import ---
HAS_WEASYPRINT = False
try:
    from weasyprint import HTML, CSS
    HAS_WEASYPRINT = True
except Exception as e:
    logger.info(f"WeasyPrint not available: {e}")
    HAS_WEASYPRINT = False

# --- PDFKIT CONFIG ---
CONFIG = None
try:
    if platform.system() == "Windows":
        paths_to_check = [
            r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
            os.path.join(BASE_DIR, "bin", "wkhtmltopdf.exe"),
        ]
        found_path = None
        for path in paths_to_check:
            if os.path.exists(path):
                found_path = path
                break
        if found_path:
            CONFIG = pdfkit.configuration(wkhtmltopdf=found_path)
    else:
        try:
            path_wkhtmltopdf = subprocess.check_output(
                ['which', 'wkhtmltopdf']
            ).decode('utf-8').strip()
            CONFIG = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        except (subprocess.SubprocessError, FileNotFoundError):
            if os.path.exists('/usr/bin/wkhtmltopdf'):
                CONFIG = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
            else:
                CONFIG = None
except Exception as e:
    logger.warning(f"PDFKit Config Error: {e}")
    CONFIG = None


def generate_story_html(story_img_1_b64):
    text_block_1 = """HEM Corporation is amongst top global leaders in the manufacturing and export of perfumed agarbattis. For over three decades now we have been parceling out high-quality masala sticks, agarbattis, dhoops, and cones to our customers in more than 70 countries. We are known and established for our superior quality products.<br><br>HEM has been showered with love and accolades all across the globe for its diverse range of products. This makes us the most preferred brand the world over. HEM has been awarded as the 'Top Exporters' brand, for incense sticks by the 'Export Promotion Council for Handicraft' (EPCH) for three consecutive years from 2008 till 2011.<br><br>We have also been awarded "Niryat Shree" (Export) Silver Trophy in the Handicraft category by 'Federation of Indian Export Organization' (FIEO). The award was presented to us by the then Honourable President of India, late Shri Pranab Mukherjee."""
    text_journey_1 = """From a brand that was founded by three brothers in 1983, HEM Fragrances has come a long way. HEM started as a simple incense store offering products like masala agarbatti, thuribles, incense burner and dhoops. However, with time, there was a huge evolution in the world of fragrances much that the customers' needs also started changing. HEM incense can be experienced not only to provide you with rich aromatic experience but also create a perfect ambience for your daily prayers, meditation, and yoga.<br><br>The concept of aromatherapy massage, burning incense sticks and incense herbs for spiritual practices, using aromatherapy diffuser oils to promote healing and relaxation or using palo santo incense to purify and cleanse a space became popular around the world.<br><br>So, while we remained focused on creating our signature line of products, especially the 'HEM Precious' range which is a premium flagship collection, there was a dire need to expand our portfolio to meet increasing customer demands."""

    img_tag = ""
    if story_img_1_b64:
        img_tag = f'<img src="data:image/jpeg;base64,{story_img_1_b64}" style="max-width: 100%; height: auto; border: 1px solid #eee;" alt="Awards Image">'
    else:
        img_tag = '<div style="border: 2px dashed red; padding: 20px; color: red;">JOURNEY IMAGE NOT FOUND</div>'

    html = f"""
    <div class="story-page" style="page-break-after: always; padding: 25px 50px; font-family: sans-serif; overflow: hidden; height: 260mm;">
        <h1 style="text-align: center; color: #333; font-size: 28pt; margin-bottom: 20px;">Our Journey</h1>
        <div style="font-size: 11pt; line-height: 1.6; margin-bottom: 30px; text-align: justify;">{text_block_1}</div>
        <div style="margin-bottom: 30px; overflow: auto; clear: both;">
            <div style="float: left; width: 50%; margin-right: 20px; font-size: 11pt; line-height: 1.6; text-align: justify;">{text_journey_1}</div>
            <div style="float: right; width: 45%; text-align: center;">
                {img_tag}
            </div>
        </div>
        <h2 style="text-align: center; font-size: 14pt; margin-top: 40px; clear: both;">Innovation, Creativity, Sustainability</h2>
    </div>
    """
    return html


def generate_table_of_contents_html(df_sorted):
    toc_html = """
    <style>
        .toc-title { text-align: center; font-family: serif; font-size: 32pt; color: #222; margin-bottom: 20px; margin-top: 10px; text-transform: uppercase; letter-spacing: 1px; }
        h3.toc-catalogue-section-header {
            background-color: #333;
            color: #ffffff;
            font-family: sans-serif;
            font-size: 16pt;
            padding: 12px;
            margin: 0 0 15px 0;
            text-align: left;
            border-left: 8px solid #ff9800;
            clear: both;
            page-break-inside: avoid;
        }
        .index-grid-container {
            display: block;
            width: 100%;
            margin: 0 auto;
            font-size: 0;
        }
        a.index-card-link {
            display: inline-block;
            width: 30%;
            margin: 1.5%;
            height: 200px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-decoration: none;
            overflow: hidden;
            border: 1px solid #e0e0e0;
            page-break-inside: avoid;
            vertical-align: top;
        }
        .index-card-image {
            width: 100%;
            height: 160px;
            background-repeat: no-repeat;
            background-position: center center;
            background-size: contain;
            background-color: #f9f9f9;
        }
        .index-card-label {
            height: 40px;
            background-color: #b30000;
            color: white;
            font-family: sans-serif;
            font-size: 9pt;
            font-weight: bold;
            display: block;
            line-height: 40px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 10px;
        }
        .clearfix::after { content: ""; clear: both; display: table; }
    </style>

    <div id="main-index" class="toc-page" style="page-break-after: always; padding: 20px;">
        <h1 class="toc-title">Table of Contents</h1>
    """

    catalogues = df_sorted['Catalogue'].unique()
    is_first_catalogue = True
    for catalogue_name in catalogues:
        page_break_style = 'style="page-break-before: always; padding-top: 20px;"' if not is_first_catalogue else 'style="padding-top: 10px;"'
        toc_html += f'<div {page_break_style}>'
        toc_html += f'<h3 class="toc-catalogue-section-header">{catalogue_name}</h3>'
        toc_html += '<div class="index-grid-container clearfix">'

        cat_df = df_sorted[df_sorted['Catalogue'] == catalogue_name]
        unique_categories = cat_df['Category'].unique()
        for category in unique_categories:
            group = cat_df[cat_df['Category'] == category]
            rep_image = ""
            for _, row in group.iterrows():
                img_str = row.get('ImageB64', '')
                if img_str and len(str(img_str)) > 100:
                    rep_image = img_str
                    break
            bg_style = f"background-image: url('data:image/png;base64,{rep_image}');" if rep_image else "background-color: #eee;"
            safe_id = create_safe_id(category)
            toc_html += f"""
                <a href="#category-{safe_id}" class="index-card-link">
                    <div class="index-card-image" style="{bg_style}"></div>
                    <div class="index-card-label">{category}</div>
                </a>
            """

        toc_html += '</div><div style="clear: both;"></div></div>'
        is_first_catalogue = False

    toc_html += """</div>"""
    return toc_html


def generate_pdf_html(df_sorted, customer_name, logo_b64, case_selection_map):
    def load_img_robust(fname, specific_full_path=None, resize=False, max_size=(500, 500)):
        paths_to_check = []
        if specific_full_path:
            paths_to_check.append(specific_full_path)
        paths_to_check.append(os.path.join(BASE_DIR, "assets", fname))
        paths_to_check.append(os.path.join(BASE_DIR, fname))
        found_path = None
        for p in paths_to_check:
            if os.path.exists(p):
                found_path = p
                break
        if found_path:
            return get_image_as_base64_str(found_path, resize=resize, max_size=max_size)
        return ""

    cover_bg_b64 = get_image_as_base64_str(COVER_IMAGE_URL)
    if not cover_bg_b64:
        cover_bg_b64 = load_img_robust("cover page.png", resize=False)

    story_img_1_b64 = get_image_as_base64_str(JOURNEY_IMAGE_URL, max_size=(600, 600))
    if not story_img_1_b64:
        story_img_1_b64 = load_img_robust("image-journey.png", specific_full_path=STORY_IMG_1_PATH, resize=True, max_size=(600, 600))

    watermark_b64 = load_img_robust("watermark.png", resize=False)

    CSS_STYLES = f"""
        <!DOCTYPE html>
        <html><head><meta charset="UTF-8">
        <style>
        @page {{ size: A4; margin: 0; }}
        * {{ box-sizing: border-box; }}
        html, body {{
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            background-color: transparent !important;
        }}
        #watermark-layer {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1;
            background-image: url('data:image/png;base64,{watermark_b64}');
            background-repeat: repeat; background-position: center center; background-size: cover;
            background-color: transparent;
        }}
        .cover-page {{ width: 210mm; height: 260mm; display: block; position: relative; margin: 0; padding: 0; overflow: hidden; page-break-after: always; background-color: #ffffff; z-index: 10; }}
        .story-page, .toc-page {{ width: 210mm; display: block; position: relative; margin: 0; background-color: transparent; page-break-after: always; }}
        .catalogue-content {{ padding-left: 10mm; padding-right: 10mm; display: block; padding-bottom: 50px; position: relative; z-index: 1; background-color: transparent; }}
        .catalogue-heading {{ background-color: #333; color: white; font-size: 18pt; padding: 8px 15px; margin-bottom: 5px; font-weight: bold; font-family: sans-serif; text-align: center; page-break-inside: avoid; clear: both; }}
        .category-heading {{ color: #333; font-size: 14pt; padding: 8px 0 4px 0; border-bottom: 2px solid #E5C384; margin-top: 5mm; clear: both; font-family: serif; page-break-inside: avoid; width: 100%; }}
        .subcat-pdf-header {{ color: #007bff; font-size: 11pt; font-weight: bold; margin-top: 10px; margin-bottom: 5px; clear: both; font-family: sans-serif; border-left: 3px solid #007bff; padding-left: 8px; page-break-inside: avoid; width: 100%; }}
        .case-size-info {{ color: #555; font-size: 10pt; font-style: italic; margin-bottom: 5px; clear: both; font-family: sans-serif; }}
        .case-size-table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 9pt; margin-bottom: 10px; clear: both; background-color: rgba(255,255,255,0.9); }}
        .case-size-table th {{ border: 1px solid #ddd; background-color: #f2f2f2; padding: 4px; text-align: center; font-weight: bold; font-size: 8pt; color: #333; }}
        .case-size-table td {{ border: 1px solid #ddd; padding: 4px; text-align: center; color: #444; }}
        .cover-image-container {{ position: absolute; top: 0; left: 0; height: 100%; width: 100%; z-index: 1; }}
        .cover-image-container img {{ width: 100%; height: 100%; object-fit: cover; }}
        .clearfix::after {{ content: ""; clear: both; display: table; }}
        .category-block {{
            display: block;
            font-size: 0;
            clear: both;
            page-break-inside: auto;
            margin-bottom: 20px;
            width: 100%;
            page-break-before: always;
        }}
        h1.catalogue-heading + .category-block {{
            page-break-before: avoid !important;
        }}
        .product-card {{
            display: inline-block;
            width: 23%;
            margin: 10px 1%;
            vertical-align: top;
            font-size: 12pt;
            padding: 0;
            box-sizing: border-box;
            background-color: #fcfcfc;
            border: 1px solid #E5C384;
            border-radius: 5px;
            text-align: center;
            position: relative;
            overflow: hidden;
            height: 180px;
            page-break-inside: avoid;
        }}
        .card-image-box {{
            width: 100%;
            height: 115px;
            position: relative;
            background-color: #fff;
            border-bottom: 1px solid #eee;
            overflow: hidden;
        }}
        .card-image-box img {{
            position: absolute;
            top: 0; bottom: 0; left: 0; right: 0;
            margin: auto;
            max-width: 95%;
            max-height: 95%;
            width: auto;
            height: auto;
            display: block;
        }}
        .card-info-box {{
            height: 60px;
            display: block;
            padding: 5px;
        }}
        .card-name {{
            font-family: serif;
            color: #000;
            line-height: 1.2;
            font-weight: bold;
            margin: 0;
            padding-top: 5px;
            display: block;
        }}
        </style></head><body style='margin: 0; padding: 0;'>
        <div id="watermark-layer"></div>
    """

    html_parts = []
    html_parts.append(CSS_STYLES)
    html_parts.append(f"""<div class="cover-page"><div class="cover-image-container"><img src="data:image/png;base64,{cover_bg_b64}"></div></div>""")
    html_parts.append(generate_story_html(story_img_1_b64))
    html_parts.append(generate_table_of_contents_html(df_sorted))
    html_parts.append('<div class="catalogue-content clearfix">')

    def get_val_fuzzy(row_data, keys_list):
        for k in keys_list:
            for data_k in row_data.keys():
                if k.lower() in data_k.lower():
                    return str(row_data[data_k])
        return "-"

    current_catalogue = None
    current_category = None
    current_subcategory = None
    is_first_item = True
    category_open = False

    for index, row in df_sorted.iterrows():
        if row['Catalogue'] != current_catalogue:
            if category_open:
                html_parts.append('</div>')
                category_open = False
            current_catalogue = row['Catalogue']
            current_category = None
            current_subcategory = None
            break_style = 'style="page-break-before: always;"' if not is_first_item else ""
            html_parts.append(f'<div style="clear:both;"></div><h1 class="catalogue-heading" {break_style}>{current_catalogue}</h1>')
            is_first_item = False

        if row['Category'] != current_category:
            if category_open:
                html_parts.append('</div>')
            current_category = row['Category']
            current_subcategory = None
            safe_category_id = create_safe_id(current_category)

            if current_category in case_selection_map:
                try:
                    row_data = case_selection_map[current_category]
                except (KeyError, TypeError):
                    row_data = {}
            else:
                row_data = {}

            html_parts.append('<div class="category-block clearfix">')
            category_open = True
            html_parts.append(f'<h2 class="category-heading" id="category-{safe_category_id}"><a href="#main-index" style="float: right; font-size: 10px; color: #555; text-decoration: none; font-weight: normal; font-family: sans-serif; margin-top: 4px;">BACK TO INDEX &uarr;</a>{current_category}</h2>')

            if row_data:
                desc = row_data.get('Description', '')
                if desc:
                    html_parts.append(f'<div class="case-size-info"><strong>Case Size:</strong> {desc}</div>')
                packing_val = get_val_fuzzy(row_data, ["Packing", "Master Ctn"])
                gross_wt = get_val_fuzzy(row_data, ["Gross Wt", "Gross Weight"])
                net_wt = get_val_fuzzy(row_data, ["Net Wt", "Net Weight"])
                length = get_val_fuzzy(row_data, ["Length"])
                breadth = get_val_fuzzy(row_data, ["Breadth", "Width"])
                height = get_val_fuzzy(row_data, ["Height"])
                cbm_val = get_val_fuzzy(row_data, ["CBM"])
                html_parts.append(f'''<table class="case-size-table"><tr><th>Packing per Master Ctn<br>(doz/box)</th><th>Gross Wt.<br>(Kg)</th><th>Net Wt.<br>(Kg)</th><th>Length<br>(Cm)</th><th>Breadth<br>(Cm)</th><th>Height<br>(Cm)</th><th>CBM</th></tr><tr><td>{packing_val}</td><td>{gross_wt}</td><td>{net_wt}</td><td>{length}</td><td>{breadth}</td><td>{height}</td><td>{cbm_val}</td></tr></table>''')

        sub_val = str(row.get('Subcategory', '')).strip()
        if sub_val.upper() != 'N/A' and sub_val.lower() != 'nan' and sub_val != '':
            if sub_val != current_subcategory:
                current_subcategory = sub_val
                html_parts.append(f'<div class="subcat-pdf-header">{current_subcategory}</div>')

        img_url = row.get("ImageB64", "")
        if not img_url.startswith("http"):
            pass
        else:
            img_b64 = get_image_as_base64_str(img_url)
            row["ImageB64"] = img_b64

        img_b64 = row["ImageB64"]
        mime_type = 'image/png' if (img_b64 and len(img_b64) > 20 and img_b64[:20].lower().find('i') != -1) else 'image/jpeg'
        image_html_content = f'<img src="data:{mime_type};base64,{img_b64}" alt="Img">' if img_b64 else '<div style="padding-top:40px; color:#ccc; font-size:10px;">IMAGE NOT FOUND</div>'
        new_badge_html = """<div style="position: absolute; top: 0; right: 0; background-color: #dc3545; color: white; font-size: 8px; font-weight: bold; padding: 2px 8px; border-radius: 0 0 0 5px; z-index: 10;">NEW</div>""" if row.get('IsNew') == 1 else ""

        item_name_text = row.get('ItemName', 'N/A')
        name_len = len(str(item_name_text))
        if name_len < 30:
            font_size = "9pt"
        elif name_len < 50:
            font_size = "8pt"
        else:
            font_size = "7pt"

        card_html = f"""
        <div class="product-card">
            {new_badge_html}
            <div class="card-image-box">
                {image_html_content}
            </div>
            <div class="card-info-box">
                <div class="card-name" style="font-size: {font_size};">
                    <span style="color: #007bff; margin-right: 2px;">{index+1}.</span>{item_name_text}
                </div>
            </div>
        </div>
        """
        html_parts.append(card_html)

    if category_open:
        html_parts.append('</div>')
    html_parts.append('<div style="clear: both;"></div></div></body></html>')
    return "".join(html_parts)


def generate_excel_file(df_sorted, customer_name, case_selection_map):
    output = io.BytesIO()
    excel_rows = []
    for idx, row in df_sorted.iterrows():
        cat = row['Category']
        suffix = ""
        cbm = 0.0
        if cat in case_selection_map:
            case_data = case_selection_map[cat]
            for k in case_data.keys():
                if "suffix" in k.lower():
                    suffix = str(case_data[k]).strip()
                if "cbm" in k.lower():
                    try:
                        cbm = round(float(case_data[k]), 3)
                    except (ValueError, TypeError):
                        cbm = 0.0
            if suffix == 'nan':
                suffix = ""
        full_name = str(row['ItemName']).strip()
        if suffix:
            full_name = f"{full_name} {suffix}"
        excel_rows.append({
            "Ref No": idx + 1, "Category": cat,
            "Product Name + Carton Name": full_name,
            "Carton per CBM": cbm, "Order Quantity (Cartons)": 0, "Total CBM": 0
        })

    df_excel = pd.DataFrame(excel_rows)
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_excel.to_excel(writer, index=False, sheet_name='Order Sheet', startrow=7)
        workbook = writer.book
        worksheet = writer.sheets['Order Sheet']
        header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        input_fmt = workbook.add_format({'bg_color': '#FFFCB7', 'border': 1, 'locked': False})
        locked_fmt = workbook.add_format({'border': 1, 'locked': True, 'num_format': '0.000'})
        count_fmt = workbook.add_format({'num_format': '0.00', 'bold': True, 'border': 1})
        title_fmt = workbook.add_format({'bold': True, 'font_size': 14})

        worksheet.protect()
        worksheet.freeze_panes(8, 0)
        worksheet.write('B1', f"Order Sheet for: {customer_name}", title_fmt)
        worksheet.write('B2', 'Total CBM:')
        worksheet.write_formula('C2', f'=SUM(F9:F{len(df_excel)+9})', workbook.add_format({'num_format': '0.000'}))
        worksheet.write('B3', 'CONTAINER TYPE', workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1}))
        worksheet.write('C3', 'ESTIMATED CONTAINERS', workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1}))
        worksheet.write('B4', '20 FT (30 CBM)', workbook.add_format({'border': 1}))
        worksheet.write('B5', '40 FT (60 CBM)', workbook.add_format({'border': 1}))
        worksheet.write('B6', '40 FT HC (70 CBM)', workbook.add_format({'border': 1}))
        worksheet.write_formula('C4', '=$C$2/30', count_fmt)
        worksheet.write_formula('C5', '=$C$2/60', count_fmt)
        worksheet.write_formula('C6', '=$C$2/70', count_fmt)
        for col_num, value in enumerate(df_excel.columns):
            worksheet.write(7, col_num, value, header_fmt)
        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 50)
        worksheet.set_column('D:F', 15)
        for i in range(len(df_excel)):
            row_idx = i + 9
            worksheet.write(row_idx - 1, 4, 0, input_fmt)
            worksheet.write_formula(row_idx - 1, 5, f'=D{row_idx}*E{row_idx}', locked_fmt)
    return output.getvalue()


def render_pdf(html_string):
    """Generate PDF bytes from HTML string. Returns (pdf_bytes, engine_name) or (None, error_msg)."""
    try:
        if CONFIG:
            options = {
                'page-size': 'A4', 'margin-top': '0mm', 'margin-right': '0mm',
                'margin-bottom': '0mm', 'margin-left': '0mm', 'encoding': "UTF-8",
                'no-outline': None, 'enable-local-file-access': None,
                'disable-smart-shrinking': None, 'print-media-type': None,
            }
            pdf_bytes = pdfkit.from_string(html_string, False, configuration=CONFIG, options=options)
            gc.collect()
            return pdf_bytes, "PDFKit (Local)"
        elif HAS_WEASYPRINT:
            pdf_bytes = HTML(string=html_string, base_url=BASE_DIR).write_pdf()
            gc.collect()
            return pdf_bytes, "WeasyPrint (Cloud)"
        else:
            return None, "No PDF engine found! Install 'wkhtmltopdf' locally or 'weasyprint' on server."
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        return None, str(e)
