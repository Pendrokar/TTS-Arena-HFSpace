import time
from gradio_client import Client
from .models import *
from .utils import *
from .config import *
from .init import *
from .sample_caching import *

import gradio as gr
from pydub import AudioSegment
import random, os, threading, tempfile
from langdetect import detect
from .vote import log_text

hf_token=os.getenv('HF_TOKEN')

def random_m():
    return random.sample(list(set(AVAILABLE_MODELS.keys())), 2)

def check_toxicity(text):
    if not TOXICITY_CHECK:
        return False
    return toxicity.predict(text)['toxicity'] > 0.8

def synthandreturn(text, autoplay, request: gr.Request):
    text = text.strip()
    if len(text) > MAX_SAMPLE_TXT_LENGTH:
        raise gr.Error(f'You exceeded the limit of {MAX_SAMPLE_TXT_LENGTH} characters')
    if len(text) < MIN_SAMPLE_TXT_LENGTH:
        raise gr.Error(f'Please input a text longer than {MIN_SAMPLE_TXT_LENGTH} characters')
    if (
        # test toxicity if not prepared text
        text not in sents
        and check_toxicity(text)
    ):
        print(f'Detected toxic content! "{text}"')
        raise gr.Error('Your text failed the toxicity test')
    if not text:
        raise gr.Error(f'You did not enter any text')
    # Check language
    try:
        if (
            text not in sents
            and not detect(text) == "en"
        ):
            gr.Warning('Warning: The input text may not be in English')
    except:
        pass
    # Get two random models

    # forced model: your TTS model versus The World!!!
    # mdl1 = 'Pendrokar/xVASynth'

    # scrutinize the top five by always picking one of them
    if (len(top_five) >= 5):
        mdl1 = random.sample(top_five, 1)[0]
        vsModels = dict(AVAILABLE_MODELS)
        del vsModels[mdl1]
        # randomize position of the forced model
        mdl2 = random.sample(list(vsModels.keys()), 1)
        # forced random
        mdl1, mdl2 = random.sample(list([mdl1, mdl2[0]]), 2)
    else:
        # actual random
        mdl1, mdl2 = random.sample(list(AVAILABLE_MODELS.keys()), 2)

    print("[debug] Using", mdl1, mdl2)
    def predict_and_update_result(text, model, result_storage, request:gr.Request):

        hf_headers = {}
        try:
            if HF_SPACES[model]['is_zero_gpu_space']:
                hf_headers = {"X-IP-Token": request.headers['x-ip-token']}
        except:
            pass

        # re-attempt if necessary
        attempt_count = 0
        max_attempts = 1 # 3 =May cause 429 Too Many Request
        while attempt_count < max_attempts:
            try:
                if model in AVAILABLE_MODELS:
                    if '/' == AVAILABLE_MODELS[model][0]:
                        # local model
                        # just Edge TTS API
                        from .tts.edge import edge_text_to_speech
                        result = edge_text_to_speech(text, 'en-US-EmmaMultilingualNeural - en-US (Female)')
                    elif '/' in model:
                        # Use public HF Space
                        # if (model not in hf_clients):
                        #     #save client to local variable; can timeout
                        #     hf_clients[model] = Client(model, hf_token=hf_token, headers=hf_headers)
                        try:
                            # use TTS host's token
                            client_token = HF_SPACES[model]['hf_token']
                        except:
                            # use arena host's token
                            client_token = hf_token
                        # even this may cause 429 Too Many Request
                        mdl_space = Client(AVAILABLE_MODELS[model], hf_token=client_token, headers=hf_headers)

                        # print(f"{model}: Fetching endpoints of HF Space")
                        # assume the index is one of the first 9 return params
                        return_audio_index = int(HF_SPACES[model]['return_audio_index'])
                        endpoints = mdl_space.view_api(all_endpoints=True, print_info=False, return_format='dict')

                        api_name = None
                        fn_index = None
                        end_parameters = None
                        # has named endpoint
                        if '/' == HF_SPACES[model]['function'][0]:
                            # audio sync function name
                            api_name = HF_SPACES[model]['function']

                            end_parameters = _get_param_examples(
                                endpoints['named_endpoints'][api_name]['parameters']
                            )
                        # has unnamed endpoint
                        else:
                            # endpoint index is the first character
                            fn_index = int(HF_SPACES[model]['function'])

                            end_parameters = _get_param_examples(
                                endpoints['unnamed_endpoints'][str(fn_index)]['parameters']
                            )

                        # override some or all default parameters
                        space_inputs = _override_params(end_parameters, model)

                        # force text
                        space_inputs[HF_SPACES[model]['text_param_index']] = text

                        print(f"{model}: Sending request to HF Space")
                        # results = mdl_space.predict(*space_inputs, api_name=api_name, fn_index=fn_index)
                        if(type(space_inputs) == dict):
                            results = mdl_space.predict(
                                **space_inputs,
                                api_name=api_name,
                                fn_index=fn_index
                            )
                        else:
                            results = mdl_space.predict(
                                *space_inputs,
                                api_name=api_name,
                                fn_index=fn_index
                            )

                        # return path to audio
                        result = results
                        if (not isinstance(results, str)):
                            # return_audio_index may be a filepath string
                            result = results[return_audio_index]
                        if (isinstance(result, dict)):
                            # return_audio_index is a dictionary
                            result = results[return_audio_index]['value']
                    else:
                        # Use the private HF Space
                        result = router.predict(text, AVAILABLE_MODELS[model].lower(), api_name="/synthesize")
                else:
                    result = router.predict(text, model.lower(), api_name="/synthesize")
                break
            except Exception as e:
                attempt_count += 1
                raise gr.Error(f"{model}:"+ repr(e))
                # print(f"{model}: Unable to call API (attempt: {attempt_count})")
                # sleep for three seconds to avoid spamming the server with requests
                # time.sleep(3)

                # Fetch and store client again
                # hf_clients[model] = Client(model, hf_token=hf_token, headers=hf_headers)

        if attempt_count >= max_attempts:
            raise gr.Error(f"{model}: Failed to call model")
        else:
            print('Done with', model)

        # Resample to 24kHz
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                audio = AudioSegment.from_file(result)
                current_sr = audio.frame_rate
                if current_sr > 24000:
                    print(f"{model}: Resampling")
                    audio = audio.set_frame_rate(24000)
                try:
                    print(f"{model}: Trying to normalize audio")
                    audio = match_target_amplitude(audio, -20)
                except:
                    print(f"{model}: [WARN] Unable to normalize audio")
                audio.export(f.name, format="wav")
                os.unlink(result)
                result = f.name
                gr.Info('Audio from a TTS model received')
        except:
            print(f"{model}: [WARN] Unable to resample audio")
            pass
        # if model in AVAILABLE_MODELS.keys(): model = AVAILABLE_MODELS[model]
        result_storage[model] = result

    def _get_param_examples(parameters):
        # named or unnamed parameters
        try:
            param_name = parameters[0]['parameter_name']
            # success => named params, use dict
            example_inputs = {}
        except:
            # unnamed params, use list
            example_inputs = []
            pass

        for param_info in parameters:


            param_name = ''
            param_default_value = param_info['example_input']
            try:
                # named params
                param_name = param_info['parameter_name']
                param_default_value = param_info['parameter_default']
            except:
                # unnamed params
                pass

            param_value = None
            if (
                param_info['component'] == 'Radio'
                or param_info['component'] == 'Dropdown'
                or param_info['component'] == 'Audio'
                or param_info['python_type']['type'] == 'str'
            ):
                param_value = str(param_default_value)
            elif param_info['python_type']['type'] == 'int':
                param_value = int(param_default_value)
            elif param_info['python_type']['type'] == 'float':
                param_value = float(param_default_value)
            elif param_info['python_type']['type'] == 'bool':
                param_value = bool(param_default_value)

            if (param_name != ''):
                # named param
                example_inputs[param_info['parameter_name']] = param_value
            else:
                # just append unnamed param and hope
                example_inputs.append(param_value)

        return example_inputs

    def _override_params(inputs, modelname):
        try:
            for key,value in OVERRIDE_INPUTS[modelname].items():
                # if override keys are integers, make the dict into a list
                if (
                    (type(inputs) is dict)
                    and (type(key) is int)
                ):
                    print(f"{modelname}: Converting unnamed override params to List")
                    inputs = list(inputs.values())

                inputs[key] = value
            print(f"{modelname}: Default inputs overridden by Arena")
        except:
            pass

        return inputs

    mdl1k = mdl1
    mdl2k = mdl2
    print(mdl1k, mdl2k)
    # if mdl1 in AVAILABLE_MODELS.keys(): mdl1k=AVAILABLE_MODELS[mdl1]
    # if mdl2 in AVAILABLE_MODELS.keys(): mdl2k=AVAILABLE_MODELS[mdl2]
    results = {}
    print(f"Sending models {mdl1k} and {mdl2k} to API")

    # do not use multithreading when both spaces are ZeroGPU type
    if (
        'is_zero_gpu_space' in HF_SPACES[mdl1]
        and HF_SPACES[mdl1]['is_zero_gpu_space']

        and 'is_zero_gpu_space' in HF_SPACES[mdl2]
        and HF_SPACES[mdl2]['is_zero_gpu_space']
    ):
        # run Zero-GPU spaces one at a time
        predict_and_update_result(text, mdl1k, results, request)
        cache_sample(results[mdl1k], text, mdl1k)

        predict_and_update_result(text, mdl2k, results, request)
        cache_sample(results[mdl2k], text, mdl2k)
    else:
        # use multithreading
        thread1 = threading.Thread(target=predict_and_update_result, args=(text, mdl1k, results, request))
        thread2 = threading.Thread(target=predict_and_update_result, args=(text, mdl2k, results, request))

        thread1.start()
        # wait 3 seconds to calm hf.space domain
        time.sleep(3)
        thread2.start()
        # timeout in 2 minutes
        thread1.join(120)
        thread2.join(120)

        # cache each result
        for model in [mdl1k, mdl2k]:
            cache_sample(results[model], text, model)

    print(f"Retrieving models {mdl1k} and {mdl2k} from API")
    return (
        text,
        "Synthesize 🐢",
        gr.update(visible=True), # r2
        mdl1, # model1
        mdl2, # model2
        gr.update(visible=True, value=results[mdl1k], autoplay=autoplay), # aud1
        gr.update(visible=True, value=results[mdl2k], autoplay=False), # aud2
        gr.update(visible=True, interactive=False), #abetter
        gr.update(visible=True, interactive=False), #bbetter
        gr.update(visible=False), #prevmodel1
        gr.update(visible=False), #prevmodel2
        gr.update(visible=True), #nxt round btn
        # reset gr.State aplayed & bplayed
        False, #aplayed
        False, #bplayed
    )

# Battle Mode

def synthandreturn_battle(text, mdl1, mdl2, autoplay):
    if mdl1 == mdl2:
        raise gr.Error('You can\'t pick two of the same models.')
    text = text.strip()
    if len(text) > MAX_SAMPLE_TXT_LENGTH:
        raise gr.Error(f'You exceeded the limit of {MAX_SAMPLE_TXT_LENGTH} characters')
    if len(text) < MIN_SAMPLE_TXT_LENGTH:
        raise gr.Error(f'Please input a text longer than {MIN_SAMPLE_TXT_LENGTH} characters')
    if (
        # test toxicity if not prepared text
        text not in sents
        and check_toxicity(text)
    ):
        print(f'Detected toxic content! "{text}"')
        raise gr.Error('Your text failed the toxicity test')
    if not text:
        raise gr.Error(f'You did not enter any text')
    # Check language
    try:
        if not detect(text) == "en":
            gr.Warning('Warning: The input text may not be in English')
    except:
        pass
    # Get two random models
    log_text(text)
    print("[debug] Using", mdl1, mdl2)
    def predict_and_update_result(text, model, result_storage):
        try:
            if model in AVAILABLE_MODELS:
                result = router.predict(text, AVAILABLE_MODELS[model].lower(), api_name="/synthesize")
            else:
                result = router.predict(text, model.lower(), api_name="/synthesize")
        except:
            raise gr.Error('Unable to call API, please try again :)')
        print('Done with', model)
        # try:
        #     doresample(result)
        # except:
        #     pass
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                audio = AudioSegment.from_file(result)
                current_sr = audio.frame_rate
                if current_sr > 24000:
                    audio = audio.set_frame_rate(24000)
                try:
                    print('Trying to normalize audio')
                    audio = match_target_amplitude(audio, -20)
                except:
                    print('[WARN] Unable to normalize audio')
                audio.export(f.name, format="wav")
                os.unlink(result)
                result = f.name
        except:
            pass
        # if model in AVAILABLE_MODELS.keys(): model = AVAILABLE_MODELS[model]
        print(model)
        print(f"Running model {model}")
        result_storage[model] = result
        # try:
        #     doloudnorm(result)
        # except:
        #     pass
    mdl1k = mdl1
    mdl2k = mdl2
    print(mdl1k, mdl2k)
    # if mdl1 in AVAILABLE_MODELS.keys(): mdl1k=AVAILABLE_MODELS[mdl1]
    # if mdl2 in AVAILABLE_MODELS.keys(): mdl2k=AVAILABLE_MODELS[mdl2]
    results = {}
    print(f"Sending models {mdl1k} and {mdl2k} to API")
    thread1 = threading.Thread(target=predict_and_update_result, args=(text, mdl1k, results))
    thread2 = threading.Thread(target=predict_and_update_result, args=(text, mdl2k, results))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    print(f"Retrieving models {mdl1k} and {mdl2k} from API")
    return (
        text,
        "Synthesize 🐢",
        gr.update(visible=True), # r2
        mdl1, # model1
        mdl2, # model2
        gr.update(visible=True, value=results[mdl1k], autoplay=autoplay), # aud1
        gr.update(visible=True, value=results[mdl2k], autoplay=False), # aud2
        gr.update(visible=True, interactive=False), #abetter
        gr.update(visible=True, interactive=False), #bbetter
        gr.update(visible=False), #prevmodel1
        gr.update(visible=False), #prevmodel2
        gr.update(visible=False), #nxt round btn
    )

def randomsent():
    return '⚡', random.choice(sents), '🎲'
def randomsent_battle():
    return tuple(randomsent()) + tuple(random_m())
def clear_stuff():
    return [
        gr.update(visible=True, value="", elem_classes=[]),
        "Synthesize 🐢",
        gr.update(visible=False), # r2
        '', # model1
        '', # model2
        gr.update(visible=False, interactive=False, autoplay=False), # aud1
        gr.update(visible=False, interactive=False, autoplay=False), # aud2
        gr.update(visible=False, interactive=False), #abetter
        gr.update(visible=False, interactive=False), #bbetter
        gr.update(visible=False), #prevmodel1
        gr.update(visible=False), #prevmodel2
        gr.update(visible=False), #nxt round btn
        False, #aplayed
        False, #bplayed
    ]