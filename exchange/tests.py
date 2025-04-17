from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal
from rest_framework.test import APIClient
from rest_framework import status


class ExchangeTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Пользователи
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # Объявления
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Телефон',
            description='Обмен на ноут',
            category='Электроника',
            condition='new'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Наушники',
            description='Отличные наушники',
            category='Аудио',
            condition='used'
        )

    def test_create_ad(self):
        self.assertEqual(Ad.objects.count(), 2)
        self.assertEqual(self.ad1.user.username, 'user1')

    def test_create_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Обменяю'
        )
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_sender, self.ad1)

    def test_api_ads_list(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get('/api/ads/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_api_create_proposal_success(self):
        self.client.login(username='user1', password='pass123')
        data = {
            'comment': 'Хочу обмен',
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id
        }
        response = self.client.post('/api/proposals/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_api_create_proposal_fail_with_foreign_sender(self):
        self.client.login(username='user2', password='pass123')
        data = {
            'comment': 'Нельзя от чужого объявления',
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id
        }
        response = self.client.post('/api/proposals/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Вы не можете отправить", str(response.data))
