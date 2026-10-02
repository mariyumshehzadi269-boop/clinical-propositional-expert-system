CONDITION_FACTS = {

    "influenza_candidate":
        "Possible influenza-like illness",

    "viral_respiratory_candidate":
        "Possible viral respiratory illness",

    "upper_respiratory_candidate":
        "Possible upper respiratory illness",

    "gastrointestinal_candidate":
        "Possible gastrointestinal illness",

    "infection_evaluation":
        "Possible infection requiring clinical evaluation",

    "inflammatory_evaluation":
        "Possible inflammatory process requiring clinical evaluation"
}


TEST_FACTS = {

    "consider_influenza_test":
        "Consider influenza testing",

    "consider_viral_testing":
        "Consider viral testing",

    "consider_cbc":
        "Consider CBC review",

    "consider_crp_review":
        "Consider CRP review",

    "consider_chest_xray":
        "Consider chest X-ray"
}


REVIEW_FACTS = {

    "urgent_respiratory_evaluation":
        "Urgent respiratory evaluation indicated",

    "respiratory_evaluation":
        "Respiratory evaluation indicated",

    "consider_clinician_review_for_antiviral":
        "Consider clinician review regarding antiviral therapy",

    "consider_fever_management":
        "Consider clinical review for fever management"
}


def format_reasoning_trace(fired_rules):

    reasoning = []

    for rule in fired_rules:

        conditions = " AND ".join(
            rule["conditions"]
        )

        conclusion = rule["conclusion"]

        reasoning.append({
            "rule_id": rule["rule_id"],
            "text": f"{conditions} → {conclusion}"
        })

    return reasoning