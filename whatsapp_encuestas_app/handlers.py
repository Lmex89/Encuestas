
from .models import Codigo, Encuesta
from datetime import datetime

class ValidateCodigo(object):

    def run(self) -> int:

        get_all_codigos = Codigo.objects.filter(
            vigencia__lt=datetime.now()
        ).select_related(
            "encuesta"
        )
        get_all_encuestas= get_all_codigos.values_list('encuesta', flat=True)
        Encuesta.objects.filter(id__in=get_all_encuestas).update(visible=False)
        get_all_codigos.update(valido=False, visible=False)
        return get_all_codigos.update(valido=False, visible=False)



