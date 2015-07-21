import os
from tornkts.base.server_response import ServerError
from tornkts.handlers import BaseHandler
from tornkts.utils import FileHelper
from hashlib import md5
from datetime import datetime


class FileHandler(BaseHandler):
    @property
    def post_methods(self):
        return {
            'upload': self.upload
        }

    def upload(self):
        fields = self.request.files.keys()
        if len(fields) != 1:
            raise ServerError('bad_request')

        field_name = fields[0]
        file_request = self.request.files[field_name][0]

        file_body = file_request['body']
        file_body_hash = md5(md5(file_body).hexdigest() + md5(datetime.now().isoformat()).hexdigest()).hexdigest()

        file_ext = FileHelper.file_ext(file_request['filename'])
        if file_ext != '':
            file_name = '%s.%s' % (file_body_hash, file_ext)
        else:
            file_name = file_body_hash

        save_path_tree = '%s/%s/%s' % (file_body_hash[0:2], file_body_hash[2:4], file_body_hash[4:6])
        save_path = '%s%s' % (self.application.settings["file_save_path"], save_path_tree)

        save_full_file_name = '%s/%s' % (save_path, file_name)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_object = open(save_full_file_name, 'wb')
        file_object.write(file_body)
        file_object.close()

        self.send_success_response(data={
            'id': '%s/%s' % (save_path_tree, file_name),
            'url': '%s/%s/%s' % (self.application.settings["static_server_address"], save_path_tree, file_name)
        })