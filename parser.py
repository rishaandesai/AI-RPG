import re
import json

def parse(filename):
    with open(filename, 'r') as f:
        content = f.read()
    instructions = re.findall(r'<state>(.*?)</state>|<dice_roll type="(\d+)d(\d+)">(.*?)</dice_roll>', content, re.DOTALL)
    parsed_instructions = []
    for instruction in instructions:
        if instruction[0]:  # For state changes
            try:
                state_json = instruction[0].strip()
                parsed_instructions.append({'type': 'state', 'value': json.loads(state_json)})
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print("Problematic JSON data:", state_json)
                continue
        else:  # For dice rolls
            parsed_instructions.append({
                'type': 'dice_roll',
                'dice_count': int(instruction[1]),
                'sides': int(instruction[2]),
                'reason': instruction[3].strip()
            })
    return parsed_instructions

if __name__ == '__main__':
    # Run the instruction parser
    instructions = parse('toparse.txt')
    print("Parsed Instructions:")
    for instruction in instructions:
        print(instruction)