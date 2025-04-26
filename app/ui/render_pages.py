import streamlit as st

def render_tables(dict_dframes):

    cols = st.columns(4, border=False)

    with cols[0]:
        st.subheader("Messages per User")
        st.dataframe(dict_dframes["user_counts"], hide_index=True, use_container_width=True)

    with cols[1]:
        st.subheader("Messages per Day")
        st.dataframe(
            dict_dframes["per_day"],
            column_config={"Dates": st.column_config.DateColumn("Date", format="DD MMM YYYY")},
            hide_index=True,
            use_container_width=True,
        )

    with cols[2]:
        st.subheader("Messages per Hour")
        st.dataframe(dict_dframes["per_hour"], hide_index=True, use_container_width=True)

    with cols[3]:
        st.subheader("Messages per Weekday")
        st.dataframe(dict_dframes["per_weekday"], hide_index=True, use_container_width=True)

    st.divider()
    cols = st.columns(2, border=False)


    with cols[0]:
        st.subheader("Probability of Starting a Conversation")
        st.dataframe(
            dict_dframes["start_conversations"],
            column_config={"Start %": st.column_config.NumberColumn("Start %", format="%.1f%%")},
            hide_index=True,
            use_container_width=True,
        )

    with cols[1]:
        st.subheader("Most Shared Links")
        st.dataframe(
            dict_dframes["links"],
            column_config={"Links": st.column_config.LinkColumn("Links")},
            hide_index=True,
            use_container_width=True,
            )



def render_charts(dict_figs):
    st.subheader("Messages over Time")
    st.pyplot(dict_figs["messages_over_time"], use_container_width=False)

    st.subheader("Word Cloud")
    st.pyplot(dict_figs["wordcloud"], use_container_width=False)