from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Presentation
from events.api_views import ConferenceListEncoder
from django.views.decorators.http import require_http_methods
import json


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder
    }

    def get_extra_data(self, o):
        return {"status": o.status.name}


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.filter(conference=conference_id)
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationDetailEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            presentations = Presentation.objects.get(id=content["presentations"])
            content["presentations"] = presentations
        except Presentation.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid presentation id"},
                status=400,
            )
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            presentations = Presentation.objects.get(id=content["presentations"])
            content["presentations"] = presentations
        except Presentation.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid presentation id"},
                status=400,
            )

        presentation = Presentation.update(**content)

        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
