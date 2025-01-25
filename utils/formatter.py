import uuid

def create_uuid(input_string):
    namespace = uuid.NAMESPACE_DNS
    return uuid.uuid5(namespace, input_string)

