def forward_chain(initial_facts, rules):
    """
    Apply propositional rules using forward chaining.

    initial_facts:
        Dictionary containing facts and Boolean values.

    rules:
        List of logical rules.

    Returns:
        inferred_facts
        fired_rules
    """

    inferred_facts = {
        fact: value
        for fact, value in initial_facts.items()
        if value is True
    }

    fired_rules = []

    changed = True

    while changed:

        changed = False

        for rule in rules:

            rule_id = rule["id"]
            conditions = rule["conditions"]
            conclusion = rule["conclusion"]

            conditions_satisfied = all(
                condition in inferred_facts
                for condition in conditions
            )

            if conditions_satisfied:

                if conclusion not in inferred_facts:

                    inferred_facts[conclusion] = True

                    changed = True

                    fired_rules.append({
                        "rule_id": rule_id,
                        "conditions": conditions,
                        "conclusion": conclusion
                    })

    return inferred_facts, fired_rules