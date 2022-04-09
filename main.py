# !pip install scikit-fuzzy
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import csv

# Define the domain of the two antecedent membership functions
distance = ctrl.Antecedent(np.arange(0.0, 5.0, 0.5), 'distance')
angle = ctrl.Antecedent(np.arange(-60, 60, 1), 'angle')

# Define Angle Antecendent membership function
angle['left'] = fuzz.trapmf(angle.universe, [-60, -60, -40, -15])
angle['front'] = fuzz.trapmf(angle.universe, [-40, -15, 15, 40])
angle['right'] = fuzz.trapmf(angle.universe, [15, 40, 60, 60])

# Define Distance Antecendent membership function
distance['very close'] = fuzz.trapmf(distance.universe, [0, 0, 1, 1.5])
distance['close'] = fuzz.trimf(distance.universe, [1, 1.5, 2])
distance['close/mid'] = fuzz.trimf(distance.universe, [1.5, 2, 2.5])
distance['mid'] = fuzz.trimf(distance.universe, [2, 2.5, 3])
distance['far'] = fuzz.trimf(distance.universe, [2.5, 3, 3.5])
distance['very far'] = fuzz.trapmf(distance.universe, [3, 3.5, 5, 5])

# Graph membership functions
angle.view()
distance.view()

# Define domain of Consequent Membership functions
warning = ctrl.Consequent(np.arange(0,101, 1), 'warning')
brake = ctrl.Consequent(np.arange(0, 101, 1), 'brake')
decelerate = ctrl.Consequent(np.arange(0, 101, 1), 'decelerate')

# Define Warning Membership functions
warning['off'] = fuzz.trapmf(warning.universe, [0, 0, 40, 60])
warning['on'] = fuzz.trapmf(warning.universe, [30, 50, 100, 100])

# Define Decelerate Membership functions
decelerate['none'] = fuzz.trapmf(decelerate.universe, [0, 0, 10, 30])
decelerate['low'] = fuzz.trimf(decelerate.universe, [10, 30, 50])
decelerate['high'] = fuzz.trapmf(decelerate.universe, [40, 50, 100, 100])

# Define Brake Membership functions
brake['none'] = fuzz.trapmf(brake.universe, [0, 0, 30, 50])
brake['low'] = fuzz.trimf(brake.universe, [40, 60, 80])
brake['high'] = fuzz.trapmf(brake.universe, [70, 90, 100, 100])

# Results - Brake (percentage), warning, reduce accelleration (percentage)

# Graph function
warning.view()
decelerate.view()
brake.view()

def print_warning(output, to_print = False):
    values = { warning:'', decelerate:'', brake:'' }

    # Warning Output
    if output['warning_on'] > output['warning_off']:
        values['warning'] = 'ON'
    else:
        values['warning'] = 'OFF'

    # Deceleration Output
    if output['decel_none'] > output['decel_low'] and output['decel_none'] > output['decel_high']:
        values['decelerate'] = 'NONE'
    if output['decel_low'] > output['decel_none'] and output['decel_low'] > output['decel_high']:
        values['decelerate'] = 'LOW'
    if output['decel_high'] > output['decel_none'] and output['decel_high'] > output['decel_low']:
        values['decelerate'] = 'HIGH'

    # Brake Output
    if output['brake_none'] > output['brake_low'] and output['brake_none'] > output['brake_high']:
        values['brake'] = 'NONE'
    if output['brake_low'] > output['brake_none'] and output['brake_low'] > output['brake_high']:
        values['brake'] = 'LOW'
    if output['brake_high'] > output['brake_none'] and output['brake_high'] > output['brake_low']:
        values['brake'] = 'HIGH'

    if not to_print:
        print('Warning: ' + values['warning'])
        print('Decelerate: ' + values['decelerate'])
        print('Brake: ' + values['brake'])


    return values

# Brake Rules
b_rule1 = ctrl.Rule(angle['front'] & distance['very far'], brake['none'])
b_rule2 = ctrl.Rule(angle['front'] & distance['far'], brake['none'])
b_rule3 = ctrl.Rule(angle['front'] & distance['mid'], brake['none'])
b_rule4 = ctrl.Rule(angle['front'] & distance['close/mid'], brake['none'])
b_rule5 = ctrl.Rule(angle['front'] & distance['close'], brake['low'])
b_rule6 = ctrl.Rule(angle['front'] & distance['very close'], brake['high'])
b_rule7 = ctrl.Rule(angle['left'] | angle['right'], brake['none'])

# Decelerate Rules
d_rule1 = ctrl.Rule(angle['front'] & distance['very far'], decelerate['none'])
d_rule2 = ctrl.Rule(angle['front'] & distance['far'], decelerate['none'])
d_rule3 = ctrl.Rule(angle['front'] & distance['mid'], decelerate['low'])
d_rule4 = ctrl.Rule(angle['front'] & distance['close/mid'], decelerate['high'])
d_rule5 = ctrl.Rule(angle['front'] & distance['close'], decelerate['high'])
d_rule6 = ctrl.Rule(angle['front'] & distance['very close'], decelerate['high'])
d_rule7 = ctrl.Rule(angle['left'] | angle['right'], decelerate['none'])

# Warning Rules
w_rule1 = ctrl.Rule(angle['front'] & distance['very far'], warning['off'])
w_rule2 = ctrl.Rule(angle['front'] & distance['far'], warning['on'])
w_rule3 = ctrl.Rule(angle['front'] & distance['mid'], warning['on'])
w_rule4 = ctrl.Rule(angle['front'] & distance['close/mid'], warning['on'])
w_rule5 = ctrl.Rule(angle['front'] & distance['close'], warning['on'])
w_rule6 = ctrl.Rule(angle['front'] & distance['very close'], warning['on'])
w_rule7 = ctrl.Rule(angle['left'] | angle['right'], warning['off'])

rules = [b_rule1, b_rule2, b_rule3, b_rule4, b_rule5, b_rule6, b_rule7, d_rule1, d_rule2, d_rule3, d_rule4, d_rule5, d_rule6, d_rule7, w_rule1, w_rule2, w_rule3, w_rule4, w_rule5, w_rule6, w_rule7]

def print_warning(output, to_print = False):
    values = { warning:'', decelerate:'', brake:'' }

    # Warning Output
    if output['warning_on'] > output['warning_off']:
        values['warning'] = 'ON'
    else:
        values['warning'] = 'OFF'

    # Deceleration Output
    if output['decel_none'] > output['decel_low'] and output['decel_none'] > output['decel_high']:
        values['decelerate'] = 'NONE'
    if output['decel_low'] > output['decel_none'] and output['decel_low'] > output['decel_high']:
        values['decelerate'] = 'LOW'
    if output['decel_high'] > output['decel_none'] and output['decel_high'] > output['decel_low']:
        values['decelerate'] = 'HIGH'

    # Brake Output
    if output['brake_none'] > output['brake_low'] and output['brake_none'] > output['brake_high']:
        values['brake'] = 'NONE'
    if output['brake_low'] > output['brake_none'] and output['brake_low'] > output['brake_high']:
        values['brake'] = 'LOW'
    if output['brake_high'] > output['brake_none'] and output['brake_high'] > output['brake_low']:
        values['brake'] = 'HIGH'

    if not to_print:
        print('Warning: ' + values['warning'])
        print('Decelerate: ' + values['decelerate'])
        print('Brake: ' + values['brake'])


    return values

# Define inference engine
system_ctrl = ctrl.ControlSystem(rules)

# Create instance of inference engine
instance1 = ctrl.ControlSystemSimulation(system_ctrl)

# Process input data
def process_input(t_dist, angle, to_print = False):
    instance1.input['distance'] = t_dist
    instance1.input['angle'] = angle
    
    instance1.compute()

    # Define output
    output = {}
    output['warning_on'] = fuzz.interp_membership(warning.universe, warning['on'].mf, instance1.output['warning'])
    output['warning_off'] = fuzz.interp_membership(warning.universe, warning['off'].mf, instance1.output['warning'])
    output['decel_none'] = fuzz.interp_membership(decelerate.universe, decelerate['none'].mf, instance1.output['decelerate'])
    output['decel_low'] = fuzz.interp_membership(decelerate.universe, decelerate['low'].mf, instance1.output['decelerate'])
    output['decel_high'] = fuzz.interp_membership(decelerate.universe, decelerate['high'].mf, instance1.output['decelerate'])
    output['brake_none'] = fuzz.interp_membership(brake.universe, brake['none'].mf, instance1.output['brake'])
    output['brake_low'] = fuzz.interp_membership(brake.universe, brake['low'].mf, instance1.output['brake'])
    output['brake_high'] = fuzz.interp_membership(brake.universe, brake['high'].mf, instance1.output['brake'])
    
    if not to_print:
        # Visualise results
        warning.view(sim=instance1)
        decelerate.view(sim=instance1)
        brake.view(sim=instance1)
        
        # Print output action to terminal
        print_warning(output)

    #return [instance1.output, output] -- FOR TESTING ONLY

# Simulate vehicle 2 seconds distance, 10 degrees angle
process_input(2, 10)

# Define working variables
x = warning.universe
w_mfx_on = warning['on'].mf
w_mfx_off = warning['off'].mf

# Defuzzify a membership function
def defuzz(universe, mem_functions, defuzz_method):
    if (defuzz_method in ('centroid', 'bisector', 'mom', 'som', 'lom')):
        result = []
        for func in mem_functions:
            result.append(fuzz.defuzz(universe, func, defuzz_method))
    else:
        print('Invalid defuzzification method! Please use centroid, bisector, mom, som or lom.')

    return result

# Plot graph
def graph(universe, mem_functions, x, defuzz_method):
    plt.figure(figsize=(8, 5))

    for func in mem_functions:
        plt.plot(universe, func, 'k')

    y = fuzz.interp_membership(universe, mem_functions[0], x)
    
    plt.vlines(x, 0, y, label=defuzz_method, color='r')
    plt.ylabel('Fuzzy membership')
    plt.xlabel('Universe variable (arb)')
    plt.ylim(-0.1, 1.1)
    plt.legend(loc=2)
    plt.show()


# Execute code
result = defuzz(x, [w_mfx_on, w_mfx_off], 'centroid')
print(result)
graph(x, [w_mfx_on, w_mfx_off], result, 'centroid')