import random
import string


class ArnheimGenerator(object):

    def __init__(self, model, group, overwrite = False):
        self.model = model
        self.group = group
        self.overwrite = overwrite
        self._name = None

        if self.group is None:
            raise NotImplementedError("Please specify a group")


    def _id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def build_name(self):
        return "test"

    @property
    def name(self):
        if self._name is None:
            if self.overwrite:
                self._name =  self.build_name()
            else:
                self._name =  self.build_name() + self._id_generator()
        return self._name

    @property
    def path(self):
        return f'{self.model.sample.id}-sample.{self.group}.{self.name}'


