"""Fields used by public section components. Hidden legacy values stay intact."""


def fields(names):
    return set(names.split())


BUTTON = 'primary_button_text primary_button_url'
BUTTONS = BUTTON + ' secondary_button_text secondary_button_url'
COURSE_HEADINGS = 'super_heading heading highlighted_heading subheading'

SECTION_FIELDS = {
    'homepage': {
        'HERO': fields('super_heading heading subheading background_image ' + BUTTONS),
        'PARTNERS': fields('heading subheading'),
        'OVERVIEW': fields('super_heading heading overview_text primary_image background_image ' + BUTTONS),
        'WHY_CHOOSE_US': fields('super_heading heading subheading primary_image background_image'),
        'OUR_SERVICES': fields('super_heading heading subheading'),
        'OUR_PLACED_STUDENTS': fields('heading subheading'),
        'TESTIMONIALS': fields('heading subheading'),
        'FAQ': fields('heading subheading'),
        'CONTACT_US': fields('super_heading heading subheading overview_text'),
        'CTA': fields('super_heading heading subheading overview_text ' + BUTTON),
    },
    'aboutus': {
        'HERO': fields('super_heading heading subheading background_image primary_image ' + BUTTON),
        'WHO_WE_ARE': fields('super_heading heading subheading overview_text primary_image'),
        'DIRECTOR_MESSAGE': fields('super_heading heading subheading overview_text primary_image ' + BUTTON),
        'OUR_STORY': fields('super_heading heading subheading'),
        'VISION_MISSION': fields('heading'),
        'EXPERTISE': fields('super_heading heading subheading overview_text'),
        'ACCREDITATIONS': fields('super_heading heading subheading overview_text'),
        'INFRASTRUCTURE': fields('super_heading heading subheading primary_image'),
        'GALLERY': fields('super_heading heading subheading overview_text primary_image'),
        'OUR_TEAM': fields('super_heading heading subheading overview_text'),
    },
    'modules': {
        'HERO': fields('heading highlighted_heading subheading background_image primary_image overlay_title overlay_description ' + BUTTONS),
        'MODULE_OPPORTUNITIES': fields('heading subheading'),
        'WHY_CHOOSE_US': fields(COURSE_HEADINGS),
        'FEATURE_HIGHLIGHTS': fields('heading subheading ' + BUTTONS),
        'PROGRAM_STRUCTURE': fields('heading subheading primary_image overlay_description'),
        'FAQ': fields('heading subheading'),
        'PAGE_BANNER': fields(COURSE_HEADINGS + ' background_image ' + BUTTON + ' secondary_button_text'),
        'COURSE_OVERVIEW': fields(COURSE_HEADINGS + ' primary_image overlay_title overlay_description'),
        'KEY_HIGHLIGHTS': fields(COURSE_HEADINGS),
        'SUBJECTS_COVERED': fields(COURSE_HEADINGS),
        'ELIGIBILITY_CRITERIA': fields(COURSE_HEADINGS + ' primary_image'),
        'FEES_BATCH_DETAILS': fields(COURSE_HEADINGS + ' ' + BUTTON),
        'FACULTY': fields(COURSE_HEADINGS),
        'PAST_RESULTS': fields(COURSE_HEADINGS + ' primary_image'),
        'TESTIMONIALS': fields(COURSE_HEADINGS),
        'CTA': fields('super_heading heading subheading background_image primary_image overlay_title overlay_description ' + BUTTONS),
    },
}

ITEM_FIELDS = {
    'homepage': {
        'HERO': fields('icon label title'), 'PARTNERS': fields('title icon description'),
        'OVERVIEW': fields('text'), 'WHY_CHOOSE_US': fields('title description icon'),
        'OUR_SERVICES': fields('title description icon label question text'),
        'OUR_PLACED_STUDENTS': fields('title icon'),
        'TESTIMONIALS': fields('title description icon question answer'),
        'FAQ': fields('question answer'), 'CONTACT_US': fields('label title description icon'),
        'CTA': set(),
    },
    'aboutus': {
        'HERO': fields('image'), 'WHO_WE_ARE': fields('label title description text'),
        'DIRECTOR_MESSAGE': fields('person_name person_role label title description text'),
        'OUR_STORY': fields('label title description image'),
        'VISION_MISSION': fields('label description image'),
        'EXPERTISE': fields('label title description image ' + BUTTON),
        'ACCREDITATIONS': fields('label title description image'),
        'INFRASTRUCTURE': fields('label title description image'),
        'GALLERY': fields('image label'),
        'OUR_TEAM': fields('person_name person_role image description label title linkedin_url twitter_url facebook_url'),
    },
    'modules': {
        'HERO': fields('icon label'),
        'MODULE_OPPORTUNITIES': fields('icon title description ' + BUTTON),
        'WHY_CHOOSE_US': fields('icon title description tags'),
        'FEATURE_HIGHLIGHTS': fields('icon title description tags'),
        'PROGRAM_STRUCTURE': fields('icon label title description tags'),
        'FAQ': fields('question answer'), 'PAGE_BANNER': fields('icon title'),
        'COURSE_OVERVIEW': fields('title description'),
        'KEY_HIGHLIGHTS': fields('icon label title description tags'),
        'SUBJECTS_COVERED': fields('icon title description tags'),
        'ELIGIBILITY_CRITERIA': fields('title description'),
        'FEES_BATCH_DETAILS': fields('icon label title description'),
        'FACULTY': fields('icon title label description tags primary_button_url'),
        'PAST_RESULTS': fields('icon label title description'),
        'TESTIMONIALS': fields('icon title description question answer'), 'CTA': set(),
    },
}

# Contextual labels for fields whose legacy database names are less descriptive.
ITEM_LABELS = {
    'homepage': {
        'PARTNERS': {'title': 'Partner name', 'icon': 'Partner logo'},
        'OUR_PLACED_STUDENTS': {'title': 'Student name', 'icon': 'Student photo'},
        'OUR_SERVICES': {'question': 'Course page URL', 'text': 'Alternative course page URL', 'icon': 'Course image'},
        'OVERVIEW': {'text': 'Highlight text'},
    },
    'aboutus': {
        'GALLERY': {'label': 'Image caption'},
        'HERO': {'image': 'Banner slide image'},
        'VISION_MISSION': {'label': 'Tab heading'},
        'OUR_TEAM': {'label': 'Display name', 'title': 'Role / expertise', 'facebook_url': 'Website URL'},
    },
    'modules': {
        'FACULTY': {'title': 'Faculty name', 'label': 'Role', 'icon': 'Faculty photo', 'primary_button_url': 'Profile URL'},
    },
}


def policy(model):
    app, name = model._meta.app_label, model._meta.model_name
    if name == 'pagesection' and app in SECTION_FIELDS:
        return SECTION_FIELDS[app], {'section_type', 'module', 'order', 'is_active'}
    if name == 'sectioncontent' and app in ITEM_FIELDS:
        return ITEM_FIELDS[app], {'section', 'order', 'is_active'}
    return None, set()


def context(model, data, obj=None):
    if model._meta.model_name == 'pagesection':
        return data.get('section_type', getattr(obj, 'section_type', ''))
    if model._meta.model_name == 'sectioncontent':
        parent_id = data.get('section', getattr(obj, 'section_id', None))
        try:
            parent = model._meta.get_field('section').related_model.objects.filter(pk=parent_id).first()
        except (ValueError, TypeError):
            return ''
        return parent.section_type if parent else ''
    return ''


def editable_fields(model, data, obj=None):
    editable = [f.name for f in model._meta.fields if f.editable and not f.primary_key and f.name not in {'content_type', 'object_id'}]
    rules, common = policy(model)
    if rules is None:
        return editable
    relevant = common | rules.get(context(model, data, obj), set())
    return [name for name in editable if name in relevant]
