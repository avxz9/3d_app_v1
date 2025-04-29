import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import numpy as np
import io

class DefectReportGenerator:

    def __init__(self, json_data=None):
       
        self.data = json_data
            
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='Heading1Center',
            parent=self.styles['Heading1'],
            alignment=1
        ))
        self.styles.add(ParagraphStyle(
            name='Normal_Center',
            parent=self.styles['Normal'],
            alignment=1
        ))
        
    def create_pdf(self):
 
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        story.append(Paragraph("3D Model Defect Analysis Report", self.styles['Heading1Center']))
        story.append(Spacer(1, 20))
        

        model_name = os.path.basename(self.data["model_path"])
        story.append(Paragraph(f"Model: {model_name}", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        summary_data = [
            ["Analysis Date:", datetime.fromisoformat(self.data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")],
            ["Watertight Model:", "Yes" if self.data["watertight"] else "No"],
            ["Total Defects Found:", str(self.data["defect_count"])]
        ]
        
        summary_table = Table(summary_data, colWidths=[150, 350])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        if self.data["defect_count"] > 0:
            story.append(Paragraph("Defect Summary", self.styles['Heading2']))
            story.append(Spacer(1, 10))
            
            defect_types = {}
            severity_counts = {"low": 0, "medium": 0, "high": 0}
            
            for defect in self.data["defects"]:
                defect_type = defect["type"]
                if defect_type not in defect_types:
                    defect_types[defect_type] = 0
                defect_types[defect_type] += 1
                
                severity = defect["severity"]
                severity_counts[severity] += 1
            
            type_data = [["Defect Type", "Count"]]
            for defect_type, count in defect_types.items():
                formatted_type = defect_type.replace('_', ' ').title()
                type_data.append([formatted_type, str(count)])
            
            type_table = Table(type_data, colWidths=[200, 100])
            type_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            story.append(type_table)
            story.append(Spacer(1, 20))
            
            
            story.append(Paragraph("Detailed Defect List", self.styles['Heading2']))
            story.append(Spacer(1, 10))
            
            for i, defect in enumerate(self.data["defects"]):

                formatted_type = defect["type"].replace('_', ' ').title()
                
                severity_color = {
                    "low": colors.green,
                    "medium": colors.orange,
                    "high": colors.red
                }.get(defect["severity"], colors.black)
                
                severity_str = f'<font color="{severity_color.hexval()}">{defect["severity"].upper()}</font>'
                
                story.append(Paragraph(f"Defect #{i+1}: {formatted_type} (Severity: {severity_str})", 
                                       self.styles['Heading3']))
                
      
                loc = defect["location"]
                location_str = f"Location: X={loc[0]:.2f}, Y={loc[1]:.2f}, Z={loc[2]:.2f}"
                story.append(Paragraph(location_str, self.styles['Normal']))
                
                story.append(Paragraph(f"Affected Points: {defect['points_count']}", self.styles['Normal']))
                
                if defect["type"] == "hole":
                    description = (
                        "A hole or gap was detected in the mesh. "
                    )
                elif defect["type"] == "noise":
                    description = (
                        "Noise points were detected in the model. "
                    )
                elif defect["type"] == "inconsistent_normals":
                    description = (
                        "Inconsistent surface normals were detected."
                    )
                else:
                    description = f"Defect of type '{defect['type']}' was detected."
                
                story.append(Paragraph(f"Description: {description}", self.styles['Normal']))
                story.append(Spacer(1, 15))
        else:
       
            story.append(Paragraph("No defects were detected in this model.", self.styles['Normal_Center']))
            story.append(Spacer(1, 10))
            if self.data["watertight"]:
                story.append(Paragraph("The model is watertight and appears to be suitable for 3D printing.", 
                                      self.styles['Normal_Center']))
        
        
        story.append(Spacer(1, 20))
       
        footer_text = f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Paragraph(footer_text, self.styles['Normal_Center']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer


def generate_report_from_json(json_data):
    
    generator = DefectReportGenerator(json_data)
    return generator.create_pdf()




