from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import api_restful

class TaskAPITestCase(APITestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Faz login e obtém o token de acesso JWT
        login_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json')

        # Verifica se o login foi bem-sucedido
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.access_token = login_response.data['access']

        # Adiciona o token JWT no cabeçalho de autenticação
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Dados de exemplo para criar uma tarefa
        self.task_data = {
            'title': 'Task Test',
            'description': 'Test Description',
            'date': '2024-09-15',
            'time': '10:00:00'
        }
        # Cria uma tarefa de exemplo no banco de dados para os testes de leitura, atualização e exclusão
        self.task = api_restful.objects.create(**self.task_data)

    def test_create_task(self):
        # Teste de criação de tarefa
        url = reverse('api_restful-list')  
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task(self):
        # Teste de leitura de uma tarefa específica
        url = reverse('api_restful-detail', args=[self.task.id])  
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        # Teste de atualização de uma tarefa
        url = reverse('api_restful-detail', args=[self.task.id])  
        updated_data = {'title': 'Updated Task'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_delete_task(self):
        # Teste de exclusão de uma tarefa
        url = reverse('api_restful-detail', args=[self.task.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(api_restful.objects.filter(id=self.task.id).exists())

