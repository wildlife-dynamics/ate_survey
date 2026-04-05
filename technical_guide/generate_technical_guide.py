"""
Generate the ATE Survey Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: ate_survey_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "ate_survey_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"ATE Survey — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("ATE Survey", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Community attitude, knowledge, and sentiment analysis towards elephants", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>ate_survey</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>ate_survey</b> workflow processes Amboseli Trust for Elephants (ATE) "
      "community questionnaire responses recorded as <b>atequestionnaire_rep</b> events "
      "in EarthRanger. It cleans and transforms survey data, computes elephant "
      "sentiment scores, runs ANOVA and OLS statistical analyses, and produces a "
      "suite of charts, maps, and a Word report."),
    sp(4),
    p("The workflow delivers:"),
    bullet("1 demographic summary table (CSV)"),
    bullet("2 Likert charts — attitudes/beliefs (agree/disagree) and mitigation effectiveness"),
    bullet("26 pie charts across participant demographic and knowledge questions"),
    bullet("9 bar charts across tribal, lifestyle, and encounter questions"),
    bullet("1 elephant sentiment score dataset (CSV) with per-respondent scores"),
    bullet("1 ANOVA results table (CSV) testing sentiment against gender, age, education, marital status"),
    bullet("5 boxplots, 2 OLS scatter plots, and 4 Tukey HSD plots"),
    bullet("3 spatial maps — survey locations, gender distribution, and attitude scores"),
    bullet("1 Word report (social_survey.docx) populated with all charts and demographic table"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Demographic CSV",        "1",       "Summary table: gender, age, tribe, household size, education"],
            ["Likert charts",          "2",       "Agree/disagree attitudes and mitigation effectiveness ratings"],
            ["Pie charts",             "26",      "One per survey question (demographics, knowledge, behaviour)"],
            ["Bar charts",             "9",       "Tribal, land tenure, wildlife feelings, encounter frequency"],
            ["Elephant sentiment CSV", "1",       "Per-respondent overall attitude score"],
            ["ANOVA results CSV",      "1",       "Type II ANOVA: sentiment vs gender, age group, education, marital status"],
            ["Boxplots",               "5",       "Sentiment score distributions by demographic group"],
            ["OLS scatter plots",      "2",       "Sentiment vs age and household size"],
            ["Tukey HSD plots",        "4",       "Post-hoc pairwise comparisons per demographic factor"],
            ["Spatial maps",           "3",       "Survey locations, gender distribution, attitude scores"],
            ["Word report",            "1",       "Populated social_survey.docx with all charts and demographic table"],
        ],
        [4.5*cm, 2*cm, W - 6.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.17.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ate",     "0.0.3.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connection"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch atequestionnaire_rep survey event records for the analysis time range"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    note("This workflow does not require a Google Earth Engine connection."),
    sp(6),
    h2("2.3  Dropbox files"),
    p("Four files are downloaded from Dropbox at runtime "
      "(<b>overwrite_existing: false</b>, retries: 3):"),
    make_table(
        [
            ["File", "Purpose"],
            ["ate_survey_template_280857.docx",
             "Word report template — populated with charts and demographic table to produce social_survey.docx"],
            ["Amboseli-Ranch-Boundaries.gpkg",
             "Polygon boundaries for Amboseli ranches — rendered as black outlines on all maps"],
            ["Amboseli-Swamps.gpkg",
             "Amboseli swamp polygons — rendered in blue (#609cb5) on all maps"],
            ["National-Parks.gpkg",
             "National park polygons — rendered in green (#4c8c2b) on all maps"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("2.4  Base maps"),
    p("Two base map tile layers are configured by default via "
      "<b>set_base_maps_pydeck</b>:"),
    make_table(
        [
            ["Layer", "URL (abbreviated)", "Opacity"],
            ["ArcGIS World Hillshade",
             "server.arcgisonline.com/…/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}",
             "1.0"],
            ["ArcGIS World Street Map",
             "server.arcgisonline.com/…/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
             "0.25"],
        ],
        [4*cm, W - 6.5*cm, 2.5*cm],
    ),
    sp(6),
    h2("2.5  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All survey records are processed as a single undivided dataset — "
      "no fan-out or per-group branching is performed."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. SURVEY DATA PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Survey Data Pipeline"),
    hr(),
    p("Survey questionnaire responses are fetched, cleaned, and transformed "
      "through an eight-step pipeline before any analysis or charting begins."),
    sp(6),
    h2("3.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",              "get_events"],
            ["Event type",        "atequestionnaire_rep"],
            ["Columns retained",  "id, time, event_type, event_category, reported_by, "
                                  "serial_number, geometry, created_at, event_details, patrols"],
            ["include_details",   "true"],
            ["include_null_geometry", "false"],
            ["raise_on_empty",    "true"],
            ["include_updates",   "false"],
            ["include_related_events", "false"],
            ["include_display_values", "false"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("3.2  Invalid record exclusion"),
    p("Task: <b>exclude_value</b>. Filters out the record with "
      "<b>event_details value 46283</b> from the dataset. This is a known "
      "test/invalid questionnaire entry that must be excluded before processing."),
    sp(6),
    h2("3.3  JSON normalisation"),
    p("Task: <b>normalize_json_column</b>. The <b>event_details</b> column "
      "contains nested JSON. This step flattens it into individual columns "
      "(skip_if_not_exists: true, sort_columns: true), producing columns "
      "with the prefix <b>event_details__</b>."),
    sp(6),
    h2("3.4  Column mapping"),
    p("Task: <b>map_columns</b>. The normalised DataFrame undergoes "
      "significant restructuring:"),
    bullet("<b>32 columns dropped</b> — unused fields including event_category, "
           "reported_by, end_time, closing_statement, tribe/occupation/land "
           "tenure 'if other' free-text columns, and supplementary livestock "
           "health detail columns."),
    bullet("<b>~60 columns renamed</b> — all <b>event_details__</b> prefixed "
           "columns are renamed to human-readable labels (e.g. "
           "event_details__participant_age → 'Participant age', "
           "event_details__belief_1 → 'Humans and elephants can live together')."),
    sp(6),
    h2("3.5  Type conversion"),
    p("Two conversion tasks run sequentially:"),
    make_table(
        [
            ["Task", "Columns", "Count"],
            ["convert_object_to_value",
             "Participant age, Number of cows, Household size, Land owned (acres), "
             "Number of shoats, Agricultural land (acres), Number of sheep or goats, "
             "Number of dogs, Number of cattle, Number of donkeys",
             "10"],
            ["convert_object_to_string",
             "id, all categorical response columns (tribe, gender, knowledge, "
             "attitude, belief, exposure, behaviour, mitigation, perception fields)",
             "49"],
        ],
        [4.5*cm, W - 7*cm, 2.5*cm],
    ),
    sp(6),
    h2("3.6  Missing value fill"),
    p("Task: <b>fill_missing_values</b>. Missing values are filled with "
      "type-appropriate defaults:"),
    make_table(
        [
            ["Column type", "Fill value", "Count"],
            ["Numeric (10 columns)", "0",            "Participant age, cow/shoat/livestock counts, land areas, household size"],
            ["Categorical (49 columns)", "Unspecified","All string/response columns"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    sp(6),
    h2("3.7  Survey response mapping"),
    p("Three <b>map_survey_responses</b> tasks normalise raw API response "
      "strings to display labels:"),
    make_table(
        [
            ["Task", "Columns", "Mapping"],
            ["map_agree_disagree",
             "11 belief/attitude columns (Humans and elephants can live together, "
             "Importance of elephants living here, Elephants should only live inside parks, "
             "cost/benefit beliefs, hazard acceptance)",
             "strongly_agree→Strongly agree, agree→Agree, neutral→Neutral, "
             "disagree→Disagree, strongly_disagree→Strongly disagree, "
             "i_dont_know→I dont know, prefer_not_to_answer→Prefer not to answer"],
            ["map_true_false",
             "7 elephant knowledge columns (family groups, seasonal movement, "
             "head-shaking, trunk-raising, musth behaviour, smell/hearing, "
             "female protection)",
             "false→False, true→True, i_dont_know→I dont know"],
            ["map_no_effect",
             "3 effectiveness columns (crop protection, behaviour practice, "
             "water protection)",
             "highly_effective→Highly effective, effective→Effective, "
             "not_effective→Not effective, i_dont_know→I dont know"],
        ],
        [3*cm, 5.5*cm, W - 8.5*cm],
    ),
    sp(6),
    h2("3.8  Ordinal column mapping and integer conversion"),
    p("<b>map_survey_columns</b> applies custom ordinal ordering to 28 columns "
      "(demographic fields plus all Agree/Disagree attitude columns) to ensure "
      "correct sort order in charts."),
    p("<b>convert_to_int</b> then casts 9 numeric columns to integer type "
      "(errors: coerce, fill_value: 0, inplace: false)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. DEMOGRAPHIC TABLE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Demographic Table"),
    hr(),
    p("Task: <b>format_demographic_table</b>. Produces a summary table from "
      "the cleaned survey data using the following five columns:"),
    make_table(
        [
            ["Column"],
            ["Participant gender"],
            ["Participant age"],
            ["Participant tribe"],
            ["Household size"],
            ["Highest level of education"],
        ],
        [W],
    ),
    sp(4),
    p("The resulting table is persisted to disk as <b>demographic_table.csv</b> "
      "and is also passed directly to the Word report generator "
      "(<b>demographic_csv: demographic_table.csv</b>)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. BINNING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Column Binning"),
    hr(),
    p("Task: <b>bin_columns</b>. Ten continuous numeric columns are binned into "
      "<b>5 equal-width bins</b> (suffix: 'bins', inplace: true). The binned "
      "columns are used downstream by all chart and map tasks:"),
    make_table(
        [
            ["Column binned", "Resulting column"],
            ["Participant age",          "Participant agebins"],
            ["Number of cows",           "Number of cowsbins"],
            ["Household size",           "Household sizebins"],
            ["Number of shoats",         "Number of shoatsbins"],
            ["Land owned (acres)",       "Land owned (acres)bins"],
            ["Agricultural land (acres)","Agricultural land (acres)bins"],
            ["Number of dogs",           "Number of dogsbins"],
            ["Number of cattle",         "Number of cattlebins"],
            ["Number of donkeys",        "Number of donkeysbins"],
            ["Number of sheep or goats", "Number of sheep or goatsbins"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(4),
    p("Two binned columns are additionally processed by <b>categorize_bins</b> "
      "to convert the numeric interval labels to ordered categorical dtype:"),
    bullet("Household sizebins"),
    bullet("Participant agebins"),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Charts"),
    hr(),
    h2("6.1  Likert chart — Agree/Disagree"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",                 "create_likert_chart"],
            ["Input columns (11)",   "Humans and elephants can live together; Importance of elephants living here; "
                                     "Elephants should only live inside parks; Elephants harm community members; "
                                     "Elephants negatively affect my livelihood; Elephants impact my emotional wellbeing; "
                                     "Benefit from enjoying seeing elephants; Elephants are important for a healthy ecosystem; "
                                     "Acceptable to harm elephants if they damage property or livestock; "
                                     "Acceptable to harm elephants if people are hurt; "
                                     "Receive livelihood benefits from elephants"],
            ["Title",                "Agree/Disagree"],
            ["height_per_question",  "60 px"],
            ["min_height",           "400 px"],
            ["width",                "1 200 px"],
            ["show_percentages",     "true"],
            ["sort_questions",       "false"],
            ["sort_by",              "positive"],
            ["response_order",       "Strongly disagree → Disagree → Neutral → Agree → Strongly agree"],
            ["neutral_categories",   "Neutral"],
            ["Color: Strongly disagree","#2c5282 (dark blue)"],
            ["Color: Disagree",      "#4299e1 (blue)"],
            ["Color: Neutral / Unspecified / I dont know","#a0aec0 (grey)"],
            ["Color: Agree",         "#ed8936 (orange)"],
            ["Color: Strongly agree","#c05621 (dark orange)"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    p("Output: <b>elephants_relationship_likert.html</b>"),
    sp(6),
    h2("6.2  Likert chart — Mitigation Effectiveness"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Input columns (3)", "Effectiveness rating of primary crop protection method; "
                                  "Effectiveness rating of that practice; "
                                  "Effectiveness rating of water protection"],
            ["Title",             "Effective/Not effective"],
            ["response_order",    "Not effective → Effective → Highly effective"],
            ["neutral_categories","I dont know"],
            ["Color: Not effective",   "#D64545 (red)"],
            ["Color: I dont know",     "#A8A8A8 (grey)"],
            ["Color: Unspecified",     "#D4D4D4 (light grey)"],
            ["Color: Effective",       "#2A9D8F (teal)"],
            ["Color: Highly effective","#2E7D32 (dark green)"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    p("Output: <b>effectiveness_mitigation_methods.html</b>"),
    sp(6),
    h2("6.3  Pie charts"),
    p("Task: <b>draw_pie_and_persist</b>. Generates one pie chart per column "
      "(26 total). Charts are saved as individual HTML files then converted to "
      "PNG (25 ms timeout, scale 2x). Columns:"),
    make_table(
        [
            ["Column"],
            ["Participant gender"],
            ["Female elephants live in family groups"],
            ["Female elephants protect their young"],
            ["Participant age group"],
            ["See more elephants now than before"],
            ["Do you change routes or schedules because of elephants"],
            ["What do you do when you encounter elephants on foot"],
            ["Noticed signs of illness in wild animals"],
            ["Willingness to join future community dialogue"],
            ["Use measures to protect crops from elephants"],
            ["Ever been involved in or witnessed an elephant harmed"],
            ["Elephants can smell and hear from far away"],
            ["Elephants move seasonally for food and water"],
            ["Elephant may shake its head when annoyed"],
            ["Elephant signals awareness by raising trunk"],
            ["Male elephants with secretions may be more aggressive"],
            ["Highest level of education"],
            ["Use measures to protect livestock from elephants"],
            ["Protect water sources from elephants"],
            ["Marital status"],
            ["Greatest threat to your livestock"],
            ["Benefit from the KCCDT Big Life electric fence"],
            ["Pay into fence maintenance fund"],
            ["Do you report elephant conflict incidents"],
            ["Which intervention would help you in future"],
            ["Opinion on having elephants in the area"],
        ],
        [W],
    ),
    sp(6),
    h2("6.4  Bar charts"),
    p("Task: <b>draw_bar_and_persist</b>. Generates one bar chart per column "
      "(9 total). Saved and converted to PNG (25 ms timeout, scale 2x). Columns:"),
    make_table(
        [
            ["Column"],
            ["Participant tribe"],
            ["Years living in area"],
            ["Overall feelings about wildlife"],
            ["How often seen elephants in the last year"],
            ["Reaction to hearing about elephants being harmed"],
            ["Land tenure"],
            ["Greatest threat to crop production"],
            ["Household sizebins"],
            ["Participant agebins"],
        ],
        [W],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. ELEPHANT SENTIMENT SCORES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Elephant Sentiment Score"),
    hr(),
    p("A per-respondent <b>elephant_sentiment_score</b> is computed by "
      "<b>calculate_elephant_sentiment_score</b> from 11 attitude/belief "
      "columns. Positive and negative columns are weighted in opposite "
      "directions to produce an overall attitude score."),
    sp(6),
    h2("7.1  Input columns"),
    make_table(
        [
            ["Direction", "Column"],
            ["Positive", "Humans and elephants can live together"],
            ["Positive", "Importance of elephants living here"],
            ["Positive", "Benefit from enjoying seeing elephants"],
            ["Positive", "Elephants are important for a healthy ecosystem"],
            ["Positive", "Receive livelihood benefits from elephants"],
            ["Negative", "Elephants should only live inside parks"],
            ["Negative", "Elephants harm community members"],
            ["Negative", "Elephants negatively affect my livelihood"],
            ["Negative", "Elephants impact my emotional wellbeing"],
            ["Negative", "Acceptable to harm elephants if they damage property or livestock"],
            ["Negative", "Acceptable to harm elephants if people are hurt"],
        ],
        [3*cm, W - 3*cm],
    ),
    sp(4),
    p("Prior to the score calculation, geometry outliers are removed "
      "(<b>z_threshold: 3</b>) and the 11 attitude columns plus id and "
      "geometry are filtered to form the input GeoDataFrame. "
      "The resulting scores are persisted to disk as "
      "<b>elephant_sentiment_scores.csv</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. STATISTICAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Statistical Analysis"),
    hr(),
    p("The workflow runs three complementary statistical analyses to "
      "investigate which demographic factors predict elephant sentiment scores."),
    sp(6),
    h2("8.1  ANOVA"),
    p("Task: <b>perform_anova_analysis</b>. A <b>Type II ANOVA</b> is run with "
      "<b>elephant_sentiment_score</b> as the target and four demographic "
      "factors as predictors:"),
    make_table(
        [
            ["Factor column"],
            ["gender_of_participant"],
            ["age_group_distribution"],
            ["education_level"],
            ["marital_status"],
        ],
        [W],
    ),
    p("Results are persisted as <b>anova_results.csv</b>."),
    sp(6),
    h2("8.2  Boxplots"),
    p("Task: <b>draw_boxplot_and_persist</b>. One boxplot per demographic "
      "column (5 total), with <b>elephant_sentiment_score</b> on the y-axis:"),
    make_table(
        [
            ["Column (x-axis)"],
            ["marital_status"],
            ["education_level"],
            ["tribe"],
            ["age_group_distribution"],
            ["gender_of_participant"],
        ],
        [W],
    ),
    sp(6),
    h2("8.3  OLS scatter plots"),
    p("Task: <b>draw_ols_scatterplot_and_persist</b>. Ordinary least-squares "
      "regression plots with <b>elephant_sentiment_score</b> on the y-axis "
      "for 2 continuous predictors:"),
    make_table(
        [
            ["Column (x-axis)"],
            ["age"],
            ["household_size"],
        ],
        [W],
    ),
    sp(6),
    h2("8.4  Tukey HSD plots"),
    p("Task: <b>draw_tukey_plots_and_persist</b>. Post-hoc pairwise comparison "
      "plots for 4 factor columns against <b>elephant_sentiment_score</b>:"),
    make_table(
        [
            ["Column"],
            ["education_level"],
            ["age_group_distribution"],
            ["gender_of_participant"],
            ["marital_status"],
        ],
        [W],
    ),
    sp(4),
    p("All statistical charts are saved as individual HTML files then "
      "converted to PNG (25 ms timeout, device_scale_factor: 2.0, "
      "max_concurrent_pages: 1)."),
    sp(6),
    h2("8.5  Merged stats DataFrame"),
    p("Before statistical analysis, a merged DataFrame is assembled: "
      "demographic columns (id, Participant age, Marital status, Highest "
      "level of education, Participant tribe, Household size, Participant age "
      "group, Participant gender) are joined to the sentiment scores on "
      "<b>id</b> (left join, preserve_left_index: false). Columns are then "
      "renamed to snake_case for use in statistical tasks."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. SPATIAL MAPS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Spatial Maps"),
    hr(),
    p("Three EcoMaps are produced. All share the same base map tiles, "
      "static context layers, and map viewport. Each uses a scatter plot "
      "layer with radius 4 m, opacity 0.75, stroked: true, and "
      "line_color [0,0,0]."),
    sp(6),
    h2("9.1  Static context layers"),
    p("Three polygon GeoPackage files are downloaded, loaded, "
      "reprojected to EPSG:4326, and typed via <b>get_gdf_geom_type</b>. "
      "All three are included on every map via <b>combine_deckgl_map_layers</b>:"),
    make_table(
        [
            ["Layer", "Fill / line color", "Hex", "Line width", "Opacity"],
            ["Ranch boundaries",
             "[0, 0, 0]",   "#000000", "2.25", "0.45 (outline only, filled: false)"],
            ["Amboseli swamps",
             "[96, 156, 181]", "#609cb5", "0.5",  "0.45 (filled: true)"],
            ["National parks",
             "[76, 140, 43]",  "#4c8c2b", "0.75", "0.45 (filled: true)"],
        ],
        [3.5*cm, 3.5*cm, 2*cm, 2.5*cm, W - 11.5*cm],
    ),
    sp(4),
    note("The map viewport is zoomed to the extent of the reprojected "
         "ranch boundaries GeoDataFrame (pitch: 0, bearing: 0). "
         "All maps use max_zoom: 10 and legend placement: bottom-right."),
    sp(6),
    h2("9.2  Survey locations map"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Input data",    "bin_survey_cols GeoDataFrame (z_threshold: 3 outlier removal)"],
            ["Fill color",    "[199, 0, 57] — crimson red (#C70039), single colour for all points"],
            ["Legend",        "Survey location (#C70039)"],
            ["Output",        "survey_locations_ecomap.html / .png"],
            ["PNG timeout",   "40 000 ms"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("9.3  Gender distribution map"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Input data",      "bin_survey_cols GeoDataFrame (z_threshold: 3 outlier removal)"],
            ["Color column",    "Participant gender → gender_colors (apply_color_map)"],
            ["Colormap (3 values)", "#FFC0CB (pink), #0000FF (blue), #DC143C (crimson)"],
            ["Legend title",    "Gender"],
            ["Output",          "gender_distribution_ecomap.html / .png"],
            ["PNG timeout",     "40 000 ms"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("9.4  Attitude scores map"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Input data",        "calc_attitude_scores GeoDataFrame (z_threshold: 3 outlier removal)"],
            ["Color column",      "overall_attitude → attitude_colors (apply_color_map)"],
            ["Colormap (5 values)","#FF0000 (red), #FFA500 (orange), #FFFF00 (yellow), "
                                   "#00FF00 (green), #0000FF (blue)"],
            ["Legend title",      "Attitude scores"],
            ["Legend columns",    "label_column: overall_attitude, color_column: attitude_colors, sort: ascending"],
            ["Output",            "attitude_scores_community.html / .png"],
            ["PNG timeout",       "40 000 ms"],
        ],
        [5*cm, W - 5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORD REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Word Report"),
    hr(),
    p("Task: <b>persist_survey_word</b>. The downloaded Word template "
      "(<b>ate_survey_template_280857.docx</b>) is populated with survey "
      "outputs and saved as <b>social_survey.docx</b>."),
    sp(6),
    make_table(
        [
            ["Parameter", "Value"],
            ["template_path",  "ate_survey_template_280857.docx (downloaded from Dropbox)"],
            ["output_dir",     "ECOSCOPE_WORKFLOWS_RESULTS"],
            ["time_period",    "Analysis time range (from set_time_range)"],
            ["box_h_cm",       "6.5 cm — height of image placeholder boxes"],
            ["box_w_cm",       "11.11 cm — width of image placeholder boxes"],
            ["filename",       "social_survey.docx"],
            ["demographic_csv","demographic_table.csv"],
        ],
        [4*cm, W - 4*cm],
    ),
    note("The Word template contains placeholder boxes sized to box_h_cm × "
         "box_w_cm. The task inserts charts and the demographic table into "
         "these placeholders."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>. "
      "Files marked with <i>&lt;column&gt;</i> are produced once per chart column."),
    make_table(
        [
            ["File", "Description"],
            ["demographic_table.csv",
             "Summary demographic table (gender, age, tribe, household size, education)"],
            ["elephant_sentiment_scores.csv",
             "Per-respondent overall_attitude score computed from 11 belief/attitude columns"],
            ["anova_results.csv",
             "Type II ANOVA results: elephant_sentiment_score vs 4 demographic factors"],
            ["elephants_relationship_likert.html / .png",
             "Agree/Disagree Likert chart for 11 attitude columns"],
            ["effectiveness_mitigation_methods.html / .png",
             "Effective/Not effective Likert chart for 3 mitigation effectiveness columns"],
            ["<column>_pie.html / .png (×26)",
             "One pie chart per survey question"],
            ["<column>_bar.html / .png (×9)",
             "One bar chart per survey question"],
            ["<column>_boxplot.html / .png (×5)",
             "Sentiment score boxplot per demographic group"],
            ["<column>_ols.html / .png (×2)",
             "OLS regression scatter plot (age, household_size vs sentiment)"],
            ["<column>_tukey.html / .png (×4)",
             "Tukey HSD post-hoc comparison plot per demographic factor"],
            ["survey_locations_ecomap.html / .png",
             "All survey point locations on Amboseli base map"],
            ["gender_distribution_ecomap.html / .png",
             "Survey points coloured by respondent gender"],
            ["attitude_scores_community.html / .png",
             "Survey points coloured by overall elephant attitude score"],
            ["social_survey.docx",
             "Final Word report populated with all charts and demographic table"],
        ],
        [6.5*cm, W - 6.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Workflow Execution Logic"),
    hr(),
    h2("12.1  Global skip conditions"),
    p("All tasks carry the default skipif block (<b>task-instance-defaults</b>):"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip task if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    h2("12.2  No mapvalues fan-out"),
    p("This workflow processes all survey records as a single batch. "
      "There is no <b>mapvalues</b> or <b>split_groups</b> fan-out — "
      "every task runs exactly once on the full dataset. "
      "The empty grouper list (groupers: []) is passed through to the "
      "dashboard but is not used for any data splitting."),
    sp(6),
    h2("12.3  Screenshot timing"),
    make_table(
        [
            ["Chart / map type", "wait_for_timeout", "Reason"],
            ["Pie charts (26)",         "25 ms",     "Static Plotly HTML — no tiles"],
            ["Bar charts (9)",          "25 ms",     "Static Plotly HTML — no tiles"],
            ["Boxplots (5)",            "25 ms",     "Static Plotly HTML — no tiles"],
            ["OLS scatter plots (2)",   "25 ms",     "Static Plotly HTML — no tiles"],
            ["Tukey plots (4)",         "25 ms",     "Static Plotly HTML — no tiles"],
            ["Likert charts (2)",       "25 ms",     "Static Plotly HTML — no tiles"],
            ["Attitude scores map",     "40 000 ms", "Tile map — waits for ArcGIS tile rendering"],
            ["Gender distribution map", "40 000 ms", "Tile map — waits for ArcGIS tile rendering"],
            ["Survey locations map",    "40 000 ms", "Tile map — waits for ArcGIS tile rendering"],
        ],
        [4.5*cm, 3*cm, W - 7.5*cm],
    ),
    sp(4),
    note("All PNG conversions use device_scale_factor: 2.0 and "
         "max_concurrent_pages: 1. The two Likert HTMLs are passed as a "
         "list to a single html_to_png call."),
    sp(6),
    h2("12.4  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> which packages "
      "workflow details, time range, and groupers. The <b>widgets</b> list "
      "is empty — no single-value or map widgets are configured for "
      "this workflow."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.17.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.17.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*"],
            ["ecoscope-workflows-ext-ate",     "0.0.3.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
