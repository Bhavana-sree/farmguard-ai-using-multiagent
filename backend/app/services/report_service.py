from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
import os


class ReportService:
    def __init__(self):
        self.output_dir = "generated_reports"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf_report(self, report_data: dict) -> str:
        latitude = report_data.get("vision_analysis", {}).get("latitude", "unknown")
        longitude = report_data.get("vision_analysis", {}).get("longitude", "unknown")
        filename = f"farmguard_report_{latitude}_{longitude}.pdf".replace(" ", "_").replace("/", "_")
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Title"],
            fontSize=22,
            textColor=colors.HexColor("#2e7d32"),
            spaceAfter=10,
        )

        section_style = ParagraphStyle(
            "SectionStyle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#1b5e20"),
            spaceAfter=8,
            spaceBefore=12,
        )

        normal_style = ParagraphStyle(
            "NormalStyle",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
        )

        small_style = ParagraphStyle(
            "SmallStyle",
            parent=styles["BodyText"],
            fontSize=9,
            textColor=colors.grey,
        )

        # Header
        story.append(Paragraph("FarmGuard AI Carbon Credit Report", title_style))
        story.append(Paragraph("AI-powered farm carbon analysis and verification summary", small_style))
        story.append(Spacer(1, 0.2 * inch))

        # Summary box
        carbon = report_data.get("carbon_analysis", {})
        market = report_data.get("market_analysis", {})
        validation = report_data.get("validation_result", {})
        vision = report_data.get("vision_analysis", {})
        iot = report_data.get("iot_analysis", {})
        blockchain = report_data.get("blockchain_record", {})
        farmer = report_data.get("farmer_data", {})
        land = report_data.get("land_data", {})
        crop = report_data.get("crop_data", {})

        summary_data = [
            ["Carbon Credits", str(carbon.get("carbon_credits", "-"))],
            ["CO₂ Removed", f"{carbon.get('co2_kg', '-')} kg"],
            ["Market Value", f"${market.get('total_value_usd', '-')}"],
            ["Validation Status", str(validation.get("status", "-"))],
        ]

        summary_table = Table(summary_data, colWidths=[2.3 * inch, 3.5 * inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8f5e9")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.8, colors.HexColor("#a5d6a7")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.2 * inch))

        # Farmer details
        story.append(Paragraph("Farmer Details", section_style))
        farmer_data = [
            ["Name", str(farmer.get("fullName") or farmer.get("name") or "-")],
            ["Phone", str(farmer.get("phone", "-"))],
            ["Village", str(farmer.get("village", "-"))],
            ["District", str(farmer.get("district", "-"))],
            ["State", str(farmer.get("state", "-"))],
            ["Language", str(farmer.get("language", "-"))],
        ]
        farmer_table = Table(farmer_data, colWidths=[2.0 * inch, 3.8 * inch])
        farmer_table.setStyle(self._table_style())
        story.append(farmer_table)

        # Land details
        story.append(Paragraph("Land Details", section_style))
        land_data = [
            ["Survey Number", str(land.get("surveyNumber", "-"))],
            ["Land Type", str(land.get("landType", "-"))],
            ["Water Source", str(land.get("waterSource", "-"))],
            ["Soil Type", str(land.get("soilType", "-"))],
            ["Area", f"{land.get('areaAcres', '-')} acres"],
            ["Latitude", str(vision.get("latitude", land.get("latitude", "-")))],
            ["Longitude", str(vision.get("longitude", land.get("longitude", "-")))],
        ]
        land_table = Table(land_data, colWidths=[2.0 * inch, 3.8 * inch])
        land_table.setStyle(self._table_style())
        story.append(land_table)

        # AI analysis
        story.append(Paragraph("AI Analysis", section_style))
        analysis_data = [
            ["NDVI", str(vision.get("ndvi", "-"))],
            ["Tree Density", str(vision.get("tree_density", "-"))],
            ["Estimated Trees", str(vision.get("estimated_trees", "-"))],
            ["Biomass", f"{carbon.get('biomass_kg', '-')} kg"],
            ["Carbon", f"{carbon.get('carbon_kg', '-')} kg"],
            ["CO₂", f"{carbon.get('co2_kg', '-')} kg"],
        ]
        analysis_table = Table(analysis_data, colWidths=[2.0 * inch, 3.8 * inch])
        analysis_table.setStyle(self._table_style())
        story.append(analysis_table)

        # IoT section
        if iot:
            story.append(Paragraph("IoT Monitoring", section_style))
            iot_data = [
                ["Soil Moisture", f"{iot.get('soil_moisture_percent', '-')} %"],
                ["Temperature", f"{iot.get('temperature_c', '-')} °C"],
                ["Humidity", f"{iot.get('humidity_percent', '-')} %"],
                ["Soil pH", str(iot.get("soil_ph", "-"))],
                ["Light Intensity", f"{iot.get('light_intensity_lux', '-')} lux"],
                ["Irrigation Status", str(iot.get("irrigation_status", "-"))],
                ["Crop Stress", str(iot.get("crop_stress", "-"))],
            ]
            iot_table = Table(iot_data, colWidths=[2.0 * inch, 3.8 * inch])
            iot_table.setStyle(self._table_style())
            story.append(iot_table)

        # Tree list
        story.append(Paragraph("Selected Trees / Manual Crop Input", section_style))
        selected_trees = crop.get("selectedTrees", {})
        if selected_trees:
            tree_rows = [["Tree Name", "Count"]]
            for tree_name, count in selected_trees.items():
                tree_rows.append([str(tree_name), str(count)])

            tree_table = Table(tree_rows, colWidths=[3.5 * inch, 1.5 * inch])
            tree_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.8, colors.HexColor("#cfd8dc")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]))
            story.append(tree_table)
        else:
            story.append(Paragraph("No manual tree input available.", normal_style))

        # Verification
        story.append(Paragraph("Verification Result", section_style))
        story.append(Paragraph(
            f"<b>Status:</b> {validation.get('status', '-')}",
            normal_style
        ))
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph(
            f"<b>Reason:</b> {validation.get('reason', '-')}",
            normal_style
        ))

        # Blockchain
        story.append(Paragraph("Blockchain Record", section_style))
        story.append(Paragraph(
            f"<b>Status:</b> {blockchain.get('status', '-')}",
            normal_style
        ))
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph(
            f"<b>Hash:</b> {blockchain.get('block_hash', '-')}",
            normal_style
        ))

        # Market
        story.append(Paragraph("Market Readiness", section_style))
        story.append(Paragraph(
            f"<b>Buyer Type:</b> {market.get('buyer_type', '-')}",
            normal_style
        ))
        story.append(Spacer(1, 0.05 * inch))
        story.append(Paragraph(
            f"<b>Market Status:</b> {market.get('market_status', '-')}",
            normal_style
        ))

        # Footer
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(
            "Generated by FarmGuard AI using satellite analysis, carbon estimation, IoT monitoring, validation, and blockchain logging.",
            small_style
        ))

        doc.build(story)
        return filepath

    def _table_style(self):
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.8, colors.HexColor("#cfd8dc")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])