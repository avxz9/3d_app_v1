from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse

from datetime import datetime

from ..models import DefectAnalysis
from ..report_generators.pdf_gen import generate_report_from_json
from ..report_generators.excel_gen import generate_excel_from_json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analysis_report(request, modelid):
    report_format = request.GET.get("report_format", "pdf").lower()

    analysis = DefectAnalysis.objects.filter(model_file__id=modelid).order_by('-created_at').first()

    if not analysis:
        return Response({"error": "No analysis found for this model."}, status=404)

    response_data = {
        "model_path": analysis.model_file.file_name,
        "defect_count": analysis.defect_count,
        "watertight": analysis.is_watertight,
        "defects": analysis.defect_data if isinstance(analysis.defect_data, list)
                   else analysis.defect_data.get("defects", []),
        "timestamp": datetime.utcnow().isoformat()
    }

    if report_format == "pdf":
        buffer = generate_report_from_json(response_data)
        content_type = "application/pdf"
        filename = f"analysis_report_{modelid}.pdf"

    elif report_format == "excel":
        buffer = generate_excel_from_json(response_data)
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"analysis_report_{modelid}.xlsx"

    else:
        return Response({"error": "Invalid format. Use 'pdf' or 'excel'."}, status=400)

    response = HttpResponse(buffer, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
