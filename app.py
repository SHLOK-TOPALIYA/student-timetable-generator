import streamlit as st
from core import (
    DAYS, candidate_activity_codes, course_catalog, detect_conflicts, find_activity_associations,
    group_options_for_codes, make_pdf, parse_activity_file, parse_lecture_file,
    safe_filename, section_options, select_activity_entries, select_lecture_entries,
)

st.set_page_config(page_title='Student Timetable Generator', page_icon='📅', layout='wide')

st.title('📅 Student Timetable Generator')
st.caption('Build a clean personalized timetable from your university timetable files — lectures, labs and tutorials in one PDF.')

MODE_OPTIONS = {
    '1': 'Make Lecture Timetable Only',
    '2': 'Make Lab & Tutorial Timetable Only',
    '3': 'Make Complete Timetable — Lecture + Lab + Tutorial',
    '4': 'Add Lab & Tutorial to an Existing Lecture Timetable',
}

mode = st.radio(
    'What do you want to make?',
    list(MODE_OPTIONS.values()),
    index=0,
    help='Choose exactly what information you currently have and what timetable you want to generate.'
)

st.divider()


def uploader(label, key, help_text):
    return st.file_uploader(label, type=['xlsx','xlsm','pdf','csv'], key=key, help=help_text)


def dynamic_course_inputs(prefix):
    """Show one extra course box whenever the current last box is filled.

    Streamlit reruns the app when the user leaves a text box (on_change), so
    the user does not need to press Enter.  The callback only increases the
    number of visible boxes; it never validates the code or controls whether
    another box appears.
    """
    count_key = f"{prefix}_course_count"
    if count_key not in st.session_state:
        st.session_state[count_key] = 1

    def add_next_field(index):
        key = f"{prefix}_course_{index}"
        if st.session_state.get(key, "").strip() and st.session_state[count_key] == index + 1:
            st.session_state[count_key] = index + 2

    count = st.session_state[count_key]
    for i in range(count):
        st.text_input(
            f"Course {i + 1}",
            key=f"{prefix}_course_{i}",
            on_change=add_next_field if i == count - 1 else None,
            args=(i,),
        )

    values = []
    for i in range(st.session_state[count_key]):
        value = st.session_state.get(f"{prefix}_course_{i}", "").strip()
        if value:
            values.append(value)
    return values


def parse_section_requests(lecture_entries, codes, prefix):
    catalog=course_catalog(lecture_entries)
    parsed=[]; errors=[]
    multi=[]
    for code_raw in codes:
        from core import split_code_section
        code, typed=split_code_section(code_raw)
        if code not in catalog:
            errors.append(f'**{code_raw}** was not found in the lecture timetable.')
            continue
        opts=section_options(lecture_entries,code)
        if typed:
            if opts and typed not in opts:
                errors.append(f'**{code_raw}** uses section {typed}, but available sections are: {", ".join(opts)}.')
            else:
                parsed.append((code,typed))
        elif len(opts)>1:
            multi.append((code,opts))
        else:
            parsed.append((code,opts[0] if len(opts)==1 else ''))
    # One global section whenever possible.
    if multi:
        common=set(multi[0][1])
        for _,opts in multi[1:]: common &= set(opts)
        if common:
            selected=st.selectbox('Your lecture section',sorted(common),key=f'{prefix}_global_section')
            for code,_ in multi: parsed.append((code,selected))
        else:
            st.warning('These selected courses do not share one common section label, so a separate choice is required only for the courses with different section sets.')
            for code,opts in multi:
                selected=st.selectbox(f'{code} section',opts,key=f'{prefix}_section_{code}')
                parsed.append((code,selected))
    return list(dict.fromkeys(parsed)),errors


def group_selectors(activity_entries,codes,prefix,explicit_map=None):
    selections={}
    for kind,label in [('lab','Lab group'),('tutorial','Tutorial group')]:
        option_sets=[]
        for code in codes:
            assoc,_=find_activity_associations(code,activity_entries,explicit_map)
            opts={e.group for e in assoc if e.kind==kind and e.group}
            if opts:
                option_sets.append((code,opts))
        if not option_sets:
            continue
        common=set.intersection(*(opts for _,opts in option_sets))
        if common:
            selections[kind]=st.selectbox(f'{label} (used for all applicable courses)',sorted(common),key=f'{prefix}_{kind}_group')
        else:
            st.warning(f'No single {label.lower()} label is shared by every applicable course. The app will ask only for the courses that need an exception.')
            per={}
            for code,opts in option_sets:
                per[code]=st.selectbox(f'{code} {label.lower()}',sorted(opts),key=f'{prefix}_{kind}_{code}')
            selections[kind]=per
    return selections


def activity_preview(activity_entries, codes, groups, explicit_map=None):
    group_by={}
    for code in codes:
        if not groups:
            group_by[code]={}
        else:
            group_by[code]={}
            for kind,value in groups.items():
                group_by[code][kind]=value.get(code) if isinstance(value,dict) else value
    return select_activity_entries(activity_entries,codes,group_by,explicit_map)


def course_name_for_code(entries, code):
    """Return a course title only when the source explicitly provides one.

    The current university lecture sheet's ``Name`` column contains faculty
    names/initials, not course titles, so those values must NOT be presented as
    course names.  This helper is intentionally conservative.
    """
    for e in entries:
        if e.code != code:
            continue
        # A future parser may store an explicit title as a tagged detail.
        m = __import__('re').search(r'(?:Course Name|Course Title)\s*:\s*(.+?)(?:\s+•|$)', e.details or '', __import__('re').I)
        if m:
            return m.group(1).strip()
    return ""


def resolve_activity_mappings(activity_entries, codes, prefix, lecture_entries=None):
    """Resolve lecture-code -> activity-code mappings with explicit approval.

    Exact code matches are automatic.  A different activity code is NEVER
    assumed to be the same course.  The user is shown the candidate code and,
    when the lecture timetable contains that code, its official course name.
    Only an explicit Yes creates the mapping.
    """
    if not activity_entries:
        st.error("❌ The Lab & Tutorial timetable has not been uploaded. Please upload the official Lab & Tutorial timetable to continue.")
        return {}, []

    explicit_map = {}
    unmatched = []
    for code in codes:
        direct, _ = find_activity_associations(code, activity_entries)
        if not direct:
            unmatched.append(code)

    if not unmatched:
        return explicit_map, []

    st.subheader("🔗 Lab/Tutorial course matching")
    if lecture_entries is not None:
        st.caption("The uploaded university timetables are the source of truth. Exact course-code matches are used directly. If the university uses a different code for the same course, you must confirm it before it is added.")
    else:
        st.caption("The uploaded university Lab/Tutorial timetable is the source of truth. Exact course-code matches are used directly. If a different code may represent the same course, you must confirm it before it is added.")
    notes = []

    for code in unmatched:
        candidates = candidate_activity_codes(code, activity_entries)
        if not candidates:
            st.warning(f"⚠️ **{code}** does not match any Lab/Tutorial course code in the uploaded university timetable. There is no Lab/Tutorial entry for this course in the uploaded timetable, so nothing will be added.")
            continue

        candidate_labels = ["No matching Lab/Tutorial course"]
        label_to_code = {candidate_labels[0]: ""}
        for candidate in candidates:
            name = course_name_for_code(lecture_entries or [], candidate)
            label = f"{candidate} — {name}" if name else candidate
            candidate_labels.append(label)
            label_to_code[label] = candidate

        choice = st.selectbox(
            f"**{code}** has no exact Lab/Tutorial code. Which university activity course corresponds to it?",
            candidate_labels,
            key=f"{prefix}_activity_map_{code}",
        )
        selected_code = label_to_code[choice]

        if selected_code:
            confirm = st.radio(
                f"Does **{selected_code}** represent the Lab/Tutorial activity for **{code}**?",
                ["Yes — this is the same course", "No — these are different courses"],
                key=f"{prefix}_activity_confirm_{code}",
                horizontal=True,
            )
            if confirm.startswith("Yes"):
                explicit_map[code] = selected_code
                display_name = course_name_for_code(lecture_entries or [], selected_code)
                notes.append(f"{code} → {selected_code}" + (f" ({display_name})" if display_name else "") + " — user confirmed")
            else:
                st.warning(
                    f"❌ **{code}** and **{selected_code}** are being treated as different courses. "
                    "There is no confirmed Lab/Tutorial match for this course. If you need the Lab/Tutorial for another lecture course, generate the correct Lecture Timetable first and then use the add-Lab/Tutorial option."
                )
        else:
            st.info(f"No Lab/Tutorial course was selected for **{code}**. No activity entry will be added.")

    return explicit_map, notes

def show_preview(entries):
    if not entries:
        return
    rows=[]
    for e in sorted(entries,key=lambda x:(DAYS.index(x.day),__import__('core').time_sort_key(x.time),x.code,x.kind,x.group)):
        rows.append({'Day':e.day,'Time':e.time,'Course':e.code + (f' ({e.section})' if e.section else ''),'Type':e.kind.title(),'Group':e.group or '—','Details':e.details or '—'})
    st.dataframe(rows,use_container_width=True,hide_index=True)


lecture_entries=None
activity_entries=None
lecture_title='Student Timetable'
activity_title='Lab/Tutorial Timetable'

if mode in [MODE_OPTIONS['1'], MODE_OPTIONS['3']]:
    if mode == MODE_OPTIONS['3']:
        col1, col2 = st.columns(2)
        with col1:
            up = uploader('📚 Upload the official Lecture Timetable', 'lecture_main', 'Excel, PDF or CSV. Excel is recommended.')
        with col2:
            act = uploader('🧪 Upload the official Lab & Tutorial Timetable', 'activity_main', 'Upload the university Lab/Tutorial timetable.')
    else:
        up = uploader('📚 Upload the official Lecture Timetable', 'lecture_main', 'Excel, PDF or CSV. Excel is recommended.')
        act = None

    if not up:
        st.info('Upload the lecture timetable to continue.')
        st.stop()
    if mode == MODE_OPTIONS['3'] and not act:
        st.info('Upload the official Lab & Tutorial timetable to continue.')
        st.stop()
    try:
        lecture_entries, lecture_title = parse_lecture_file(up.name, up.getvalue())
        st.success(f'Lecture timetable loaded: {len(lecture_entries)} entries detected.')
        if mode == MODE_OPTIONS['3']:
            activity_entries, activity_title = parse_activity_file(act.name, act.getvalue())
            st.success(f'Lab/Tutorial timetable loaded: {len(activity_entries)} entries detected.')
    except Exception as e:
        st.error(str(e)); st.stop()

if mode==MODE_OPTIONS['2']:
    up=uploader('🧪 Upload the Lab & Tutorial Timetable', 'activity_only', 'Upload the university Lab/Tutorial timetable.')
    if not up:
        st.info('Upload the Lab/Tutorial timetable to continue.')
        st.stop()
    try:
        activity_entries,activity_title=parse_activity_file(up.name,up.getvalue())
        st.success(f'Lab/Tutorial timetable loaded: {len(activity_entries)} entries detected.')
    except Exception as e:
        st.error(str(e)); st.stop()

if mode==MODE_OPTIONS['4']:
    old=uploader('📄 Upload an existing Lecture Timetable PDF', 'existing_lecture', 'Upload a lecture timetable PDF generated by this application.')
    act=uploader('🧪 Upload the new Lab & Tutorial Timetable', 'activity_existing', 'Upload the university Lab/Tutorial timetable.')
    if not old or not act:
        st.info('Upload both the existing lecture PDF and the Lab/Tutorial timetable.')
        st.stop()
    try:
        lecture_entries,lecture_title=parse_lecture_file(old.name,old.getvalue())
        activity_entries,activity_title=parse_activity_file(act.name,act.getvalue())
        st.success(f'Existing lecture timetable read: {len(lecture_entries)} entries. Lab/Tutorial timetable read: {len(activity_entries)} entries.')
        st.caption('If a lecture code and Lab/Tutorial code differ, the app will ask you to confirm whether the university uses the different code for the same course.')
    except Exception as e:
        st.error(str(e)); st.stop()

codes=[]
lecture_selected=[]
activity_selected=[]

if mode in [MODE_OPTIONS['1'],MODE_OPTIONS['2'],MODE_OPTIONS['3']]:
    st.subheader('1️⃣ Enter your course codes')
    codes=dynamic_course_inputs('main')

if mode==MODE_OPTIONS['4']:
    # Codes are recovered from the existing lecture PDF, so no re-entry is needed.
    codes=sorted({e.code for e in lecture_entries})
    st.subheader('1️⃣ Courses recovered from your existing lecture timetable')
    st.write(', '.join(codes))

if mode in [MODE_OPTIONS['1'],MODE_OPTIONS['3'],MODE_OPTIONS['4']]:
    if not codes:
        st.info('Enter at least one course code.')
        st.stop()
    lecture_requests,errors=parse_section_requests(lecture_entries,codes,'lecture')
    for err in errors: st.error('❌ '+err)
    lecture_selected=select_lecture_entries(lecture_entries,lecture_requests)
    if not lecture_selected:
        st.stop()
    st.subheader('📚 Lecture timetable preview')
    show_preview(lecture_selected)

if mode in [MODE_OPTIONS['2'],MODE_OPTIONS['3'],MODE_OPTIONS['4']]:
    st.subheader('2️⃣ Lab & Tutorial groups')
    st.caption('The app reads the group labels directly from the uploaded Lab/Tutorial timetable. One selected Lab Group is reused for all applicable labs, and one Tutorial Group is reused for all applicable tutorials.')
    if mode==MODE_OPTIONS['2']:
        if not codes:
            st.stop()
    explicit_map={}
    if mode in [MODE_OPTIONS['2'],MODE_OPTIONS['3'],MODE_OPTIONS['4']]:
        # Always validate every entered course against the uploaded Lab/Tutorial timetable.
        # Exact matches are automatic; different codes require explicit user confirmation.
        explicit_map,association_notes=resolve_activity_mappings(
            activity_entries, codes, 'activity', lecture_entries if mode in [MODE_OPTIONS['3'],MODE_OPTIONS['4']] else None
        )
    else:
        association_notes=[]

    relevant=[]
    for code in codes:
        assoc,_=find_activity_associations(code,activity_entries,explicit_map)
        if assoc:
            relevant.append(code)

    if not relevant:
        st.info('No Lab/Tutorial entry was matched to the entered course codes. No activity classes will be added.')
    else:
        if association_notes:
            st.success('Confirmed Lab/Tutorial mappings: ' + '; '.join(association_notes))
        group_choices=group_selectors(activity_entries,relevant,'activity',explicit_map)
        activity_selected=activity_preview(activity_entries,relevant,group_choices,explicit_map)
        if activity_selected:
            st.subheader('🧪 Lab & Tutorial preview')
            show_preview(activity_selected)

all_selected=lecture_selected+activity_selected
if not all_selected:
    st.stop()

st.subheader('3️⃣ Combined timetable')
show_preview(all_selected)
conflicts=detect_conflicts(all_selected)
if conflicts:
    st.warning('⚠️ Possible timetable clashes detected:')
    for (day,slot),items in conflicts:
        st.write(f'- **{day}:** {slot} — ' + ', '.join(f'{e.code} ({e.kind})' for e in items))
else:
    st.success('✅ No overlapping classes detected in the selected timetable.')

st.subheader('4️⃣ Generate PDF')
default_title=lecture_title if mode!=MODE_OPTIONS['2'] else activity_title
title=st.text_input('PDF title',value=default_title,help='The title is prefilled from the uploaded timetable. You can edit it if desired.')

if st.button('✨ Generate Timetable PDF',type='primary',use_container_width=True):
    try:
        pdf=make_pdf(all_selected,title)
        st.session_state.final_pdf=pdf
        st.session_state.final_filename=safe_filename(title)
    except Exception as e:
        st.error(f'Could not generate the PDF: {e}')

if st.session_state.get('final_pdf'):
    st.success('🎉 Your combined timetable PDF is ready!')
    st.download_button('⬇️ Download Timetable PDF',st.session_state.final_pdf,file_name=st.session_state.final_filename,mime='application/pdf',use_container_width=True)

st.divider()
st.caption('Course matching uses the uploaded university timetables. Different Lab/Tutorial codes are never treated as the same course without your confirmation.')
