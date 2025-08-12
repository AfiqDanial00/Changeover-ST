def main():
    translations = get_translations()
    load_css()
    logo = load_logo()

    with st.sidebar:
        st.markdown("### 🌐 Language Settings")
        lang = st.selectbox("Select Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
        lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
        t = translations[lang_code]

    header_html = f"""
    <div class='header-container'>
        <img src="https://www.sumiputeh.com.my/website/public/img/logo/01.png" class="logo">
        <h2 style="color: var(--sumiputeh-green);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-darkgreen);">{t['company']}</h4>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        with st.expander(f"### {t['changeover_details']}", expanded=True):
            date = st.date_input(t['date'], value=datetime.today())
            time_started_str = st.text_input(t['time_started'], value="08:00 AM")
            time_completed_str = st.text_input(t['time_completed'], value="08:30 AM")
            product_from = st.text_input(t['product_from'])
            product_to = st.text_input(t['product_to'])
            operator_name = st.text_input(t['operator'])

    with col2:
        with st.expander(f"### {t['documentation']}", expanded=True):
            remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

    # Capture checklist selections with keys
    length_checks = []
    with st.expander(f"### {t['length_adjustment']}", expanded=False):
        for i, step in enumerate(t['length_steps']):
            checked = st.checkbox(step, key=f"length_{i}")
            length_checks.append(checked)

    three_point_checks = []
    with st.expander(f"### {t['three_point_die']}", expanded=False):
        for i, step in enumerate(t['three_point_steps']):
            checked = st.checkbox(step, key=f"three_point_{i}")
            three_point_checks.append(checked)

    burring_checks = []
    with st.expander(f"### {t['burring_die']}", expanded=False):
        for i, step in enumerate(t['burring_steps']):
            checked = st.checkbox(step, key=f"burring_{i}")
            burring_checks.append(checked)

    # Load existing data
    try:
        df_all = pd.read_csv("checklist_records.csv", parse_dates=["Start_Time", "End_Time", "Timestamp"])
    except:
        df_all = pd.DataFrame()

    if not df_all.empty:
        st.markdown(f"### {t['summary']}")
        total_submissions = len(df_all)
        avg_duration = df_all["Duration_Minutes"].mean()
        st.write(f"**Total submissions:** {total_submissions}")
        st.write(f"**Average duration (minutes):** {avg_duration:.2f}")

    if not df_all.empty and len(df_all) > 5:
        df_display = df_all.iloc[:-5].copy()
    else:
        df_display = df_all.copy()

    if not df_display.empty:
        df_display["Start_Time"] = df_display["Start_Time"].dt.strftime("%I:%M %p")
        df_display["End_Time"] = df_display["End_Time"].dt.strftime("%I:%M %p")

    st.markdown(f"### {t['download']}")
    st.download_button(
        t['download'],
        data=df_all.to_csv(index=False),
        file_name="checklist_records.csv",
        mime="text/csv",
        use_container_width=True
    )

    if not df_display.empty:
        st.dataframe(df_display)

    # Submit button logic
    if st.button(f"✅ {t['submit']}", use_container_width=True):
        time_started = parse_time_input_ampm(time_started_str)
        time_completed = parse_time_input_ampm(time_completed_str)

        if not all([date, product_from.strip(), product_to.strip(), operator_name.strip()]):
            st.warning(t['warning'])
        elif not time_started or not time_completed:
            st.warning(t['invalid_time'])
        else:
            start_datetime = datetime.combine(date, time_started)
            end_datetime = datetime.combine(date, time_completed)

            if end_datetime < start_datetime:
                st.warning("⚠️ End time cannot be before start time.")
                return

            duration = end_datetime - start_datetime

            data = {
                "Date": [date],
                "Start_Time": [start_datetime],
                "End_Time": [end_datetime],
                "Duration_Minutes": [round(duration.total_seconds() / 60, 2)],
                "From_Part": [product_from],
                "To_Part": [product_to],
                "Operator": [operator_name],
                "Remarks": [remarks],
                "Timestamp": [datetime.now()],
                "Language": [lang]
            }

            # Add checklist step results with step names as keys
            for step, checked in zip(t['length_steps'], length_checks):
                data[step] = [checked]
            for step, checked in zip(t['three_point_steps'], three_point_checks):
                data[step] = [checked]
            for step, checked in zip(t['burring_steps'], burring_checks):
                data[step] = [checked]

            df_new = pd.DataFrame(data)

            try:
                df_existing = pd.read_csv("checklist_records.csv")
                df_all = pd.concat([df_existing, df_new], ignore_index=True)
            except:
                df_all = df_new

            df_all.to_csv("checklist_records.csv", index=False)
            st.markdown(f'<div class="success-message">{t["success"]} Duration: {duration}</div>', unsafe_allow_html=True)

            # Optionally clear inputs or rerun to refresh UI
            # st.experimental_rerun()

if __name__ == "__main__":
    main()
