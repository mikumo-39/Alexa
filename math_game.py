# -*- coding: utf-8 -*-
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions Original -------------------------------

def check_custom_slots(intent):
    code = intent['slots']['level']['resolutions']['resolutionsPerAuthority'][0]['status']['code']
    if code == "ER_SUCCESS_MATCH":
        return  intent['slots']['level']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    else:
        return None

def make_question(level):
    randnum = random.randint(100,1000)
    if level == "初級":
        level_num = 5
        answer_num = random.randint(1,level_num)
        num_list = range(1, randnum, int(randnum/level_num))
    elif level == "中級":
        level_num = 10
        answer_num = random.randint(1,level_num)
        num_list = range(1, randnum, int(randnum/level_num))
    elif level == "上級":
        level_num = 20
        answer_num = random.randint(1,level_num)
        num_list = range(1, randnum, int(randnum/level_num))
    elif level == "神級":
        level_num = 30
        answer_num = random.randint(1,level_num)
        num_list = range(1, randnum, int(randnum/level_num))

    information = {}
    random.shuffle(num_list)
    information['level'] = level
    information['level_num'] = level_num
    information['num_list'] = num_list
    information['answer_num'] = answer_num
    return information


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "ようこそ数字記憶ゲームへ"
    speech_output = "こんにちは。数字記憶ゲームです。" \
                    "このスキルでは、４種類の難易度からあなたの記憶力を試すことができます。" \
                    "それでは、初級、中級、上級、神級の中からあなたのレベルにあったものを選んで、" \
                    "「初級を開始して」のように問いかけてください"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "please prompt"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "終了"
    speech_output = "遊んでくれてありがとう。" \
                    "また遊んでね。"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}

def start_game(intent, session):
    """ゲームの開始 ここで難易度の分岐とレスポンスの作成をするよ
    """
    level = check_custom_slots(intent)
    if level is not None:
        card_title = level + "にチャレンジ"
        session_attributes = {}
        should_end_session = False
        information = make_question(level)
        session_attributes['information'] = information
        speech_output = level + "の問題が完成したよ。"
        for num in information['num_list']:
            speech_output = speech_output + str(num) + ","
        speech_output = speech_output + "さぁ、" + str(information['answer_num']) + "番目に言った数字を教えて。"
        reprompt_text = speech_output
    else:
        card_title = "不明な難易度"
        session_attributes = {}
        should_end_session = False
        speech_output = "そんな難易度はないよ。初級、中級、上級、神級の４種類だけだよ。もう一度言ってみてね。"
        reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))




def get_hint(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "information" in session.get('attributes', {}):
        card_title = "ヒント"
        information = session['attributes']['information']
        answer_num = information['answer_num']
        answer = information['num_list'][answer_num-1]
        randnum = random.randint(1,50)
        hint_pattern = random.randint(1,3)
        if hint_pattern == 1:
            speech_output = "しょうがない。ヒントをあげるよ。確か " + str(answer - randnum) + \
                            "から" + str(answer + randnum) + "の間の数字だったと思うよ"
        elif hint_pattern == 2 or answer_num == 1:
            speech_output = "しょうがない。ヒントをあげるよ。確か答えの数字の後に言った数が" + str(information['num_list'][answer_num]) + \
                            "だったと思うよ"
        elif hint_pattern == 3 or answer_num == information['level_num']:
            speech_output = "しょうがない。ヒントをあげるよ。確か答えの数字の前に言った数が" + str(information['num_list'][answer_num-2]) + \
                            "だったと思うよ"
        reprompt_text = speech_output
        session_attributes['information'] = information
        should_end_session = False
    else:
        card_title = "まだ問題を出してないよ"
        speech_output = "まだ問題は出してないよ。焦らないで。"
        reprompt_text = speech_output
        should_end_session = False


    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def check_answer(intent, session):
    session_attributes = {}
    user_answer = intent['slots']['answer']['value']
    reprompt_text = None


    if session.get('attributes', {}) and "information" in session.get('attributes', {}):
        information = session['attributes']['information']
        answer_num = information['answer_num']
        answer = information['num_list'][answer_num-1]
        print(user_answer)
        print(answer)
        if int(user_answer) == int(answer):
            card_title = "大正解"
            if information['level'] == "初級":
                speech_output = "正解!次は中級にチャレンジしてみてね"
            elif  information['level'] == "中級":
                speech_output = "正解!上級にもチャレンジしてみてね"
            elif information['level'] == "上級":
                speech_output = "正解!神級にもチャレンジしてみてね"
            elif information['level'] == "神級":
                speech_output = "大正解!あなたは天才だね"
            should_end_session = True
        else:
            speech_output = "残念。不正解。もう一度記憶を思い出してみて。"
            session_attributes['information'] = information
            should_end_session = False

        reprompt_text = speech_output
    else:
        card_title = "まだ問題を出してないよ"
        speech_output = "まだ問題は出してないよ。焦らないで。"
        reprompt_text = speech_output
        should_end_session = False


    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartIntent":
        return start_game(intent, session)
    elif intent_name == "HintIntent":
        return get_hint(intent, session)
    elif intent_name == "AnswerIntent":
        return check_answer(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
