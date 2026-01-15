import json
import operator

# ----------------------------
# Rule engine (same logic)
# ----------------------------
OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

def evaluate_condition(facts, cond):
    field, op, value = cond
    return OPS[op](facts[field], value)

def rule_matches(facts, rule):
    return all(evaluate_condition(facts, c) for c in rule["conditions"])

def run_rules(facts, rules):
    fired = [r for r in rules if rule_matches(facts, r)]
    fired_sorted = sorted(fired, key=lambda r: r["priority"], reverse=True)
    return fired_sorted[0]["action"], fired_sorted


# ----------------------------
# Load rules (JSON file)
# ----------------------------
rules_json = """PASTE YOUR JSON HERE"""
rules = json.loads(rules_json)

# ----------------------------
# Given home conditions
# ----------------------------
facts = {
    "temperature": 22,
    "humidity": 46,
    "occupancy": "OCCUPIED",
    "time_of_day": "NIGHT",
    "windows_open": False
}

# ----------------------------
# Run rule engine
# ----------------------------
final_action, matched_rules = run_rules(facts, rules)

print("Final AC Decision")
print("AC Mode:", final_action["ac_mode"])
print("Fan Speed:", final_action["fan_speed"])
print("Setpoint:", final_action["setpoint"])
print("Reason:", final_action["reason"])