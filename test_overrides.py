from app.models import *

# # has named endpoint
# if '/' == HF_SPACES[model]['function'][0]:
#     # audio sync function name
#     api_name = HF_SPACES[model]['function']

#     end_parameters = _get_param_examples(
#         endpoints['named_endpoints'][api_name]['parameters']
#     )
# # has unnamed endpoint
# else:
#     # endpoint index is the first character
#     fn_index = int(HF_SPACES[model]['function'])

#     end_parameters = _get_param_examples(
#         endpoints['unnamed_endpoints'][str(fn_index)]['parameters']
#     )

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
                print("Converting unnamed override params to List")
                inputs = list(inputs.values())

            inputs[key] = value
        print(f"{modelname}: Default inputs overridden by Arena")
    except:
        pass

    return inputs