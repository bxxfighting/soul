DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'PORT': 3306,
        'NAME': 'soul',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
