from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import api_restful
from .serializers import api_Serializer
from .google_calendar import get_google_calendar_service

class api_restfulViewSet(viewsets.ModelViewSet):
    queryset = api_restful.objects.all()
    serializer_class = api_Serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Cria a tarefa no banco de dados
        task = serializer.save()
        # Cria o evento no Google Calendar
        self.create_google_calendar_event(task)

    def perform_destroy(self, instance):
        # Exclui o evento do Google Calendar se o ID estiver presente
        self.delete_google_calendar_event(instance)
        # Exclui a tarefa do banco de dados
        instance.delete()

    def create_google_calendar_event(self, task):
        service = get_google_calendar_service()
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': f'{task.date}T{task.time}',
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': f'{task.date}T{task.time}',
                'timeZone': 'America/Sao_Paulo',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        # Salva o ID do evento do Google Calendar no modelo da tarefa
        task.google_event_id = event.get('id')
        task.save()

    def delete_google_calendar_event(self, task):
        if task.google_event_id:
            service = get_google_calendar_service()
            try:
                service.events().delete(calendarId='primary', eventId=task.google_event_id).execute()
            except Exception as e:
                print(f'Erro ao excluir evento do Google Calendar: {e}')