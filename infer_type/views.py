import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .forms import JSONFileForm, FileForm
from .services import infer_types, change_types


from django.http import JsonResponse
import pandas as pd
@api_view(["POST", "OPTIONS"])
@permission_classes([AllowAny])
@csrf_exempt
@require_POST
def upload_csv(request):
    form = JSONFileForm(request.POST, request.FILES)

    if form.is_valid():
        csv_file = form.cleaned_data['file']
        json_file = form.cleaned_data['json_data']
        try:
            if json_file:
                result = change_types(csv_file, json_file)
            else:

                result = infer_types(csv_file)
        except Exception as e:
            raise e
        response = HttpResponse(result, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="output.csv"'

        # Allow requests from the React app's origin
        response["Access-Control-Allow-Origin"] = (
            "http://localhost:5173"  # Update with your React app's URL
        )
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response
    else:
        form = JSONFileForm()

    return render(request, "infer_type/upload_csv.html", {"form": form})
