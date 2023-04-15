from api.resources.translations import trs
from django.utils.translation import get_language
from django.utils import translation

def tr(key: None | str | list[str] = '__all__', lang=get_language()):
	''' return dict or str '''
	if key is None:
		return {}
	translation.activate(lang)
	res = {}
	if key == '__all__':
		res = trs
	elif isinstance(key, list):
		keys = key.split(',')
		res = {k: v for k, v in trs.items() if k in keys}
	else:
		return trs.get(str(key), None)
	return res