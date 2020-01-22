import json
from flask import Blueprint

views = Blueprint('views', __name__)

default_language = 'fi'
supported_languages = ('en', 'fi', 'sv')


def init_app(app):
    with app.app_context():
        # Register routes with the app

        # Admin views
        from . import login, attribute, attribute_group, building_class, session

        from . import answer
        from . import index
        from . import previous
        from . import question
        from . import feedback
        from . import updateData

        # Register blueprint
        app.register_blueprint(views)


def get_best_match_language(request):
    lang = request.args.get('lang')
    languages = [lang] if lang else request.accept_languages.values()
    return validate_language(languages)


def validate_language(langs):
    if isinstance(langs, str):
        langs = [langs]
    for lang in langs:
        # force strings like en-us to correct format
        try:
            lang = lang[:2].lower()
        except:
            print(f"Got weird lang param: {lang}")
            return default_language
        if lang in supported_languages:
            return lang
        return default_language


def translate_attr(attrJson, language):
    try:
        attr = json.loads(attrJson)
    except:
        print(f"Error parsing {attrJson}.")
        print("Expected this to be a dict of translations. Either the json is malformed or the attribute was translated already.")
        return attrJson

    ret_lang = default_language

    if language is not None:
        if language in supported_languages:
            ret_lang = language
        else:
            ret_lang = default_language
    else:
        print('language not defined, falling back to "fi"')
    try:
        translated = attr[ret_lang]
    except KeyError:
        print(f"Language {language} not found in {attrJson}")
        translated = ""
    return translated


def fix_question_language(question, language):
    if question['type'] == 'none':
        # Don't translate the empty question
        return
    elif question['type'] == 'multi':
        question['attribute_question'] = translate_attr(
            question['attribute_question'], language)
        for attribute in question['attributes']:
            attribute['attribute_name'] = translate_attr(
                attribute['attribute_name'], language)
            attribute['attribute_tooltip'] = translate_attr(
                attribute['attribute_tooltip'], language)
    else:
        question['attribute_name'] = translate_attr(
            question['attribute_name'], language)
        question['attribute_question'] = translate_attr(
            question['attribute_question'], language)
        question['attribute_tooltip'] = translate_attr(
            question['attribute_tooltip'], language)
