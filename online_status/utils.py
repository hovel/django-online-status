from online_status.status import OnlineStatus


def encode_json(obj):
    if isinstance(obj, OnlineStatus):
        seen = obj.seen.isoformat()
        # TODO adapt to custom user model
        user = {
            'username': obj.user.get_username(),
            'first_name': getattr(obj.user, 'first_name', ''),
            'last_name': getattr(obj.user, 'last_name', ''),
        }
        return {'user': user, 'seen': seen, 'status': obj.status, }
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")
