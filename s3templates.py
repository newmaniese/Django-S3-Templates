from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from boto.s3.connection import S3Connection 

ACCESS_KEY_NAME = getattr(settings, 'AWS_S3_ACCESS_KEY_ID', getattr(settings, 'AWS_ACCESS_KEY_ID', None))
SECRET_KEY_NAME = getattr(settings, 'AWS_S3_SECRET_ACCESS_KEY', getattr(settings, 'AWS_SECRET_ACCESS_KEY', None))
TEMPLATE_BUCKET = getattr(settings, 'AWS_TEMPLATE_BUCKET')


class Loader(BaseLoader):
    is_usable = True

    def __init__(self, *args, **kwargs):
        conn = S3Connection(ACCESS_KEY_NAME, SECRET_KEY_NAME)
        self.bucket = conn.get_bucket(TEMPLATE_BUCKET)
        return super(Loader, self).__init__(*args, **kwargs)

    def get_template_keys(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS
        for template_dir in template_dirs:
            if template_dir.endswith("/"):
                template_dir = template_dir[:-1]
            yield "/".join([template_dir, template_name])

    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        for key in self.get_template_keys(template_name, template_dirs):
            print key
            template_key = self.bucket.get_key(key)
            
            if template_key:
                return (template_key.read().decode(settings.FILE_CHARSET), key)
            
            tried.append(key)
        if tried:
            error_msg = "Tried Keys %s" % tried
        else:
            error_msg = "Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory."
        raise TemplateDoesNotExist(error_msg)
    load_template_source.is_usable = True        