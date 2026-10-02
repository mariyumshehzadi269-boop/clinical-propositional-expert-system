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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Clinical Decision Support System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM RESPONSIVE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- General page ---------- */

    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* ---------- Header ---------- */

    .app-header {
        padding: 1.4rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.2rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background: linear-gradient(
            135deg,
            rgba(240, 247, 255, 0.95),
            rgba(248, 251, 255, 0.95)
        );
    }

    .app-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .app-subtitle {
        font-size: 1rem;
        opacity: 0.75;
        margin-bottom: 0;
    }

    /* ---------- Section cards ---------- */

    .section-card {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.55);
    }

    /* ---------- Result cards ---------- */

    .result-card {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        margin-bottom: 0.75rem;
        background: rgba(250, 250, 250, 0.75);
    }

    .result-title {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }

    .result-description {
        font-size: 0.9rem;
        opacity: 0.78;
    }

    /* ---------- Analyze button ---------- */

    div.stButton > button {
        width: 100%;
        min-height: 3rem;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
    }

    /* ---------- Mobile ---------- */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
            padding-top: 0.5rem;
        }

        .app-header {
            padding: 1rem;
            border-radius: 12px;
        }

        .app-title {
            font-size: 1.45rem;
            line-height: 1.25;
        }

        .app-subtitle {
            font-size: 0.85rem;
        }

        .section-card {
            padding: 0.85rem;
            border-radius: 11px;
        }

        .result-card {
            padding: 0.85rem;
        }

        h1 {
            font-size: 1.45rem !important;
        }

        h2 {
            font-size: 1.25rem !important;
        }

        h3 {
            font-size: 1.1rem !important;
        }

        /* Make inputs comfortable on mobile */

        input,
        textarea,
        select {
            font-size: 16px !important;
        }

        /* Full-width buttons */

        div.stButton > button {
            min-height: 3.2rem;
        }

        /* Reduce excessive vertical spacing */

        [data-testid="stVerticalBlock"] {
            gap: 0.65rem;
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
    <div class="app-header">
        <div class="app-title">
            🩺 Intelligent Clinical Decision Support System
        </div>
        <div class="app-subtitle">
            Propositional Logic & Forward-Chaining Expert System
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "Clinical decision-support tool for educational and clinician-review purposes. "
    "It does not provide an autonomous medical diagnosis or prescription."
)


# ============================================================
# PATIENT INFORMATION
# ============================================================

with st.expander("👤 Patient Information", expanded=True):

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        patient_id = st.text_input(
            "Patient ID",
            placeholder="Enter patient ID",
        )

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=25,
            step=1,
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"],
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=300.0,
            value=60.0,
            step=0.5,
        )

    with col2:
        height = st.number_input(
            "Height (cm)",
            min_value=0.0,
            max_value=250.0,
            value=165.0,
            step=0.5,
        )

        symptom_duration = st.number_input(
            "Symptom duration (days)",
            min_value=0,
            max_value=365,
            value=1,
            step=1,
        )

        main_complaint = st.text_input(
            "Main complaint",
            placeholder="e.g. fever and cough",
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# SYMPTOMS
# ============================================================

SYMPTOMS = [
    ("fever", "Fever"),
    ("cough", "Cough"),
    ("headache", "Headache"),
    ("sore_throat", "Sore throat"),
    ("fatigue", "Fatigue"),
    ("body_aches", "Body aches"),
    ("runny_nose", "Runny nose"),
    ("shortness_of_breath", "Shortness of breath"),
    ("chest_pain", "Chest pain"),
    ("nausea", "Nausea"),
    ("vomiting", "Vomiting"),
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

with st.expander("🩹 Symptoms", expanded=True):

    symptom_values = {}

    # Four columns on desktop.
    # Streamlit automatically stacks these appropriately on narrow screens.
    cols = st.columns(4)

    for index, (key, label) in enumerate(SYMPTOMS):
        with cols[index % 4]:
            symptom_values[key] = st.checkbox(label)


# ============================================================
# MEDICAL HISTORY
# ============================================================

HISTORY = [
    ("diabetes", "Diabetes"),
    ("hypertension", "Hypertension"),
    ("asthma", "Asthma"),
    ("heart_disease", "Heart disease"),
    ("kidney_disease", "Kidney disease"),
    ("liver_disease", "Liver disease"),
    ("drug_allergy", "Drug allergy"),
    ("smoking", "Smoking"),
]

with st.expander("📋 Medical History", expanded=False):

    history_values = {}

    cols = st.columns(2)

    for index, (key, label) in enumerate(HISTORY):
        with cols[index % 2]:
            history_values[key] = st.checkbox(label)


# ============================================================
# VITAL SIGNS
# ============================================================

with st.expander("❤️ Vital Signs", expanded=False):

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
            "Heart rate (bpm)",
            min_value=30,
            max_value=250,
            value=75,
            step=1,
        )

        respiratory_rate = st.number_input(
            "Respiratory rate (/min)",
            min_value=5,
            max_value=80,
            value=16,
            step=1,
        )

    with vital_col2:

        systolic_bp = st.number_input(
            "Systolic blood pressure (mmHg)",
            min_value=50,
            max_value=250,
            value=120,
            step=1,
        )

        oxygen_saturation = st.number_input(
            "Oxygen saturation (%)",
            min_value=50.0,
            max_value=100.0,
            value=98.0,
            step=0.1,
        )


# ============================================================
# LABORATORY FINDINGS
# ============================================================

with st.expander("🧪 Laboratory Findings", expanded=False):

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


# ============================================================
# ADDITIONAL NOTES
# ============================================================

with st.expander("📝 Additional Clinical Notes", expanded=False):

    additional_notes = st.text_area(
        "Notes",
        placeholder=(
            "Enter any additional clinical information..."
        ),
        height=120,
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("### 🔍 Clinical Analysis")

analyze = st.button(
    "Analyze Patient",
    type="primary",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if age < 1:
        st.error("Analysis cannot proceed. Please enter a valid patient age.")
        st.stop()

    if weight <= 0:
        st.error("Please enter a valid patient weight.")
        st.stop()

    if height <= 0:
        st.error("Please enter a valid patient height.")
        st.stop()

    if symptom_duration < 0:
        st.error("Please enter a valid symptom duration.")
        st.stop()

    if oxygen_saturation < 50 or oxygen_saturation > 100:
        st.error("Please enter a valid oxygen saturation value.")
        st.stop()

    # --------------------------------------------------------
    # CREATE PROPOSITIONAL FACTS
    # --------------------------------------------------------

    facts = create_patient_facts(
        fever=symptom_values["fever"],
        cough=symptom_values["cough"],
        headache=symptom_values["headache"],
        sore_throat=symptom_values["sore_throat"],
        fatigue=symptom_values["fatigue"],
        body_aches=symptom_values["body_aches"],
        runny_nose=symptom_values["runny_nose"],
        shortness_of_breath=symptom_values["shortness_of_breath"],
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
        loss_of_appetite=symptom_values["loss_of_appetite"],
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

    # --------------------------------------------------------
    # FORWARD CHAINING
    # --------------------------------------------------------

    inferred_facts, fired_rules = forward_chain(
        facts,
        RULES,
    )

    # --------------------------------------------------------
    # RESULTS HEADER
    # --------------------------------------------------------

    st.divider()

    st.header("📊 Clinical Assessment")

    st.caption(
        f"Patient: {patient_id if patient_id else 'Not specified'}"
    )

    # --------------------------------------------------------
    # RESULT METRICS
    # --------------------------------------------------------

    condition_count = sum(
        1
        for fact in CONDITION_FACTS
        if fact in inferred_facts
    )

    test_count = sum(
        1
        for fact in TEST_FACTS
        if fact in inferred_facts
    )

    review_count = sum(
        1
        for fact in REVIEW_FACTS
        if fact in inferred_facts
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Possible conditions",
            condition_count,
        )

    with metric2:
        st.metric(
            "Tests to consider",
            test_count,
        )

    with metric3:
        st.metric(
            "Clinical reviews",
            review_count,
        )

    # --------------------------------------------------------
    # POSSIBLE CONDITIONS
    # --------------------------------------------------------

    st.subheader("🩺 Possible Conditions / Clinical Evaluations")

    condition_results = [
        description
        for fact, description in CONDITION_FACTS.items()
        if fact in inferred_facts
    ]

    if condition_results:

        for result in condition_results:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-title">🩺 {result}</div>
                    <div class="result-description">
                        Derived from the configured propositional rules.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.info(
            "No condition-related propositions were derived "
            "from the current inputs."
        )

    # --------------------------------------------------------
    # TESTS
    # --------------------------------------------------------

    st.subheader("🧪 Tests to Consider")

    test_results = [
        (fact, description)
        for fact, description in TEST_FACTS.items()
        if fact in inferred_facts
    ]

    if test_results:

        for fact, description in test_results:

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-title">🧪 {description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if fact in TEST_INFORMATION:

                information = TEST_INFORMATION[fact]

                with st.expander(
                    f"Information: {information['name']}"
                ):
                    st.write(
                        f"**Purpose:** {information['purpose']}"
                    )
                    st.caption(
                        information["note"]
                    )

    else:
        st.info(
            "No test-related propositions were derived."
        )

    # --------------------------------------------------------
    # CLINICAL REVIEW / SAFETY
    # --------------------------------------------------------

    st.subheader("⚕️ Clinical Review / Safety")

    review_results = [
        (fact, description)
        for fact, description in REVIEW_FACTS.items()
        if fact in inferred_facts
    ]

    if review_results:

        for fact, description in review_results:

            st.warning(description)

            if fact in MEDICATION_INFORMATION:

                medication = MEDICATION_INFORMATION[fact]

                with st.expander(
                    f"Medication information: {medication['category']}"
                ):

                    st.write(
                        medication["information"]
                    )

                    st.caption(
                        f"Safety note: {medication['safety_note']}"
                    )

    else:

        st.success(
            "No additional clinical-review propositions "
            "were triggered by the configured rules."
        )

    # --------------------------------------------------------
    # REASONING TRACE
    # --------------------------------------------------------

    st.subheader("🔎 Propositional Logic Reasoning")

    reasoning_trace = format_reasoning_trace(
        fired_rules
    )

    if reasoning_trace:

        for step in reasoning_trace:

            with st.expander(
                f"Rule {step['rule_id']}"
            ):
                st.code(
                    step["text"],
                    language="text",
                )

    else:

        st.info(
            "No reasoning steps were generated."
        )

    # --------------------------------------------------------
    # DERIVED PROPOSITIONS
    # --------------------------------------------------------

    st.subheader("🧠 Derived Propositions")

    derived = [
        fact
        for fact in inferred_facts
        if fact not in facts
    ]

    if derived:

        st.write(
            ", ".join(derived)
        )

    else:

        st.info(
            "No additional propositions were derived."
        )

    # --------------------------------------------------------
    # PATIENT PROPOSITIONS
    # --------------------------------------------------------

    with st.expander("📋 Patient Propositions"):

        true_patient_facts = [
            fact
            for fact, value in facts.items()
            if value is True
        ]

        if true_patient_facts:

            for fact in true_patient_facts:
                st.write(f"• {fact}")

        else:

            st.info(
                "No positive patient propositions were recorded."
            )

    # --------------------------------------------------------
    # FINAL SAFETY NOTICE
    # --------------------------------------------------------

    st.divider()

    st.warning(
        """
        **Clinical safety notice**

        This system is an educational clinical decision-support
        prototype based on propositional logic and forward chaining.

        Its outputs represent rule-derived possibilities and
        considerations. They must not be treated as a definitive
        diagnosis, prescription, or substitute for professional
        clinical judgment.

        Medication selection, dosing, contraindications,
        interactions, testing decisions, and patient management
        require assessment by a qualified healthcare professional.
        """
    )