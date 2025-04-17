from rest_framework import generics, permissions, serializers
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class AdListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProposalListCreateAPIView(generics.ListCreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Получаем ID объявления-отправителя
        sender_ad_id = self.request.data.get('ad_sender')

        # Проверяем, что оно действительно принадлежит текущему пользователю
        sender_ad = Ad.objects.filter(id=sender_ad_id, user=self.request.user).first()

        if not sender_ad:
            raise serializers.ValidationError("Вы не можете отправить предложение от чужого объявления.")

        serializer.save(ad_sender=sender_ad)
