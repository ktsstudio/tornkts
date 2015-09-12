import os
from tornkts.base.server_response import ServerError
from tornkts.handlers import BaseHandler
from tornkts.utils import FileHelper
from hashlib import md5
from datetime import datetime


def get_file_pathes(file_request, file_save_path):
    file_body = file_request['body']
    file_body_hash = md5(md5(file_body).hexdigest() + md5(datetime.now().isoformat()).hexdigest()).hexdigest()

    file_ext = FileHelper.file_ext(file_request['filename'])
    if file_ext != '':
        file_name = '%s.%s' % (file_body_hash, file_ext)
    else:
        file_name = file_body_hash

    save_path_tree = '%s/%s/%s' % (file_body_hash[0:2], file_body_hash[2:4], file_body_hash[4:6])
    save_path = '%s%s' % (file_save_path, save_path_tree)

    save_full_file_name = '%s/%s' % (save_path, file_name)
    return save_path, save_path_tree, save_full_file_name, file_name, file_body


def save_file(file_request, file_save_path):
    save_path, save_path_tree, \
    save_full_file_name, file_name, \
    file_body = get_file_pathes(file_request, file_save_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_object = open(save_full_file_name, 'wb')
    file_object.write(file_body)
    file_object.close()

    return save_path_tree, file_name


class FileHandler(BaseHandler):

    @property
    def allowed_extensions(self):
        return []

    def check_request(self):
        return True

    @property
    def post_methods(self):
        return {
            'upload': self.upload
        }

    def make_result(self, id, url):
        self.save_to_db(id, url)
        self.send_success_response(data={
            "id": id,
            'url': url
        })

    def save_to_db(self, id, url):
        pass

    @property
    def file_save_path(self):
        return self.application.settings['file_save_path']

    @property
    def statis_server_address(self):
        return self.application.settings["static_server_address"]


    def upload(self):
        self.check_request()

        fields = self.request.files.keys()
        if len(fields) != 1:
            raise ServerError('bad_request')

        field_name = fields[0]
        file_request = self.request.files[field_name][0]

        file_ext = FileHelper.file_ext(file_request['filename'])
        if len(self.allowed_extensions) > 0 and file_ext not in self.allowed_extensions:
            raise ServerError('bad_request', data="incorrect_file_extension")

        save_path_tree, file_name = save_file(file_request, self.file_save_path)

        self.make_result(
            '%s/%s' % (save_path_tree, file_name),
            '%s/%s/%s' % (self.statis_server_address, save_path_tree, file_name)
        )
