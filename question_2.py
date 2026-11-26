import json
import operator

# ==========================================
# 1. RULE ENGINE
# ==========================================

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

    # Sort matched rules according to priority
    fired_sorted = sorted(
        fired,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    if not fired_sorted:
        return None, []

    return fired_sorted[0]["action"], fired_sorted


# ==========================================
# 2. LOAD JSON RULES
# ==========================================

rules_json = """
[
    {
        "priority": 100,
        "conditions": [
            ["windows_open", "==", true]
        ],
        "action": {
            "ac_mode": "OFF",
            "fan_speed": "OFF",
            "setpoint": 0,
            "reason": "Windows are open"
        }
    },
    {
        "priority": 90,
        "conditions": [
            ["occupancy", "==", "UNOCCUPIED"]
        ],
        "action": {
            "ac_mode": "OFF",
            "fan_speed": "OFF",
            "setpoint": 0,
            "reason": "Room is unoccupied"
        }
    },
    {
        "priority": 80,
        "conditions": [
            ["temperature", ">=", 26]
        ],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "HIGH",
            "setpoint": 23,
            "reason": "Temperature is high"
        }
    },
    {
        "priority": 70,
        "conditions": [
            ["temperature", ">=", 24],
            ["occupancy", "==", "OCCUPIED"]
        ],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "MEDIUM",
            "setpoint": 24,
            "reason": "Room temperature is moderately high"
        }
    },
    {
        "priority": 50,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", "<", 24]
        ],
        "action": {
            "ac_mode": "AUTO",
            "fan_speed": "LOW",
            "setpoint": 24,
            "reason": "Comfortable room temperature"
        }
    }
]
"""

rules = json.loads(rules_json)


# ==========================================
# 3. GIVEN HOME CONDITIONS
# ==========================================

facts = {
    "temperature": 22,
    "humidity": 46,
    "occupancy": "OCCUPIED",
    "time_of_day": "NIGHT",
    "windows_open": False
}


# ==========================================
# 4. RUN RULE ENGINE
# ==========================================

final_action, matched_rules = run_rules(facts, rules)


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("=" * 45)
print("       SMART HOME AC CONTROL SYSTEM")
print("=" * 45)

print("\nHOME CONDITIONS")
print("-" * 45)

for key, value in facts.items():
    print(f"{key.replace('_', ' ').title():<20}: {value}")

print("\nRULE ENGINE RESULTS")
print("-" * 45)

if final_action is not None:

    print("Matched Rules:", len(matched_rules))

    for rule in matched_rules:
        print(
            f"Priority {rule['priority']}: "
            f"{rule['action']['reason']}"
        )

    print("\nFINAL AC DECISION")
    print("-" * 45)

    print("AC Mode   :", final_action["ac_mode"])
    print("Fan Speed :", final_action["fan_speed"])
    print("Setpoint  :", f"{final_action['setpoint']}°C")
    print("Reason    :", final_action["reason"])

else:

    print("No matching rules found.")
    print("Please check the home conditions and rules.")

print("\n" + "=" * 45)
