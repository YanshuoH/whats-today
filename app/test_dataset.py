import datetime
from app import db, models

datasets = [
    {
        'social_id': 'user 1 social_id',
        'nickname': 'user 1 nickname',
        'email': 'user1@email.com',
        'words': [
            {
                'name': 'word 1 and for user 1',
                'explain': 'this is word 1 and for user 1',
                'example': 'some examples of word 1 and for user 1',
                'created_at': datetime.date.today(),
                'updated_at': datetime.date.today()
            },
            {
                'name': 'word 2 and for user 1',
                'explain': 'this is word 2 and for user 1',
                'example': 'some examples of word 2 and for user 1',
                'created_at': datetime.date.today() - datetime.timedelta(days=7),
                'updated_at': datetime.date.today()
            },
            {
                'name': 'word 3 and for user 1',
                'explain': 'this is word 3 and for user 1',
                'example': 'some examples of word 3 and for user 1',
                'created_at': datetime.date.today() - datetime.timedelta(days=14),
                'updated_at': datetime.date.today()
            },
        ]
    },
    {
        'social_id': 'user 2 social_id',
        'nickname': 'user 2 nickname',
        'email': 'user1@email.com',
        'words': [
            {
                'name': 'word 1 and for user 2',
                'explain': 'this is word 1 and for user 2',
                'example': 'some examples of word 1 and for user 2',
                'created_at': datetime.date.today(),
                'updated_at': datetime.date.today()
            },
            {
                'name': 'word 2 and for user 2',
                'explain': 'this is word 2 and for user 2',
                'example': 'some examples of word 2 and for user 2',
                'created_at': datetime.date.today() - datetime.timedelta(days=7),
                'updated_at': datetime.date.today()
            },
            {
                'name': 'word 3 and for user 2',
                'explain': 'this is word 3 and for user 2',
                'example': 'some examples of word 3 and for user 2',
                'created_at': datetime.date.today() - datetime.timedelta(days=14),
                'updated_at': datetime.date.today()
            },
        ]
    }
]
