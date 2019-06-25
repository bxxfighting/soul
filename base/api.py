import json
import traceback

from django.http import HttpResponse
from django.core.signing import TimestampSigner
from django.core.signing import SignatureExpired

from base import errors


class Api:
    NEED_LOGIN = True
    NEED_PERMISSION = True

    def __inif__(self, **opts):
        for k, v in opts.iteritems():
            setattr(self, k, v)

    def _get_token(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise errors.NoTokenError
        return token

    def _token2user_id(self, token):
        signer = TimestampSigner()
        try:
            # 如果加上max_age就可以控制登录有效时长
            user_id = signer.unsign(token, max_age=12*60*60)
            # user_id = signer.unsign(token)
        except SignatureExpired as e:
            raise errors.LoginExpireError
        return int(user_id)

    def _identification(self, request):
        token = self._get_token(request)
        self.user_id = self._token2user_id(token)

    def _permission(self, user_id, url):
        '''
        权限验证
        '''
        from account.controllers import is_permission
        if not is_permission(user_id, url):
            raise errors.CommonError('权限不足，无法进行此操作')

    def _pre_handle(self, request):
        '''
        请求处理前处理
        '''
        if self.NEED_LOGIN:
            self._identification(request)
        if self.NEED_PERMISSION:
            self._permission(self.user_id, request.path)

    def _after_handle(self):
        '''
        请求处理后处理
        '''
        pass

    def find_method(self, request):
        method = getattr(self, request.method, None)
        if not method:
            raise
        return method

    def __call__(self, request, *args, **kwargs):
        errno = 0
        errmsg = ''
        data = None
        try:
            self._pre_handle(request)
            method = self.find_method(request)
            data = method(request, *args, **kwargs)
            self._after_handle()
            if isinstance(data, HttpResponse):
                return data
        except errors.BaseError as e:
            errno = e.errno
            errmsg = e.errmsg
        except Exception as e:
            print(traceback.format_exc())
            errno = errors.BaseError.errno
            errmsg = errors.BaseError.errmsg
        data = {
            'errno': errno,
            'errmsg': errmsg,
            'data': data,
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
