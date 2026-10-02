from inference_engine import forward_chain
from rules import RULES


TEST_CASE_1 = {

    "name": "Influenza-like respiratory case",

    "facts": {
        "fever": True,
        "cough": True,
        "sore_throat": True,
        "body_aches": True,

        "shortness_of_breath": False,
        "chest_pain": False,

        "nausea": False,
        "vomiting": False,
        "diarrhea": False,
        "abdominal_pain": False,

        "low_oxygen": False,
        "elevated_wbc": False,
        "elevated_crp": False,
        "high_fever": True
    },

    "expected_facts": [
        "influenza_candidate",
        "consider_influenza_test",
        "consider_clinician_review_for_antiviral",
        "consider_fever_management"
    ]
}


TEST_CASE_2 = {

    "name": "Gastrointestinal illness case",

    "facts": {
        "fever": False,
        "cough": False,
        "sore_throat": False,
        "body_aches": False,

        "shortness_of_breath": False,
        "chest_pain": False,

        "nausea": True,
        "vomiting": True,
        "diarrhea": True,
        "abdominal_pain": True,

        "low_oxygen": False,
        "elevated_wbc": False,
        "elevated_crp": False,
        "high_fever": False
    },

    "expected_facts": [
        "gastrointestinal_candidate"
    ]
}


TEST_CASE_3 = {

    "name": "Respiratory warning case",

    "facts": {
        "fever": True,
        "cough": True,
        "sore_throat": False,
        "body_aches": False,

        "shortness_of_breath": True,
        "chest_pain": False,

        "nausea": False,
        "vomiting": False,
        "diarrhea": False,
        "abdominal_pain": False,

        "low_oxygen": True,
        "elevated_wbc": False,
        "elevated_crp": False,
        "high_fever": True
    },

    "expected_facts": [
        "urgent_respiratory_evaluation",
        "consider_fever_management"
    ]
}


def run_test_case(test_case):

    inferred_facts, fired_rules = forward_chain(
        test_case["facts"],
        RULES
    )

    expected_facts = set(
        test_case["expected_facts"]
    )

    actual_facts = set(
        inferred_facts.keys()
    )

    passed = expected_facts.issubset(
        actual_facts
    )

    return {
        "name": test_case["name"],
        "passed": passed,
        "expected": expected_facts,
        "actual": actual_facts,
        "fired_rules": fired_rules
    }


if __name__ == "__main__":

    test_cases = [
        TEST_CASE_1,
        TEST_CASE_2,
        TEST_CASE_3
    ]

    print(
        "\n=== Clinical Expert System Test Suite ===\n"
    )

    for test_case in test_cases:

        result = run_test_case(
            test_case
        )

        if result["passed"]:
            print(
                f"PASS: {result['name']}"
            )
        else:
            print(
                f"FAIL: {result['name']}"
            )

        print(
            "Expected:",
            result["expected"]
        )

        print(
            "Derived:",
            result["actual"]
        )

        print()