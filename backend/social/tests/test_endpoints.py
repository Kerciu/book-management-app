from django.db.models import Q
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from social.models import FriendshipRequest, Friendship, Follow

User = get_user_model()


class FriendshipRequestEndpointTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='testpass1',
            first_name='User', last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='testpass2',
            first_name='User', last_name='Two'
        )
        self.client.force_authenticate(user=self.user1)

    def test_send_friend_request(self):
        url = reverse('friend-request-list')
        data = {'to_user': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_friend_requests(self):
        FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        url = reverse('friend-request-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_accept_friend_request(self):
        Friendship.objects.filter(
            (Q(user1=self.user1) & Q(user2=self.user2)) |
            (Q(user1=self.user2) & Q(user2=self.user1))
        ).delete()

        fr = FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user2)
        url = reverse('friend-request-accept', args=[fr.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fr.refresh_from_db()
        self.assertEqual(fr.status, 'accepted')

    def test_reject_friend_request(self):
        fr = FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user2)
        url = reverse('friend-request-reject', args=[fr.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fr.refresh_from_db()
        self.assertEqual(fr.status, 'rejected')

    def test_cancel_friend_request(self):
        fr = FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        url = reverse('friend-request-detail', args=[fr.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FriendshipRequest.objects.filter(id=fr.id).exists())


class FriendshipEndpointTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='testpass1',
            first_name='User', last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='testpass2',
            first_name='User', last_name='Two'
        )
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        self.client.force_authenticate(user=self.user1)

    def test_list_friendships(self):
        url = reverse('friendship-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class FollowEndpointTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='testpass1',
            first_name='User', last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='testpass2',
            first_name='User', last_name='Two'
        )
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        url = reverse('follow-list')
        data = {'followee': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_follows(self):
        Follow.objects.create(follower=self.user1, followee=self.user2)
        url = reverse('follow-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_unfollow_user(self):
        follow = Follow.objects.create(follower=self.user1, followee=self.user2)
        url = reverse('follow-detail', args=[follow.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.filter(id=follow.id).exists())
