# yourapp/views.py
from django.http import HttpResponse
from django.views import View
from django.utils.encoding import escape_uri_path
from .resources import StudentResource
from django.shortcuts import render


class ExportRankingView(View):
    def get(self, request, *args, **kwargs):
        # Get the selected percentage from the request
        percentage = request.GET.get('percentage', 100)  # Default to 100% if not provided

        # Create a new StudentResource instance with the selected percentage
        student_resource = StudentResource()
        queryset = student_resource.apply_percentage_filter(student_resource.get_queryset(), float(percentage))

        # Generate the Excel file
        dataset = student_resource.export(queryset)
        response = HttpResponse(dataset.xlsx,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={escape_uri_path(f"ranking_{percentage}percent.xlsx")}'
        return response

def downloadpage(request):
    return render(request, 'DownloadPage/index.html')
