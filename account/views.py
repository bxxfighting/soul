import ujson as json

from django.db import transaction

from base.api import Api
from . import controllers as account_ctl


class LoginView(Api):
    NEED_LOGIN = False
    NEED_PERMISSION = False

    def POST(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = account_ctl.login(username, password)
        token = account_ctl.gen_token(user.id)
        mod_list = account_ctl.get_mod_list_by_user_id(user.id)
        data = {
            'token': token,
            'mod_list': mod_list,
        }
        return data


class ListUserModView(Api):
    '''
    获取用户可见模块列表
    '''
    NEED_PERMISSION = False
    def POST(self, request):
        data = account_ctl.get_mod_list_by_user_id(self.user_id)
        return data


class ListUserView(Api):
    '''
    获取全部用户列表
    '''
    def POST(self, request):
        data = json.loads(request.body)
        page_num = data.get('page_num')
        page_size = data.get('page_size')
        data = account_ctl.get_user_list(page_num, page_size)
        return data


class ListRoleView(Api):
    '''
    获取全部角色列表
    '''
    def POST(self, request):
        data = json.loads(request.body)
        page_num = data.get('page_num')
        page_size = data.get('page_size')
        data = account_ctl.get_role_list(page_num, page_size)
        return data


class ListModView(Api):
    '''
    获取全部模块列表
    '''
    def POST(self, request):
        data = json.loads(request.body)
        page_num = data.get('page_num')
        page_size = data.get('page_size')
        data = account_ctl.get_mod_list(page_num, page_size)
        return data


class CreateRoleView(Api):
    '''
    创建角色
    '''
    def POST(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        sign = data.get('sign')
        mod_ids = data.get('mod_ids')
        with transaction.atomic():
            role = account_ctl.create_role(name, sign)
            account_ctl.set_role_mods(role.id, mod_ids)
            data = role.to_dict()
        return data


class UpdateRoleView(Api):
    '''
    编辑角色
    '''
    def POST(self, request):
        data = json.loads(request.body)
        role_id = data.get('id')
        name = data.get('name')
        sign = data.get('sign')
        mod_ids = data.get('mod_ids')
        with transaction.atomic():
            role = account_ctl.update_role(role_id, name, sign)
            account_ctl.set_role_mods(role.id, mod_ids)
        data = role.to_dict()
        return data


class DeleteRoleView(Api):
    '''
    删除角色
    '''
    def POST(self, request):
        data = json.loads(request.body)
        role_id = data.get('id')
        account_ctl.delete_role(role_id)


class SetRoleModsView(Api):
    '''
    角色关联模块
    '''
    def POST(self, request):
        data = json.loads(request.body)
        role_id = data.get('id')
        mod_ids = data.get('mod_ids')
        data = {
            'role_id': role_id,
            'mod_ids': mod_ids,
        }
        account_ctl.set_role_mods(**data)


class CreateModView(Api):
    '''
    创建模块
    '''
    def POST(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        sign = data.get('sign')
        rank = data.get('rank')
        url_ids = data.get('url_ids')
        with transaction.atomic():
            obj = account_ctl.create_mod(name, sign, rank)
            account_ctl.set_mod_urls(obj.id, url_ids)
            data = obj.to_dict()
        return data


class UpdateModView(Api):
    '''
    编辑模块
    '''
    def POST(self, request):
        data = json.loads(request.body)
        mod_id = data.get('id')
        name = data.get('name')
        sign = data.get('sign')
        rank = data.get('rank')
        url_ids = data.get('url_ids')
        with transaction.atomic():
            obj = account_ctl.update_mod(mod_id, name, sign, rank)
            account_ctl.set_mod_urls(obj.id, url_ids)
            data = obj.to_dict()
        return data


class DeleteModView(Api):
    '''
    删除模块
    '''
    def POST(self, request):
        data = json.loads(request.body)
        mod_id = data.get('id')
        account_ctl.delete_mod(mod_id)


class CreateUserView(Api):
    '''
    创建用户
    '''
    def POST(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        role_ids = data.get('role_ids')
        data = {
            'username': username,
            'password': password,
            'name': name,
            'phone': phone,
            'email': email,
        }
        with transaction.atomic():
            obj = account_ctl.create_user(**data)
            account_ctl.set_user_roles(obj.id, role_ids)
            data = obj.to_dict()
        return data


class UpdateUserView(Api):
    '''
    编辑用户
    '''
    def POST(self, request):
        data = json.loads(request.body)
        user_id = data.get('id')
        name = data.get('name')
        password = data.get('password')
        phone = data.get('phone')
        email = data.get('email')
        role_ids = data.get('role_ids')
        data = {
            'user_id': user_id,
            'name': name,
            'password': password,
            'phone': phone,
            'email': email,
        }
        with transaction.atomic():
            obj = account_ctl.update_user(**data)
            account_ctl.set_user_roles(obj.id, role_ids)
            data = obj.to_dict()
        return data


class DeleteUserView(Api):
    '''
    删除用户
    '''
    def POST(self, request):
        data = json.loads(request.body)
        user_id = data.get('id')
        account_ctl.delete_user(user_id)


class ChangePasswordView(Api):
    '''
    修改密码
    用于修改自己的密码
    '''
    NEED_PERMISSION = False
    def POST(self, request):
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        data = {
            'user_id': self.user_id,
            'old_password': old_password,
            'new_password': new_password,
        }
        account_ctl.change_password(**data)


class ListUrlView(Api):
    '''
    获取全部URL列表
    '''
    def POST(self, request):
        data = json.loads(request.body)
        page_num = data.get('page_num')
        page_size = data.get('page_size')
        data = account_ctl.get_url_list(page_num, page_size)
        return data


class CreateUrlView(Api):
    '''
    创建URL
    '''
    def POST(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        url = data.get('url')
        obj = account_ctl.create_url(name, url)
        data = obj.to_dict()
        return data


class UpdateUrlView(Api):
    '''
    编辑URL
    '''
    def POST(self, request):
        data = json.loads(request.body)
        obj_id = data.get('id')
        name = data.get('name')
        url = data.get('url')
        obj = account_ctl.update_url(obj_id, name, url)
        data = obj.to_dict()
        return data


class DeleteUrlView(Api):
    '''
    删除URL
    '''
    def POST(self, request):
        data = json.loads(request.body)
        obj_id = data.get('id')
        account_ctl.delete_url(obj_id)
