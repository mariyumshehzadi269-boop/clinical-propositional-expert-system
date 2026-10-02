import streamlit as st

from propositions import create_patient_facts
from rules import RULES
from inference_engine import forward_chain
from clinical_outputs import (
    CONDITION_FACTS,
    TEST_FACTS,
    REVIEW_FACTS,
    format_reasoning_trace,
)
from clinical_information import (
    TEST_INFORMATION,
    MEDICATION_INFORMATION,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Intelligent Clinical Decision System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #f5f9fd;
    }

    .block-container {
        max-width: 1500px;
        padding: 0.8rem 1.2rem 2rem 1.2rem;
    }

    /* ========================================================
       HEADER
       ======================================================== */

    .top-header {
        background: linear-gradient(135deg, #174b91, #2878d7);
        padding: 1rem 1.5rem;
        border-radius: 0 0 12px 12px;
        margin: -0.8rem -1.2rem 1.2rem -1.2rem;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 3px 12px rgba(0, 60, 120, 0.18);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .header-icon {
        font-size: 3rem;
        line-height: 1;
    }

    .header-title {
        font-size: 1.9rem;
        font-weight: 700;
        line-height: 1.15;
    }

    .header-subtitle {
        font-size: 0.95rem;
        margin-top: 0.25rem;
        opacity: 0.95;
    }

    .header-right {
        font-size: 0.85rem;
        opacity: 0.95;
        white-space: nowrap;
    }

    /* ========================================================
       MAIN PANELS
       ======================================================== */

    .main-panel {
        background: white;
        border: 1px solid #c9dced;
        border-radius: 9px;
        padding: 0.8rem;
        box-shadow: 0 2px 8px rgba(30, 80, 130, 0.05);
    }

    /* ========================================================
       SECTION CARDS
       ======================================================== */

    .clinical-card {
        background: linear-gradient(
            135deg,
            #f7fbff,
            #eef7ff
        );
        border: 1px solid #c7def4;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.75rem;
    }

    .clinical-card-title {
        color: #12366b;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }

    /* ========================================================
       RESULT CARDS
       ======================================================== */

    .result-success {
        background: #edfbf5;
        border: 1px solid #a9e6d0;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
    }

    .result-condition {
        background: #fff4f5;
        border: 1px solid #ffb6c0;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
    }

    .result-tests {
        background: #eef7ff;
        border: 1px solid #9ed0ff;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
    }

    .result-medication {
        background: #effaf7;
        border: 1px solid #9edfc9;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
    }

    .result-rules {
        background: #f6f2ff;
        border: 1px solid #c9b8ff;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
    }

    .result-notice {
        background: #fff9e9;
        border: 1px solid #f5d68b;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.8rem;
    }

    .result-heading {
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    /* ========================================================
       ANALYZE BUTTON
       ======================================================== */

    div.stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border-radius: 8px;
        font-size: 1.05rem;
        font-weight: 700;
    }

    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        font-weight: 600;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 0.7rem;
            padding-right: 0.7rem;
        }

        .top-header {
            margin-left: -0.7rem;
            margin-right: -0.7rem;
            padding: 0.85rem 1rem;
        }

        .header-icon {
            font-size: 2.2rem;
        }

        .header-title {
            font-size: 1.35rem;
        }

        .header-subtitle {
            font-size: 0.78rem;
        }

        .header-right {
            display: none;
        }

        .main-panel {
            padding: 0.55rem;
        }

        .clinical-card {
            padding: 0.7rem;
        }

        .clinical-card-title {
            font-size: 1rem;
        }

        .result-heading {
            font-size: 0.98rem;
        }

        div.stButton > button {
            min-height: 3.4rem;
        }
    }

    /* ========================================================
       SMALL MOBILE
       ======================================================== */

    @media (max-width: 600px) {

        .header-left {
            gap: 0.6rem;
        }

        .header-icon {
            font-size: 1.9rem;
        }

        .header-title {
            font-size: 1.15rem;
        }

        .header-subtitle {
            font-size: 0.7rem;
        }

        .block-container {
            padding-top: 0.4rem;
        }

        h1 {
            font-size: 1.35rem !important;
        }

        h2 {
            font-size: 1.15rem !important;
        }

        h3 {
            font-size: 1rem !important;
        }

        input,
        textarea,
        select {
            font-size: 16px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="top-header">

        <div class="header-left">

            <div class="header-icon">🩺</div>

            <div>
                <div class="header-title">
                    Intelligent Clinical Decision System
                </div>

                <div class="header-subtitle">
                    Propositional Logic Based Expert System for Decision Support
                </div>
            </div>

        </div>

        <div class="header-right">
            Better Decisions &nbsp; | &nbsp; Healthier Tomorrows
            &nbsp;&nbsp; ❤️
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MAIN LAYOUT
# ============================================================

left_panel, right_panel = st.columns(
    [1, 2],
    gap="medium",
)


# ============================================================
# LEFT PANEL — PATIENT INPUT
# ============================================================

with left_panel:

    st.markdown(
        '<div class="main-panel">',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="clinical-card">
            <div class="clinical-card-title">
                👤 Patient Information
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    patient_col1, patient_col2 = st.columns(2)

    with patient_col1:

        patient_id = st.text_input(
            "Patient ID",
            placeholder="ID",
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=25,
            step=1,
        )

    with patient_col2:

        gender = st.selectbox(
            "Sex",
            [
                "Female",
                "Male",
                "Other",
                "Prefer not to say",
            ],
        )

        symptom_duration = st.number_input(
            "Symptom duration (days)",
            min_value=0,
            max_value=365,
            value=1,
            step=1,
        )


    # ========================================================
    # SYMPTOMS
    # ========================================================

    st.markdown(
        """
        <div class="clinical-card">
            <div class="clinical-card-title">
                🧑‍⚕️ Symptoms
            </div>
        """,
        unsafe_allow_html=True,
    )

    symptoms = [
        ("fever", "Fever"),
        ("cough", "Cough"),
        ("sore_throat", "Sore throat"),
        ("headache", "Headache"),
        ("shortness_of_breath", "Shortness of breath"),
        ("vomiting", "Vomiting"),
        ("chest_pain", "Chest pain"),
        ("fatigue", "Fatigue"),
        ("body_aches", "Body aches"),
        ("runny_nose", "Runny nose"),
        ("nausea", "Nausea"),
        ("diarrhea", "Diarrhea"),
        ("abdominal_pain", "Abdominal pain"),
        ("dizziness", "Dizziness"),
        ("chills", "Chills"),
        ("rash", "Rash"),
        ("joint_pain", "Joint pain"),
        ("weakness", "Weakness"),
        ("loss_of_appetite", "Loss of appetite"),
        ("sweating", "Sweating"),
    ]

    symptom_values = {}

    symptom_cols = st.columns(2)

    for index, (key, label) in enumerate(symptoms):

        with symptom_cols[index % 2]:

            symptom_values[key] = st.checkbox(
                label,
                key=f"symptom_{key}",
            )

    st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # MEDICAL HISTORY
    # ========================================================

    st.markdown(
        """
        <div class="clinical-card">
            <div class="clinical-card-title">
                🏥 Medical History
            </div>
        """,
        unsafe_allow_html=True,
    )

    history = [
        ("diabetes", "Diabetes"),
        ("asthma", "Asthma"),
        ("hypertension", "Hypertension"),
        ("heart_disease", "Heart disease"),
        ("kidney_disease", "Kidney disease"),
        ("liver_disease", "Liver disease"),
        ("drug_allergy", "Drug allergy"),
        ("smoking", "Smoking"),
    ]

    history_values = {}

    history_cols = st.columns(2)

    for index, (key, label) in enumerate(history):

        with history_cols[index % 2]:

            history_values[key] = st.checkbox(
                label,
                key=f"history_{key}",
            )

    st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # VITAL SIGNS
    # ========================================================

    st.markdown(
        """
        <div class="clinical-card">
            <div class="clinical-card-title">
                ❤️ Vital Signs
            </div>
        """,
        unsafe_allow_html=True,
    )

    vital_col1, vital_col2 = st.columns(2)

    with vital_col1:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=30.0,
            max_value=45.0,
            value=37.0,
            step=0.1,
        )

        heart_rate = st.number_input(
            "Heart Rate (bpm)",
            min_value=30,
            max_value=250,
            value=75,
            step=1,
        )

        respiratory_rate = st.number_input(
            "Respiratory Rate (/min)",
            min_value=5,
            max_value=80,
            value=16,
            step=1,
        )

    with vital_col2:

        systolic_bp = st.number_input(
            "Systolic BP (mmHg)",
            min_value=50,
            max_value=250,
            value=120,
            step=1,
        )

        oxygen_saturation = st.number_input(
            "Oxygen Saturation (%)",
            min_value=50.0,
            max_value=100.0,
            value=98.0,
            step=0.1,
        )

    st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # ADDITIONAL DATA
    # ========================================================

    with st.expander("🧪 Laboratory Findings & Clinical Notes"):

        lab_col1, lab_col2 = st.columns(2)

        with lab_col1:

            wbc = st.number_input(
                "WBC",
                min_value=0.0,
                max_value=100.0,
                value=7.0,
                step=0.1,
            )

            crp = st.number_input(
                "CRP",
                min_value=0.0,
                max_value=500.0,
                value=3.0,
                step=0.1,
            )

        with lab_col2:

            glucose = st.number_input(
                "Glucose",
                min_value=0.0,
                max_value=1000.0,
                value=100.0,
                step=1.0,
            )

            hemoglobin = st.number_input(
                "Hemoglobin",
                min_value=0.0,
                max_value=30.0,
                value=13.0,
                step=0.1,
            )

        additional_notes = st.text_area(
            "Additional Clinical Notes",
            placeholder="Enter additional information...",
            height=100,
        )


    # ========================================================
    # MAIN ANALYZE BUTTON
    # ========================================================

    analyze = st.button(
        "🔍  Analyze Patient",
        type="primary",
        use_container_width=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# RIGHT PANEL — RESULTS
# ============================================================

with right_panel:

    st.markdown(
        '<div class="main-panel">',
        unsafe_allow_html=True,
    )

    results_tab, rules_tab, explanation_tab, summary_tab = st.tabs(
        [
            "📄 Results",
            "🔗 Logic Rules Fired",
            "💡 Explanation",
            "📋 Patient Summary",
        ]
    )


    # ========================================================
    # DEFAULT STATE
    # ========================================================

    if not analyze:

        with results_tab:

            st.markdown(
                """
                <div class="result-success">

                    <div class="result-heading">
                        👋 Ready for Analysis
                    </div>

                    Enter the patient's information on the left
                    and click <b>Analyze Patient</b> to generate
                    rule-based clinical decision-support results.

                </div>
                """,
                unsafe_allow_html=True,
            )

        with rules_tab:

            st.info(
                "Logic rules will appear here after patient analysis."
            )

        with explanation_tab:

            st.info(
                "The reasoning explanation will appear here after analysis."
            )

        with summary_tab:

            st.info(
                "The patient summary will appear here after analysis."
            )


    # ========================================================
    # RUN ANALYSIS
    # ========================================================

    else:

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if age < 1:

            st.error(
                "Analysis cannot proceed. Please enter a valid patient age."
            )
            st.stop()

        if oxygen_saturation < 50 or oxygen_saturation > 100:

            st.error(
                "Please enter a valid oxygen saturation value."
            )
            st.stop()

        # ----------------------------------------------------
        # CREATE FACTS
        # ----------------------------------------------------

        facts = create_patient_facts(

            fever=symptom_values["fever"],
            cough=symptom_values["cough"],
            headache=symptom_values["headache"],
            sore_throat=symptom_values["sore_throat"],
            fatigue=symptom_values["fatigue"],
            body_aches=symptom_values["body_aches"],
            runny_nose=symptom_values["runny_nose"],
            shortness_of_breath=symptom_values[
                "shortness_of_breath"
            ],
            chest_pain=symptom_values["chest_pain"],
            nausea=symptom_values["nausea"],
            vomiting=symptom_values["vomiting"],
            diarrhea=symptom_values["diarrhea"],
            abdominal_pain=symptom_values["abdominal_pain"],
            dizziness=symptom_values["dizziness"],
            chills=symptom_values["chills"],
            rash=symptom_values["rash"],
            joint_pain=symptom_values["joint_pain"],
            weakness=symptom_values["weakness"],
            loss_of_appetite=symptom_values[
                "loss_of_appetite"
            ],
            sweating=symptom_values["sweating"],

            diabetes=history_values["diabetes"],
            hypertension=history_values["hypertension"],
            asthma=history_values["asthma"],
            heart_disease=history_values["heart_disease"],
            kidney_disease=history_values["kidney_disease"],
            liver_disease=history_values["liver_disease"],
            drug_allergy=history_values["drug_allergy"],
            smoking=history_values["smoking"],

            temperature=temperature,
            heart_rate=heart_rate,
            respiratory_rate=respiratory_rate,
            systolic_bp=systolic_bp,
            oxygen_saturation=oxygen_saturation,

            wbc=wbc,
            crp=crp,
            glucose=glucose,
            hemoglobin=hemoglobin,
        )

        # ----------------------------------------------------
        # FORWARD CHAINING
        # ----------------------------------------------------

        inferred_facts, fired_rules = forward_chain(
            facts,
            RULES,
        )

        # ----------------------------------------------------
        # DERIVED CONDITIONS
        # ----------------------------------------------------

        condition_results = [
            description
            for fact, description in CONDITION_FACTS.items()
            if fact in inferred_facts
        ]

        test_results = [
            (fact, description)
            for fact, description in TEST_FACTS.items()
            if fact in inferred_facts
        ]

        review_results = [
            (fact, description)
            for fact, description in REVIEW_FACTS.items()
            if fact in inferred_facts
        ]

        reasoning_trace = format_reasoning_trace(
            fired_rules
        )

        derived_facts = [
            fact
            for fact in inferred_facts
            if fact not in facts
        ]


        # ====================================================
        # RESULTS TAB
        # ====================================================

        with results_tab:

            st.markdown(
                """
                <div class="result-success">

                    <div class="result-heading">
                        🟢 Analysis Complete
                    </div>

                    Based on the provided information,
                    the system has generated the following
                    rule-derived clinical considerations.

                </div>
                """,
                unsafe_allow_html=True,
            )


            # ------------------------------------------------
            # CONDITIONS
            # ------------------------------------------------

            st.markdown(
                """
                <div class="result-condition">

                    <div class="result-heading">
                        🩺 Possible Condition(s) / Clinical Evaluations
                    </div>
                """,
                unsafe_allow_html=True,
            )

            if condition_results:

                for number, result in enumerate(
                    condition_results,
                    start=1,
                ):

                    st.markdown(
                        f"{number}. **{result}**"
                    )

            else:

                st.write(
                    "No condition-related propositions were derived."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


            # ------------------------------------------------
            # TESTS
            # ------------------------------------------------

            st.markdown(
                """
                <div class="result-tests">

                    <div class="result-heading">
                        🧪 Recommended Tests to Consider
                    </div>
                """,
                unsafe_allow_html=True,
            )

            if test_results:

                for fact, description in test_results:

                    st.markdown(
                        f"• **{description}**"
                    )

                    if fact in TEST_INFORMATION:

                        information = TEST_INFORMATION[fact]

                        st.caption(
                            f"Purpose: {information['purpose']}"
                        )

            else:

                st.write(
                    "No test-related propositions were derived."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


            # ------------------------------------------------
            # MEDICATION / CLINICAL REVIEW
            # ------------------------------------------------

            st.markdown(
                """
                <div class="result-medication">

                    <div class="result-heading">
                        💊 Medication Information
                        (for Clinician Review)
                    </div>
                """,
                unsafe_allow_html=True,
            )

            medication_items = []

            for fact, description in review_results:

                if fact in MEDICATION_INFORMATION:

                    medication_items.append(
                        MEDICATION_INFORMATION[fact]
                    )

            if medication_items:

                for medication in medication_items:

                    st.markdown(
                        f"• **{medication['category']}**"
                    )

                    st.write(
                        medication["information"]
                    )

                    st.caption(
                        medication["safety_note"]
                    )

            else:

                st.write(
                    "No medication-related information was triggered."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


            # ------------------------------------------------
            # RULES FIRED SUMMARY
            # ------------------------------------------------

            st.markdown(
                """
                <div class="result-rules">

                    <div class="result-heading">
                        ⚙️ Rules That Fired
                    </div>
                """,
                unsafe_allow_html=True,
            )

            if fired_rules:

                for rule in fired_rules:

                    conditions = " ∧ ".join(
                        rule["conditions"]
                    )

                    st.markdown(
                        f"• **{rule['rule_id']}**: "
                        f"`{conditions}` → "
                        f"`{rule['conclusion']}`"
                    )

            else:

                st.write(
                    "No rules were triggered."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


            # ------------------------------------------------
            # IMPORTANT NOTICE
            # ------------------------------------------------

            st.markdown(
                """
                <div class="result-notice">

                    <div class="result-heading">
                        ⚠️ Important Notice
                    </div>

                    This system provides decision support
                    based on predefined propositional rules
                    and does not replace professional medical
                    judgment.

                    <br><br>

                    Always consult a qualified healthcare
                    professional for final diagnosis and
                    treatment decisions.

                </div>
                """,
                unsafe_allow_html=True,
            )


        # ====================================================
        # LOGIC RULES TAB
        # ====================================================

        with rules_tab:

            st.subheader("🔗 Logic Rules Fired")

            if fired_rules:

                for rule in fired_rules:

                    conditions = " AND ".join(
                        rule["conditions"]
                    )

                    st.markdown(
                        f"""
                        **{rule['rule_id']}**

                        `{conditions}`

                        ↓

                        `{rule['conclusion']}`
                        """
                    )

                    st.divider()

            else:

                st.info(
                    "No rules fired for the current patient data."
                )


        # ====================================================
        # EXPLANATION TAB
        # ====================================================

        with explanation_tab:

            st.subheader("💡 Explanation")

            if reasoning_trace:

                for step in reasoning_trace:

                    st.markdown(
                        f"**{step['rule_id']}**"
                    )

                    st.code(
                        step["text"],
                        language="text",
                    )

            else:

                st.info(
                    "No reasoning steps were generated."
                )

            st.subheader("🧠 Derived Propositions")

            if derived_facts:

                for fact in derived_facts:

                    st.write(
                        f"• `{fact}`"
                    )

            else:

                st.info(
                    "No additional propositions were derived."
                )


        # ====================================================
        # PATIENT SUMMARY TAB
        # ====================================================

        with summary_tab:

            st.subheader("📋 Patient Summary")

            summary_col1, summary_col2 = st.columns(2)

            with summary_col1:

                st.write(
                    f"**Patient ID:** "
                    f"{patient_id or 'Not specified'}"
                )

                st.write(
                    f"**Age:** {age}"
                )

                st.write(
                    f"**Sex:** {gender}"
                )

                st.write(
                    f"**Symptom duration:** "
                    f"{symptom_duration} day(s)"
                )

            with summary_col2:

                st.write(
                    f"**Temperature:** "
                    f"{temperature} °C"
                )

                st.write(
                    f"**Heart rate:** "
                    f"{heart_rate} bpm"
                )

                st.write(
                    f"**Respiratory rate:** "
                    f"{respiratory_rate} /min"
                )

                st.write(
                    f"**Oxygen saturation:** "
                    f"{oxygen_saturation}%"
                )


            st.subheader("Positive Symptoms")

            positive_symptoms = [
                label
                for key, label in symptoms
                if symptom_values[key]
            ]

            if positive_symptoms:

                st.write(
                    ", ".join(positive_symptoms)
                )

            else:

                st.write(
                    "No positive symptoms selected."
                )


            st.subheader("Medical History")

            positive_history = [
                label
                for key, label in history
                if history_values[key]
            ]

            if positive_history:

                st.write(
                    ", ".join(positive_history)
                )

            else:

                st.write(
                    "No relevant medical history selected."
                )


    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#66788a;
        font-size:0.78rem;
        margin-top:1rem;
    ">
        Intelligent Clinical Decision Support System
        &nbsp; • &nbsp;
        Propositional Logic & Forward Chaining
        &nbsp; • &nbsp;
        Educational / Clinical Review Prototype
    </div>
    """,
    unsafe_allow_html=True,
)