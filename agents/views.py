from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ResearchProject
from .services.runner import run_product_research


class ProductResearchAgentView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        asin  = request.data.get('asin', '').strip()
        niche = request.data.get('niche', '').strip()
        file  = request.FILES.get('helium_file')

        if not asin or not niche:
            return Response(
                {'error': 'asin and niche are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        project = ResearchProject.objects.create(
            asin=asin,
            niche=niche,
            uploaded_file=file,
        )

        try:
            result = run_product_research(project)
            return Response({
                'project_id': project.id,
                'status': 'complete',
                'result': result,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'project_id': project.id,
                'status': 'failed',
                'error': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk=None):
        if pk:
            try:
                project = ResearchProject.objects.get(pk=pk)
                return Response({
                    'project_id': project.id,
                    'asin': project.asin,
                    'niche': project.niche,
                    'status': project.status,
                    'result': project.result,
                    'created_at': project.created_at,
                })
            except ResearchProject.DoesNotExist:
                return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        projects = ResearchProject.objects.all().values(
            'id', 'asin', 'niche', 'status', 'created_at', 'uploaded_file'
        )
        return Response(list(projects))
