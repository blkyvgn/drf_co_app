from django.conf import settings

def get_json_by_key(val, key=None, default=None):
	lang_value = val.get(str(key), val.get(default, None))
	return lang_value

def set_json_by_key(val, v, key=None, default=None):
	_key = key if key is not None else default
	dict_val = {} if val is None else val.copy()
	dict_val[str(_key)] = v
	return dict_val