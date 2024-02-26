import streamlit as st
from instaloader import (
    BadCredentialsException,
    ConnectionException,
    Instaloader,
    Profile,
    QueryReturnedBadRequestException,
)

st.set_page_config(
    page_title="UnfollowCheck",
    page_icon=":mag:",
    menu_items={
        "About": "Identify unfollowers on Instagram.",
    },
)

st.title("UnfollowCheck", anchor=False)

with st.form("login"):
    st.subheader("Login", anchor=False)

    username: str = st.text_input("Username", placeholder="Enter your username")
    password: str = st.text_input(
        "Password", type="password", placeholder="Enter your password"
    )

    submitted: bool = st.form_submit_button("Login")

if submitted:
    if not username or not password:
        st.warning("Please enter your username and password.")

    else:
        with st.spinner("Please wait..."):
            loader: Instaloader = Instaloader(
                download_pictures=False,
                download_videos=False,
                download_video_thumbnails=False,
                save_metadata=False,
                iphone_support=False,
            )

            try:
                loader.login(username, password)

            except BadCredentialsException:
                st.error("Wrong password. Please double-check your password.")

            except ConnectionException as e:
                if "Login: Checkpoint required." in str(e):
                    st.error(
                        "Checkpoint required. Please open your Instagram app, "
                        "follow the instructions, then retry."
                    )

                else:
                    st.error("Invalid username. Please double-check your username.")

            except QueryReturnedBadRequestException:
                st.error(
                    "Checkpoint required. Please open your Instagram app, "
                    "follow the instructions, then retry."
                )

            else:
                profile: Profile = Profile.from_username(loader.context, username)

                followers: list[str] = [i.username for i in profile.get_followers()]
                followees: list[str] = [i.username for i in profile.get_followees()]

                unfollowers: set[str] = set(followers) - set(followees)
                unfollowees: set[str] = set(followees) - set(followers)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Followers who you don't follow back", anchor=False)
                    st.markdown(
                        "- @" + "\n- @".join(unfollowers) if unfollowers else "(None)"
                    )

                with col2:
                    st.subheader("Followees who don't follow you back", anchor=False)
                    st.markdown(
                        "- @" + "\n- @".join(unfollowees) if unfollowees else "(None)"
                    )
