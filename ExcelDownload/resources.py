# yourapp/resources.py
from import_export import resources
from .models import Student

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('id', 'schoolClass', 'className', 'schoolClassChinese', 'seatNumber', 'studentID', 'name', 'identityCard', 'sex', 'birth_date')
        order_by = ('studentID',)

    # Add a method to filter data based on the selected percentage range
    def apply_percentage_filter(self, queryset, percentage):
        queryset.order_by('studentID')
        total_students = queryset.count()
        selected_count = int((percentage / 100) * total_students)+1
        return queryset[:selected_count]


    def get_export_queryset(self, request, *args, **kwargs):
        queryset = super().get_export_queryset(request, *args, **kwargs)

        # Get the selected percentage from the request
        percentage = request.GET.get('percentage', 100)  # Default to 100% if not provided

        # Apply the percentage filter
        queryset = self.apply_percentage_filter(queryset, float(percentage))

        return queryset

    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = self.get_export_queryset()
        return super().export(queryset=queryset, *args, **kwargs)
