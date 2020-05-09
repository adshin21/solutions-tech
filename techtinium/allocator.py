#!/usr/bin/env python3

# Mapping size to number of units
type_to_capacity = {
    "Large": 10,
    "XLarge": 20,
    "2XLarge": 40,
    "4XLarge": 80,
    "8XLarge": 160,
    "10XLarge": 320,
}

cost_by_region = {
    "New York": {
        "Large": 120,
        "XLarge": 230,
        "2XLarge": 450,
        "4XLarge": 774,
        "8XLarge": 1400,
        "10XLarge": 2820,
    },
    "India": {
        "Large": 140,
        "XLarge": None,
        "2XLarge": 413,
        "4XLarge": 890,
        "8XLarge": 1300,
        "10XLarge": 2970,
    },
    "China": {
        "Large": 110,
        "XLarge": 200,
        "2XLarge": None,
        "4XLarge": 670,
        "8XLarge": 1180,
        "10XLarge": None,
    }
}


def get_cost_per_unit_per_size(cost_by_capacity):
    '''
        To get cost per unit with respected 
        capacity in increasing order

        This function will sort the machine 
        which by their cost per unit
    '''

    for each_size in cost_by_capacity.keys():
        cost = cost_by_capacity[each_size]

        if cost is None:
            continue

        cost_by_capacity[each_size] /= type_to_capacity[each_size]

    cost_per_unit = {key: val for key, val in sorted(
        cost_by_capacity.items(), key=lambda x: (x[1] is None, x[1]))}

    return cost_per_unit


def resource_allocator(region, units, hours):
    '''
        Algorithm to resouce allocation

        Idea is to use that unit first 
        which is charging less value
        per unit and if they are not 
        capable to produce the required 
        unitthen go to the next one
    '''

    if units <= 0 or hours <= 0:
        return 'Not a valid combination of time and units'
    
    total_units = units * hours

    if total_units <= 0:
        return 'Not a valid combination of time and units'

    # making a copy of dic to avoid passing in funtion by reference
    region_dict = { **(cost_by_region[region]) }

    cost_per_unit_by_size = get_cost_per_unit_per_size(region_dict)
    total_cost = 0
    machines = []

    for type_of_machine in cost_per_unit_by_size.keys():
        particular_size_machine_cost = cost_per_unit_by_size[type_of_machine]
        machine_per_hour_capacity = type_to_capacity[type_of_machine]

        number_of_machines_required, total_units = divmod(total_units, machine_per_hour_capacity)
        total_cost += particular_size_machine_cost * number_of_machines_required * machine_per_hour_capacity

        if number_of_machines_required:
            machines.append((type_of_machine, number_of_machines_required))
        if total_units == 0:
            break

    return {
        "region" : region,
        "total_cost" : "$" + str(round(total_cost)),
        "machines" : machines
    }
    

def parse_input():
    '''Function to parse the input'''

    units, hours = None, None
    
    lst_input = list(input().split(' '))
    input_len = len(lst_input)
    
    for i in range(input_len-1):
        if lst_input[i+1].lower() == 'units' or lst_input[i+1].lower() == 'unit':
            try:
                units = int(lst_input[i])
            except:
                print('Please provide the valid input (natural number)')
                return
        if lst_input[i+1].lower() == 'hours' or lst_input[i+1].lower() == 'hour':
            try:
                hours = int(lst_input[i])
            except:
                print('Please provide the valid input (natural number)')
                return
    
    return (units, hours)


def format(json):
    '''The fuction is use to format the output as desired'''

    if not json:
        return ''
    
    result = []
    multiplier = 0

    # this is to use the output indent level currently it is of 4 spaces
    tab = '    '
    length = len(json)

    i = 0
    
    while i < length:
        if json[i] in ['{', '[']:
            if json[i] == '[':
                result[-1] += ' ['
            else:
                result.append(tab * multiplier + json[i])
            multiplier += 1
            i += 1
        elif json[i] == '(':
            strart = i
            while i < length and json[i] != ')':
                i += 1
            cur = json[strart:i+1]
            result.append(tab * multiplier + cur)
            i += 1
        elif json[i] in ['}', ']']:
            multiplier -= 1
            result.append(tab * multiplier + json[i])
            i += 1
        elif json[i] == ',':
            result[-1]+= ','
            i += 1
        else:
            start = i
            curr_s = []
            while i < length and json[i] not in ['{', '}', ',', '[', ']']:
                if json[i] == ':':
                    curr_s.append(': ')
                else:
                    curr_s.append(json[i])
                i += 1

            curr_s = ''.join(curr_s)
            result.append(tab * multiplier + curr_s)
    
    for row in result:
        print(row)

    
def main(units, hours):

    if units <= 0 and hours <= 0:
        print('Units and Hours can not be zero/negative')
        return
    elif units <= 0 or not units:
        print('Units can not be zero/negative')
        return
    elif hours <= 0 or not hours:
        print('Hours can not be zero/negative')
        return
    
    output = {
        'Output' : []
    }

    for region in [ 'New York', 'India', 'China' ]:
        out = resource_allocator(region, units, hours) # Calcutation the cost by region
        output['Output'].append(out)

    output = str(output).replace(' ', '')
    format(str(output)) # formatting the output as desired


if __name__ == '__main__':

    # You can comment the next line (216) to avoid console input 
    # and provide units and hours in next to next line manually in (217)
    units, hours = parse_input()
    main(units, hours)
