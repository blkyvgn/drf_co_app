

def get_filter_arguments(request):
	exclude = ['page', 'alias']
	arguments = {}
	if request.query_params:
		arguments = {key: val for key, val in request.query_params.items() if key not in exclude}
	return arguments