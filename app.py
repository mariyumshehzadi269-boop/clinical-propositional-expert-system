import streamlit as st

from propositions import create_patient_facts
from rules import RULES
from inference_engine import forward_chain

from clinical_outputs import (
    CONDITION_FACTS,
    TEST_FACTS,
    REVIEW_FACTS,
    format_reasoning_trace
)

from clinical_information import (
    TEST_INFORMATION,
    MEDICATION_INFORMATION
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Clinical Decision Support System",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🩺 Intelligent Clinical Decision Support System")

st.markdown(
    """
    **Propositional Logic + Forward-Chaining Expert System**

    This system processes patient information using a rule-based
    propositional inference engine to generate clinical decision-support
    information for clinician review.
    """
)

st.warning(
    "⚠️ This system is a clinical decision-support prototype. "
    "It does not replace professional medical diagnosis or treatment."
)


# ============================================================
# PATIENT INFORMATION
# ============================================================

st.header("👤 Patient Information")

col1, col2, col3 = st.columns(3)

with col1:
    patient_id = st.text_input(
        "Patient ID",
        placeholder="e.g. PT-001"
    )

with col2:
    age = st.number_input(
        "Age (years)",
        min_value=0,
        max_value=120,
        value=25
    )

with col3:
    gender = st.selectbox(
        "Gender",
        ["Female", "Male", "Other", "Prefer not to say"]
    )


col1, col2, col3 = st.columns(3)

with col1:
    weight = st.number_input(
        "Weight (kg)",
        min_value=0.0,
        max_value=300.0,
        value=60.0,
        step=0.1
    )

with col2:
    height = st.number_input(
        "Height (cm)",
        min_value=0.0,
        max_value=250.0,
        value=165.0,
        step=0.1
    )

with col3:
    symptom_duration = st.number_input(
        "Symptom duration (days)",
        min_value=0,
        max_value=365,
        value=1
    )

main_complaint = st.text_area(
    "Main Complaint",
    placeholder="Describe the patient's main complaint..."
)


# ============================================================
# SYMPTOMS
# ============================================================

st.header("🩹 Symptoms")

st.markdown("Select the symptoms currently reported by the patient.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    headache = st.checkbox("Headache")
    sore_throat = st.checkbox("Sore throat")
    fatigue = st.checkbox("Fatigue")

with col2:
    body_aches = st.checkbox("Body aches")
    runny_nose = st.checkbox("Runny nose")
    shortness_of_breath = st.checkbox("Shortness of breath")
    chest_pain = st.checkbox("Chest pain")
    nausea = st.checkbox("Nausea")

with col3:
    vomiting = st.checkbox("Vomiting")
    diarrhea = st.checkbox("Diarrhea")
    abdominal_pain = st.checkbox("Abdominal pain")
    dizziness = st.checkbox("Dizziness")
    chills = st.checkbox("Chills")

with col4:
    rash = st.checkbox("Rash")
    joint_pain = st.checkbox("Joint pain")
    weakness = st.checkbox("Weakness")
    loss_of_appetite = st.checkbox("Loss of appetite")
    sweating = st.checkbox("Sweating")


# ============================================================
# MEDICAL HISTORY
# ============================================================

st.header("📋 Medical History")

col1, col2, col3, col4 = st.columns(4)

with col1:
    diabetes = st.checkbox("Diabetes")
    hypertension = st.checkbox("Hypertension")

with col2:
    asthma = st.checkbox("Asthma")
    heart_disease = st.checkbox("Heart disease")

with col3:
    kidney_disease = st.checkbox("Kidney disease")
    liver_disease = st.checkbox("Liver disease")

with col4:
    drug_allergy = st.checkbox("Drug allergy")
    smoking = st.checkbox("Smoking history")


# ============================================================
# VITAL SIGNS
# ============================================================

st.header("❤️ Vital Signs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=30.0,
        max_value=45.0,
        value=37.0,
        step=0.1
    )

with col2:
    heart_rate = st.number_input(
        "Heart Rate (bpm)",
        min_value=20,
        max_value=250,
        value=80
    )

with col3:
    respiratory_rate = st.number_input(
        "Respiratory Rate (/min)",
        min_value=5,
        max_value=60,
        value=16
    )

with col4:
    systolic_bp = st.number_input(
        "Systolic BP (mmHg)",
        min_value=50,
        max_value=250,
        value=120
    )

with col5:
    oxygen_saturation = st.number_input(
        "Oxygen Saturation (%)",
        min_value=50,
        max_value=100,
        value=98
    )


# ============================================================
# LABORATORY FINDINGS
# ============================================================

st.header("🧪 Laboratory Findings")

col1, col2, col3, col4 = st.columns(4)

with col1:
    wbc = st.number_input(
        "WBC",
        min_value=0.0,
        max_value=100.0,
        value=7.0,
        step=0.1
    )

with col2:
    crp = st.number_input(
        "CRP",
        min_value=0.0,
        max_value=500.0,
        value=2.0,
        step=0.1
    )

with col3:
    glucose = st.number_input(
        "Glucose",
        min_value=0.0,
        max_value=1000.0,
        value=100.0,
        step=1.0
    )

with col4:
    hemoglobin = st.number_input(
        "Hemoglobin",
        min_value=0.0,
        max_value=30.0,
        value=13.0,
        step=0.1
    )


# ============================================================
# ADDITIONAL CLINICAL NOTES
# ============================================================

st.header("📝 Additional Clinical Notes")

additional_notes = st.text_area(
    "Additional information",
    placeholder=(
        "Enter relevant clinical observations, previous findings, "
        "or other information..."
    )
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.divider()

analyze = st.button(
    "🔍 Analyze Patient",
    type="primary",
    use_container_width=True
)


# ============================================================
# VALIDATION
# ============================================================

if analyze:

    validation_errors = []

    if age < 1:
        validation_errors.append(
            "Please enter a valid patient age."
        )

    if weight <= 0:
        validation_errors.append(
            "Please enter a valid patient weight."
        )

    if height <= 0:
        validation_errors.append(
            "Please enter a valid patient height."
        )

    if symptom_duration < 0:
        validation_errors.append(
            "Symptom duration cannot be negative."
        )

    if oxygen_saturation < 50 or oxygen_saturation > 100:
        validation_errors.append(
            "Oxygen saturation must be between 50% and 100%."
        )

    if validation_errors:

        for error in validation_errors:
            st.error(error)

        st.stop()


    # ========================================================
    # CREATE PROPOSITIONS / PATIENT FACTS
    # ========================================================

    facts = create_patient_facts(

        fever=fever,
        cough=cough,
        headache=headache,
        sore_throat=sore_throat,
        fatigue=fatigue,
        body_aches=body_aches,
        runny_nose=runny_nose,
        shortness_of_breath=shortness_of_breath,
        chest_pain=chest_pain,
        nausea=nausea,
        vomiting=vomiting,
        diarrhea=diarrhea,
        abdominal_pain=abdominal_pain,
        dizziness=dizziness,
        chills=chills,
        rash=rash,
        joint_pain=joint_pain,
        weakness=weakness,
        loss_of_appetite=loss_of_appetite,
        sweating=sweating,

        diabetes=diabetes,
        hypertension=hypertension,
        asthma=asthma,
        heart_disease=heart_disease,
        kidney_disease=kidney_disease,
        liver_disease=liver_disease,
        drug_allergy=drug_allergy,
        smoking=smoking,

        temperature=temperature,
        heart_rate=heart_rate,
        respiratory_rate=respiratory_rate,
        systolic_bp=systolic_bp,
        oxygen_saturation=oxygen_saturation,

        wbc=wbc,
        crp=crp,
        glucose=glucose,
        hemoglobin=hemoglobin
    )


    # ========================================================
    # FORWARD CHAINING
    # ========================================================

    inferred_facts, fired_rules = forward_chain(
        facts,
        RULES
    )


    # ========================================================
    # PATIENT SUMMARY
    # ========================================================

    st.divider()

    st.header("📊 Clinical Assessment")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Patient Age",
            f"{age} years"
        )

    with col2:
        st.metric(
            "Symptom Duration",
            f"{symptom_duration} days"
        )

    with col3:
        st.metric(
            "Rules Triggered",
            len(fired_rules)
        )


    # ========================================================
    # POSSIBLE CONDITIONS
    # ========================================================

    st.subheader("🔎 Possible Conditions / Clinical Evaluations")

    condition_results = []

    for fact_name, description in CONDITION_FACTS.items():

        if fact_name in inferred_facts:
            condition_results.append(description)

    if condition_results:

        for result in condition_results:
            st.info(f"• {result}")

    else:
        st.success(
            "No predefined condition-related rule was triggered."
        )


    # ========================================================
    # TESTS
    # ========================================================

    st.subheader("🧪 Tests to Consider")

    test_results = []

    for fact_name, description in TEST_FACTS.items():

        if fact_name in inferred_facts:
            test_results.append(description)

    if test_results:

        for result in test_results:
            st.write(f"• {result}")

    else:
        st.write(
            "No predefined test recommendation was triggered."
        )


    # ========================================================
    # CLINICAL REVIEW
    # ========================================================

    st.subheader("⚕️ Clinical Review / Safety Information")

    review_results = []

    for fact_name, description in REVIEW_FACTS.items():

        if fact_name in inferred_facts:
            review_results.append(description)

    if review_results:

        for result in review_results:
            st.warning(f"• {result}")

    else:
        st.write(
            "No additional clinical review rule was triggered."
        )


    # ========================================================
    # TEST INFORMATION
    # ========================================================

    st.subheader("📚 Test Information")

    displayed_test_information = False

    for fact_name, information in TEST_INFORMATION.items():

        if fact_name in inferred_facts:

            displayed_test_information = True

            with st.expander(information["name"]):

                st.write(
                    f"**Purpose:** {information['purpose']}"
                )

                st.caption(
                    information["note"]
                )

    if not displayed_test_information:

        st.write(
            "No additional test information is available."
        )


    # ========================================================
    # MEDICATION INFORMATION
    # ========================================================

    st.subheader("💊 Medication Information")

    displayed_medication_information = False

    for fact_name, information in MEDICATION_INFORMATION.items():

        if fact_name in inferred_facts:

            displayed_medication_information = True

            with st.expander(information["category"]):

                st.write(
                    information["information"]
                )

                st.warning(
                    information["safety_note"]
                )

    if not displayed_medication_information:

        st.write(
            "No medication-related information was triggered."
        )


    # ========================================================
    # REASONING TRACE
    # ========================================================

    st.subheader("🧠 Propositional Logic Reasoning")

    reasoning_trace = format_reasoning_trace(
        fired_rules
    )

    if reasoning_trace:

        for step in reasoning_trace:

            st.code(
                f"{step['rule_id']}: {step['text']}",
                language="text"
            )

    else:

        st.info(
            "No inference rules were triggered."
        )


    # ========================================================
    # DERIVED PROPOSITIONS
    # ========================================================

    st.subheader("⚙️ Derived Propositions")

    derived_facts = [
        fact
        for fact in inferred_facts
        if fact not in facts
    ]

    if derived_facts:

        for fact in derived_facts:
            st.write(f"✓ `{fact}`")

    else:

        st.write(
            "No additional propositions were derived."
        )


    # ========================================================
    # TRUE INPUT FACTS
    # ========================================================

    with st.expander("View Patient Propositions"):

        true_facts = [
            fact
            for fact, value in facts.items()
            if value is True
        ]

        if true_facts:

            for fact in true_facts:
                st.write(f"✓ `{fact}`")

        else:

            st.write(
                "No positive patient propositions were recorded."
            )


    # ========================================================
    # FINAL SAFETY NOTICE
    # ========================================================

    st.divider()

    st.warning(
        """
        **Clinical Safety Notice**

        The outputs shown above are generated from predefined
        propositional rules. They represent decision-support
        information rather than a confirmed diagnosis.

        Final diagnosis, testing, medication selection, dosage,
        contraindications, and treatment decisions require assessment
        by a qualified healthcare professional.
        """
    )