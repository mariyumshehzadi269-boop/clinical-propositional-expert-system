RULES = [

    {
        "id": "R1",
        "conditions": [
            "fever",
            "cough",
            "sore_throat"
        ],
        "conclusion": "influenza_candidate"
    },

    {
        "id": "R2",
        "conditions": [
            "fever",
            "cough",
            "body_aches"
        ],
        "conclusion": "influenza_candidate"
    },

    {
        "id": "R3",
        "conditions": [
            "fever",
            "cough",
            "runny_nose"
        ],
        "conclusion": "viral_respiratory_candidate"
    },

    {
        "id": "R4",
        "conditions": [
            "cough",
            "sore_throat",
            "runny_nose"
        ],
        "conclusion": "upper_respiratory_candidate"
    },

    {
        "id": "R5",
        "conditions": [
            "cough",
            "shortness_of_breath",
            "low_oxygen"
        ],
        "conclusion": "urgent_respiratory_evaluation"
    },

    {
        "id": "R6",
        "conditions": [
            "shortness_of_breath",
            "chest_pain"
        ],
        "conclusion": "respiratory_evaluation"
    },

    {
        "id": "R7",
        "conditions": [
            "vomiting",
            "diarrhea",
            "abdominal_pain"
        ],
        "conclusion": "gastrointestinal_candidate"
    },

    {
        "id": "R8",
        "conditions": [
            "nausea",
            "vomiting",
            "diarrhea"
        ],
        "conclusion": "gastrointestinal_candidate"
    },

    {
        "id": "R9",
        "conditions": [
            "fever",
            "elevated_wbc"
        ],
        "conclusion": "infection_evaluation"
    },

    {
        "id": "R10",
        "conditions": [
            "fever",
            "elevated_crp"
        ],
        "conclusion": "inflammatory_evaluation"
    },

    {
        "id": "R11",
        "conditions": [
            "influenza_candidate"
        ],
        "conclusion": "consider_influenza_test"
    },

    {
        "id": "R12",
        "conditions": [
            "viral_respiratory_candidate"
        ],
        "conclusion": "consider_viral_testing"
    },

    {
        "id": "R13",
        "conditions": [
            "infection_evaluation"
        ],
        "conclusion": "consider_cbc"
    },

    {
        "id": "R14",
        "conditions": [
            "inflammatory_evaluation"
        ],
        "conclusion": "consider_crp_review"
    },

    {
        "id": "R15",
        "conditions": [
            "respiratory_evaluation"
        ],
        "conclusion": "consider_chest_xray"
    },

    {
        "id": "R16",
        "conditions": [
            "high_fever"
        ],
        "conclusion": "consider_fever_management"
    },

    {
        "id": "R17",
        "conditions": [
            "influenza_candidate"
        ],
        "conclusion": "consider_clinician_review_for_antiviral"
    }
]