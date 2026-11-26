
import json
import operator

# ----------------------------
# Rule Engine
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
    return all(
        evaluate_condition(facts, condition)
        for condition in rule["conditions"]
    )


def run_rules(facts, rules):
    fired = [
        rule for rule in rules
        if rule_matches(facts, rule)
    ]

    fired_sorted = sorted(
        fired,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    if not fired_sorted:
        return None, []

    return fired_sorted[0]["action"], fired_sorted


# ----------------------------
# Define Rules (JSON)
# ----------------------------

rules_json = """
[
    {
        "priority": 1,
        "conditions": [
            ["occupancy", "==", "UNOCCUPIED"]
        ],
        "action": {
            "ac_mode": "OFF",
            "fan_speed": "OFF",
            "setpoint": 0,
            "reason": "Room is unoccupied."
        }
    },
    {
        "priority": 2,
        "conditions": [
            ["windows_open", "==", true]
        ],
        "action": {
            "ac_mode": "OFF",
            "fan_speed": "OFF",
            "setpoint": 0,
            "reason": "Windows are open."
        }
    },
    {
        "priority": 3,
        "conditions": [
            ["temperature", ">=", 28],
            ["occupancy", "==", "OCCUPIED"]
        ],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "HIGH",
            "setpoint": 22,
            "reason": "High temperature detected."
        }
    },
    {
        "priority": 4,
        "conditions": [
            ["temperature", ">=", 24],
            ["occupancy", "==", "OCCUPIED"]
        ],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "MEDIUM",
            "setpoint": 24,
            "reason": "Moderate temperature detected."
        }
    },
    {
        "priority": 5,
        "conditions": [
            ["temperature", "<", 24],
            ["occupancy", "==", "OCCUPIED"]
        ],
        "action": {
            "ac_mode": "ECO",
            "fan_speed": "LOW",
            "setpoint": 26,
            "reason": "Room temperature is comfortable."
        }
    }
]
"""

rules = json.loads(rules_json)


# ----------------------------
# Given Home Conditions
# ----------------------------

facts = {
    "temperature": 22,
    "humidity": 46,
    "occupancy": "OCCUPIED",
    "time_of_day": "NIGHT",
    "windows_open": False
}


# ----------------------------
# Run Rule Engine
# ----------------------------

final_action, matched_rules = run_rules(facts, rules)


# ----------------------------
# Display Results
# ----------------------------

print("=" * 40)
print("       FINAL AC DECISION")
print("=" * 40)

if final_action:

    print("AC Mode:", final_action["ac_mode"])
    print("Fan Speed:", final_action["fan_speed"])
    print("Setpoint:", final_action["setpoint"])
    print("Reason:", final_action["reason"])

    print("\nMatched Rules:")

    for rule in matched_rules:
        print(
            "Priority:",
            rule["priority"],
            "| Action:",
            rule["action"]["ac_mode"]
        )

else:
    print("No matching rules found.")
