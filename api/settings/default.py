
# DEFAULT 
NUMBER_PER_PAGE = 15
NUMBER_PAGINATIONS = 10

RATING_MAX = 10

IMAGE_EXTS = ['jpg','jpeg']
VIDEO_FILE_EXTS = ['mp4']

IMAGE_WIDTH = {
    'THUMBNAIL': 60,
    'SHOWCASE': 220,
    'SLIDER': 500,
    'LOGO': 170,
}

DEFAULT_IMAGE = {
    'PLACEHOLDER': 'company/images/default/placeholder.png',
    'LOGO':        'company/images/default/logo.png',
    'ICON':        'company/images/default/icon.png',
    'USER':        'company/images/default/user.png',
}
DEFAULT_IMAGE_KEY = list(DEFAULT_IMAGE)[0]

CACHE_TIMEOUT = {
    'YEAR':         60 * 60 * 24 * 364,
    'MONTH':        60 * 60 * 24 * 364,
    'DAY':          60 * 60 * 24 * 364,
    'FIVE_MINUTES': 60 * 60 * 5
}

COMPANY_ALIAS = 'grkr'
EMPTY_VALUE = '_'