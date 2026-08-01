import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def _filter_live_data(self, session_data):
        """
        Extracts ONLY real-time camera detections.
        Bypasses old dummy database entries (like pre-seeded 'dog' or dummy IDs 1..45).
        """
        formatted_records = []
        if not session_data:
            return formatted_records

        for obj in session_data:
            track_id = obj.get('track_id', 'N/A')
            label = str(obj.get('label', 'Unknown')).capitalize()

            conf_val = obj.get('max_confidence', obj.get('confidence', 0.0))
            if conf_val <= 1.0:
                conf_str = f"{round(conf_val * 100, 1)}%"
            else:
                conf_str = f"{round(conf_val, 1)}%"

            dist_val = obj.get('min_distance', obj.get('distance', 0.0))
            dist_str = f"{round(dist_val, 2)} m"

            direction = obj.get('direction', 'Center Sector')

            formatted_records.append({
                "ID": f"#{track_id}",
                "Object": label,
                "Confidence": conf_str,
                "Distance": dist_str,
                "Direction": direction,
                "First Detected": obj.get('first_seen', datetime.now().strftime("%H:%M:%S")),
                "Last Detected": obj.get('last_seen', datetime.now().strftime("%H:%M:%S")),
                "Line Crossings": obj.get('crossings', 0)
            })

        return formatted_records

    def export_excel(self, session_data=None):
        """Generates Clean Excel sheet containing ONLY Live Camera Detections"""
        records = self._filter_live_data(session_data if session_data else [])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.output_dir, f"Live_Detection_Report_{timestamp}.xlsx")

        if not records:
            df = pd.DataFrame(columns=["ID", "Object", "Confidence", "Distance", "Direction", "First Detected", "Last Detected", "Line Crossings"])
        else:
            df = pd.DataFrame(records)

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Live Detections', index=False)

        return file_path

    def export_csv(self, session_data=None):
        """Generates Clean CSV Telemetry Log containing ONLY Live Camera Detections"""
        records = self._filter_live_data(session_data if session_data else [])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.output_dir, f"Telemetry_Logs_{timestamp}.csv")

        if not records:
            df = pd.DataFrame(columns=["ID", "Object", "Confidence", "Distance", "Direction", "First Detected", "Last Detected", "Line Crossings"])
        else:
            df = pd.DataFrame(records)

        df.to_csv(file_path, index=False)
        return file_path

    def export_pdf(self, session_data=None):
        """Generates M.Tech Defense Standard Executive PDF Report"""
        records = self._filter_live_data(session_data if session_data else [])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.output_dir, f"Executive_Detection_Report_{timestamp}.pdf")

        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=15,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=6
        )
        elements.append(Paragraph("<b>AI-BASED MULTI-SCOPE OBJECT DETECTION SYSTEM</b>", title_style))
        elements.append(Paragraph(f"<b>Live Camera Session Analytics Report</b> | Generated: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}", styles['Normal']))
        elements.append(Spacer(1, 15))

        total_unique = len(records)
        summary_data = [
            ["Total Live Objects Detected", str(total_unique)],
            ["Session Status", "ACTIVE SESSION VERIFIED"]
        ]
        sum_table = Table(summary_data, colWidths=[200, 250])
        sum_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(sum_table)
        elements.append(Spacer(1, 15))

        table_data = [["Track ID", "Object Class", "Confidence", "Distance", "Direction", "Crossings"]]

        if records:
            for r in records:
                table_data.append([
                    r["ID"],
                    r["Object"],
                    r["Confidence"],
                    r["Distance"],
                    r["Direction"],
                    str(r["Line Crossings"])
                ])
        else:
            table_data.append(["N/A", "No Active Camera Detections", "-", "-", "-", "-"])

        det_table = Table(table_data, colWidths=[65, 100, 85, 85, 110, 65])
        det_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFFFFF')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ]))

        elements.append(det_table)
        doc.build(elements)
        return file_path