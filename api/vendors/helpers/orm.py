from django.db.models import Aggregate
from django.db.models import CharField, Value as V


class GroupConcat(Aggregate):
	function = 'GROUP_CONCAT'
	template = '%(function)s(%(distinct)s%(expressions)s)'
	allow_distinct = True

	def __init__(self, expression, distinct=False, **extra):
		super(GroupConcat, self).__init__(
			expression,
			distinct='DISTINCT ' if distinct else '',
			output_field=CharField(),
			**extra
		)