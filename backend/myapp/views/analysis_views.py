from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..models import DefectAnalysis
from ..serializers import DefectAnalysisSerializer


class DefectAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DefectAnalysis.objects.all()
    serializer_class = DefectAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        modelid = request.query_params.get('modelid')
        if modelid:
            queryset = self.queryset.filter(model_file__id=modelid, model_file__user=user)
            print(f"[USER] Filtering for own modelid: {modelid}")
        else:
            queryset = self.queryset.filter(model_file__user=user)
            print("[USER] Returning only own analysis")

        if not queryset.exists():
            return Response({"message": "No analysis found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
