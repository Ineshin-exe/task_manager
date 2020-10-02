import json

from datetime import date, datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Task, ChangeLogTask
from api.serializers import TaskSerializer, ChangeLogTaskSerializer


class TaskSerializerTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test',
                                       password='zxcv1223')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=1,
                                       title='test1',
                                       description='create',
                                       createdAt=datetime.utcnow(),
                                       deadline='2020-10-30',
                                       status='Planned')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=2,
                                       title='test2',
                                       description='create',
                                       createdAt=datetime.utcnow(),
                                       deadline='2020-10-29',
                                       status='Planned')

    def test_task_serializer(self):

        expected = [
        {
            "owner": "test",
            "id": 1,
            "title": "test1",
            "description": "create",
            "createdAt": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "deadline": "2020-10-30",
            "status": "Planned"
        },
        {
            "owner": "test",
            "id": 2,
            "title": "test2",
            "description": "create",
            "createdAt": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "deadline": "2020-10-29",
            "status": "Planned"
        }]

        serialized = TaskSerializer(Task.objects.all(), many=True).data
        self.assertEqual(serialized, expected)


class ChangeLogTaskSerializerTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test',
                                       password='zxcv1223')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=1,
                                       title='test1',
                                       description='create',
                                       createdAt=datetime.utcnow(),
                                       deadline='2020-10-30',
                                       status='Planned')

    def test_changelog_serializer(self):

        expected = [
            {
                "id": 1,
                "changeTime": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                "data": {
                    "title": "test1",
                    "description": "create",
                    "deadline": "2020-10-30",
                    "status": "Planned"
                },
                "task": 1
            }
        ]

        serialized = ChangeLogTaskSerializer(ChangeLogTask.objects.filter(task__id=1), many=True).data
        print(serialized)
        self.assertEqual(serialized, expected)


class CreateTaskTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test',
                                       password='zxcv1223')

        cls.key = Token.objects.create(user=User.objects.get(username='test'))
        cls.token = cls.key.key

    def test_create_task(self):
        url = reverse('create')
        data = {
            "title": "test",
            "description": "create",
            "deadline": "2020-10-30",
            "status": "Planned"
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().owner, User.objects.get())
        self.assertEqual(Task.objects.get().title, 'test')
        self.assertEqual(Task.objects.get().description, 'create')
        self.assertEqual(Task.objects.get().createdAt.strftime('%Y-%m-%d %H:%M:%S'),
                         datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(Task.objects.get().deadline, date.fromisoformat('2020-10-30'))
        self.assertEqual(Task.objects.get().status, 'Planned')

    def test_create_deadline_only(self):
        url = reverse('create')
        data = {
            "deadline": "2020-12-31",
        }
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().owner, User.objects.get())
        self.assertEqual(Task.objects.get().title, 'Undefined')
        self.assertEqual(Task.objects.get().description, 'No description.')
        self.assertEqual(Task.objects.get().createdAt.strftime('%Y-%m-%d %H:%M:%S'),
                         datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(Task.objects.get().deadline, date.fromisoformat('2020-12-31'))
        self.assertEqual(Task.objects.get().status, 'New')

    def test_create_empty(self):
        url = reverse('create')
        data = {}
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().owner, User.objects.get())
        self.assertEqual(Task.objects.get().title, 'Undefined')
        self.assertEqual(Task.objects.get().description, 'No description.')
        self.assertEqual(Task.objects.get().createdAt.strftime('%Y-%m-%d %H:%M:%S'),
                         datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(Task.objects.get().deadline, None)
        self.assertEqual(Task.objects.get().status, 'New')


class ListTaskTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test',
                                       password='zxcv1223')

        cls.key = Token.objects.create(user=User.objects.get(username='test'))
        cls.token = cls.key.key

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=1,
                                       title='test1',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-30',
                                       status='Planned')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=2,
                                       title='test2',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-29',
                                       status='Planned')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=3,
                                       title='test3',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-30',
                                       status='New')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=4,
                                       title='test4',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-29',
                                       status='New')

    def test_list_task(self):
        url = reverse('read')

        expected = TaskSerializer(Task.objects.all(), many=True).data

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_filter_status_list_task(self):
        url = reverse('read')

        expected = TaskSerializer(Task.objects.filter(status='Planned'), many=True).data

        response = self.client.get("{}?status=Planned".format(url), format='json',
                                   HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_filter_deadline_list_task(self):
        url = reverse('read')

        expected = TaskSerializer(Task.objects.filter(deadline='2020-10-29'), many=True).data

        response = self.client.get("{}?deadline=2020-10-29".format(url), format='json',
                                   HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_filter_deadline_status_list_task(self):
        url = reverse('read')

        expected = TaskSerializer(Task.objects.filter(deadline='2020-10-30', status='New'), many=True).data

        response = self.client.get("{}?deadline=2020-10-30&status=New".format(url), format='json',
                                   HTTP_AUTHORIZATION='Token {}'.format(self.token))

        print(expected)
        print(json.loads(response.content))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_filter_not_exists_list_task(self):
        url = reverse('read')

        print(datetime.today().isoformat(' ', 'seconds'))

        expected = {
            "message": "filter 'title' is not supported"
        }

        response = self.client.get("{}?title=test3".format(url), format='json',
                                   HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected)


class OneTaskTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test',
                                       password='zxcv1223')

        cls.key = Token.objects.create(user=User.objects.get(username='test'))
        cls.token = cls.key.key

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=1,
                                       title='test1',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-30',
                                       status='Planned')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=2,
                                       title='test2',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-29',
                                       status='Planned')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=3,
                                       title='test3',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-30',
                                       status='New')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=4,
                                       title='test4',
                                       description='create',
                                       createdAt=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                       deadline='2020-10-29',
                                       status='New')

    def test_one_exist_task(self):
        url = reverse('item', args=('1'))

        expected = TaskSerializer(Task.objects.filter(id=1).first()).data

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_one_not_exist_task(self):
        url = reverse('item', args=("9"))

        expected = {
            "message": "Task does not exist"
        }

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), expected)

    def test_nothing_update_task(self):
        url = reverse('item', args=('1'))

        expected = {'message': 'No data to update'}

        response = self.client.patch(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), expected)

    def test_title_update_task(self):
        url = reverse('item', args=('4'))

        data = {
            "title": "updated"
        }

        task = Task.objects.filter(id=4).first()
        task.title = 'updated'
        task.save()

        expected = TaskSerializer(task).data

        response_update = self.client.patch(url, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_delete_task(self):
        url = reverse('item', args=('4'))

        expected = {
            "message": "Task was deleted successfully!"
        }

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        task = Task.objects.filter(id=4).exists()

        self.assertFalse(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), expected)

    def test_delete_not_exist_task(self):
        url = reverse('item', args=('9'))

        expected = {
            "message": "Task does not exist"
        }

        response = self.client.delete(url, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), expected)


class ChangeLogTaskTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test',
                                       password='zxcv1223')
        cls.key = Token.objects.create(user=User.objects.get(username='test'))
        cls.token = cls.key.key

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=1,
                                       title='test1',
                                       description='create',
                                       createdAt=datetime.utcnow(),
                                       deadline='2020-10-30',
                                       status='Planned')

        cls.data = Task.objects.create(owner=User.objects.get(username='test'),
                                       id=2,
                                       title='test2',
                                       description='create',
                                       createdAt=datetime.utcnow(),
                                       deadline='2020-10-29',
                                       status='Planned')

    def test_check_changelog_task(self):
        url_task = reverse('item', args=('1'))
        url_changelog = reverse('changelog', args=('1'))

        data = {
            "title": "updated"
        }

        task = Task.objects.filter(id=1).first()
        task.title = 'updated'
        task.save()

        expected_task = TaskSerializer(task).data

        response_update = self.client.patch(url_task, data, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response_task = self.client.get(url_task, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response_changelog = self.client.get(url_changelog, format='json', HTTP_AUTHORIZATION='Token {}'.format(self.token))

        expected_log = ChangeLogTaskSerializer(ChangeLogTask.objects.filter(task=task), many=True).data

        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_task.status_code, status.HTTP_200_OK)
        self.assertEqual(response_changelog.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response_update.content), expected_task)
        self.assertEqual(json.loads(response_task.content), expected_task)
        self.assertEqual(json.loads(response_changelog.content), expected_log)

