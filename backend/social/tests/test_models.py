from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import FriendshipRequest, Friendship, Follow

User = get_user_model()


class FriendshipModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='alice',
            email='alice@gmail.com',
            first_name='Alice',
            last_name='Smith',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='bob',
            email='bob@gmail.com',
            first_name='Bob',
            last_name='Johnson',
            password='pass123'
        )
        self.user3 = User.objects.create_user(
            username='carol',
            email='carol@gmail.com',
            first_name='Carol',
            last_name='Williams',
            password='pass123'
        )

    def test_create_friendship_request(self):
        req = FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.assertEqual(req.from_user, self.user1)
        self.assertEqual(req.to_user, self.user2)
        self.assertEqual(str(req), f"{self.user1.username} -> {self.user2.username}")

    def test_cannot_send_request_to_self(self):
        with self.assertRaises(ValidationError):
            FriendshipRequest.objects.create(
                from_user=self.user1, to_user=self.user1).full_clean()

    def test_cannot_duplicate_friendship_request(self):
        FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        with self.assertRaises(Exception):
            FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)

    def test_reverse_duplicate_request_is_allowed(self):
        FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)
        try:
            FriendshipRequest.objects.create(from_user=self.user2, to_user=self.user1)
        except Exception:
            self.fail("Reverse request should be allowed")

    def test_create_friendship(self):
        friendship = Friendship.objects.create(user1=self.user1, user2=self.user2)
        self.assertEqual(friendship.user1, self.user1)
        self.assertEqual(friendship.user2, self.user2)
        self.assertEqual(str(friendship),
                         f"{self.user1.username} - {self.user2.username}")

    def test_cannot_duplicate_friendship(self):
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        with self.assertRaises(Exception):
            Friendship.objects.create(user1=self.user1, user2=self.user2)

    def test_reverse_friendship_is_duplicate(self):
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        with self.assertRaises(Exception):
            Friendship.objects.create(user1=self.user2, user2=self.user1)

    def test_cannot_friend_self(self):
        with self.assertRaises(ValidationError):
            Friendship(user1=self.user1, user2=self.user1).full_clean()

    def test_get_friends_of_user(self):
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        Friendship.objects.create(user1=self.user1, user2=self.user3)

        user1_friends = (
            Friendship.objects.filter(user1=self.user1)
            | Friendship.objects.filter(user2=self.user1)
        )

        friend_ids = set()
        for f in user1_friends:
            friend_ids.add(f.user2.id if f.user1 == self.user1 else f.user1.id)

        self.assertIn(self.user2.id, friend_ids)
        self.assertIn(self.user3.id, friend_ids)
        self.assertNotIn(self.user1.id, friend_ids)


class FollowModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='dave',
            email='dave@gmail.com',
            first_name='Dave',
            last_name='Brown',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='eva',
            email='eva@gmail.com',
            first_name='Eva',
            last_name='Davis',
            password='pass123'
        )
        self.user3 = User.objects.create_user(
            username='frank',
            email='frank@gmail.com',
            first_name='Frank',
            last_name='Moore',
            password='pass123'
        )

    def test_create_follow(self):
        follow = Follow.objects.create(follower=self.user1, following=self.user2)
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
        self.assertEqual(str(follow),
                         f"{self.user1.username} follows {self.user2.username}")

    def test_cannot_follow_self(self):
        with self.assertRaises(ValidationError):
            Follow(follower=self.user1, following=self.user1).full_clean()

    def test_cannot_duplicate_follow(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.user1, following=self.user2)

    def test_different_users_can_follow_same_target(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        try:
            Follow.objects.create(follower=self.user3, following=self.user2)
        except Exception:
            self.fail("Different users should be allowed to follow the same target")

    def test_following_is_directional(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        try:
            Follow.objects.create(follower=self.user2, following=self.user1)
        except Exception:
            self.fail("Reverse follow should be allowed")
