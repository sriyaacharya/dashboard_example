import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Loading the csv file using pandas
df = pd.read_csv('Student_performance_data.csv')
df['GradeClass'] = 6 - df['GradeClass']  # Adjusting grade if needed
# Set up Streamlit app
# --- Streamlit UI ---
st.title("Student Grade Analysis Dashboard")
# --- Explore Impact of Any Parameter on GradeClass ---

st.subheader("Explore Impact of Any Parameter on GradeClass")

# Dropdown to select one parameter (excluding GradeClass)
selected_param = st.selectbox("Select a Parameter", [col for col in df.columns if col != 'GradeClass'])

# Set up figure
fig, ax = plt.subplots(figsize=(8, 5))

# Plot type based on variable type
if df[selected_param].dtype == 'object' or df[selected_param].nunique() < 10:
    # Categorical: use barplot
    sns.barplot(data=df, x=selected_param, y='GradeClass', ax=ax, ci=None)
    ax.set_title(f"Average GradeClass by {selected_param}")
    ax.set_ylabel("Average GradeClass")
else:
    # Numeric: use boxplot
    sns.boxplot(data=df, x='GradeClass', y=selected_param, ax=ax)
    ax.set_title(f"{selected_param} Distribution by GradeClass")
    ax.set_xlabel("GradeClass")
    ax.set_ylabel(selected_param)

st.pyplot(fig)

st.subheader("Explore Categorical Imapct on GradeClass")
# --- Define variable groups ---
params_group1 = ['Age', 'Gender', 'Ethnicity']
params_group2 = ['StudyTimeWeekly', 'Tutoring', 'ParentalSupport', 'Absences', 'ParentalEducation']
params_group3 = ['Extracurricular', 'Sports', 'Music', 'Volunteering']

group_dict = {
    "Demographic Factors": params_group1,
    "Academic and Family Support": params_group2,
    "Extracurricular Involvement": params_group3
}


selected_group = st.selectbox("Select Variable Group to View Correlation with Grades", list(group_dict.keys()))

# --- Plot heatmap based on selection ---
def plot_corr_heatmap(params, title):
    data = df[params + ['GradeClass']].corr()[['GradeClass']].drop(index='GradeClass')
    fig, ax = plt.subplots(figsize=(10, len(params)))
    sns.heatmap(
        data.sort_values(by='GradeClass', ascending=False),
        annot=True, cmap='PiYG', vmin=-1, vmax=1, ax=ax
    )
    ax.set_title(title)
    st.pyplot(fig)

# --- Call the function with selected group ---
plot_corr_heatmap(group_dict[selected_group], selected_group)

# --- End of Streamlit App ---



