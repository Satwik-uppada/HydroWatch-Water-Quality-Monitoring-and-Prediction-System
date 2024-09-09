# -----> Required libraries 
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import requests
import json
import components.database_creation as database_creation
from streamlit_lottie import st_lottie


def lottie_files(filepath: str):
    with open(filepath,'r') as f:
        return json.load(f)

login_lottie_file = lottie_files("lottiefiles/login.json")
fb_credentials = st.secrets["firebase"]['pass_key']

if not firebase_admin._apps:
    cred = credentials.Certificate(fb_credentials)
    firebase_admin.initialize_app(cred)

if 'username' not in st.session_state:
    st.session_state.username = ''
    
if 'useremail' not in st.session_state:
    st.session_state.useremail = ''


def app():
    
    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):  
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            # -----> make sure you insert your firebase passkey here 
            r = requests.post(rest_api_url, params={"key": "Your pass key here"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email, password, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token,
            }
            
            
            if email:
                payload["email"] = email
            else:
                st.write("Please give email or you forgot to enter after filling the details....")
            
            if password:
                payload["password"] = password
            else:
                st.write("Please give password or you forgot to enter after filling the details....")
                
           
            payload = json.dumps(payload)
            # -----> make sure you insert your firebase passkey here 
            r = requests.post(rest_api_url, params={"key": "Your passkey here"}, data=payload)
            
            data = r.json()
            user_info = {
                'email': data['email'],
                'username': data.get('displayName')  # Retrieve username if available
            }
            return user_info
            
        except Exception as e:
            st.warning(f'Sign-in failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            # -----> make sure you insert your firebase passkey here 
            r = requests.post(rest_api_url, params={"key": "your pass key here"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)
          
    def authentication():
        try:
            userinfo = sign_in_with_email_and_password( st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']

            global Usernm
            Usernm=(userinfo['username'])

            st.session_state.signedout = True
            st.session_state.signout = True

        except:
            st.warning("Login Failed")
           
    def signout():
        st.session_state.signedout = False
        st.session_state.signout = False
        st.session_state.username = ''       
                           
                                            
    def forget():
        st.subheader("Forgot Password...❓",divider='gray')
        email = st.text_input('Email')
        if st.button("Send Link"):
            try:
                success, message = reset_password(email)
                if success:
                    st.success("Password reset email sent successfully.")
                else:
                    st.warning(f"Password reset failed: {message}")
            except:
                st.warning("Process Failed.....")
                
    def analysis():
        try:
            st.markdown(
                f"""
                <style>
                .analysis {{
                    font-size: 2em;
                    font-weight: bold;
                    color: grey ;
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 2px 2px 12px #aaaaaa;
                    margin: 0px 0px 8px 0px;
                }}
                </style>
                <div class="analysis">
                    Analysis Report
                </div>
                """,
                unsafe_allow_html=True
            )              
            st.subheader("Personal Data :open_file_folder:",divider='rainbow')
            database_creation.show_user_table(current_username= st.session_state.username)
            data= database_creation.get_database(st.session_state.username)
            
            with st.container(border=True):
                st.header("EDA Report",divider='grey')
                c1,c2,c3 =st.columns(3)
                with c1:
                   st.line_chart(data,x='timestamp',y='aluminium',color='#1995ad')
                   st.line_chart(data,x='timestamp',y='ammonia',color='#1995ad')
                   st.line_chart(data,x='timestamp',y='arsenic',color='#1995ad')
                   st.line_chart(data,x='timestamp',y='barium',color="#1995ad") 
                   st.line_chart(data,x='timestamp',y='cadmium',color="#1995ad") 
                   st.line_chart(data,x='timestamp',y='chloramine',color="#1995ad")
                   st.line_chart(data,x='timestamp',y='chromium',color="#1995ad")
                 
                with c2:
                    st.line_chart(data,x='timestamp',y='copper',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='flouride',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='bacteria',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='viruses',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='lead',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='nitrates',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='nitrites',color="#1995ad")
                		
                with c3:
                    st.line_chart(data,x='timestamp',y='mercury',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='perchlorate',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='radium',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='selenium',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='silver',color="#1995ad")
                    st.line_chart(data,x='timestamp',y='uranium',color="#1995ad")
                    st.bar_chart(data,x='timestamp',y='is_safe',color="#1995ad")
                
        except:
             st.info("Please use water quality model to see your personalized data and analysis of result by time")
    
                     
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
        
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    
    # if the state is signed out means not sign in till now
    if  not st.session_state["signedout"]:
        st.toast("Please login for Personalized analysis",icon=":material/login:")
        # only show if the state is False, hence the button has never been clicked
        
        with st.container(border=True):
            c1,c2 = st.columns(2,vertical_alignment='center',gap='medium')
            with c1:
                st_lottie(login_lottie_file,speed=1,reverse=False,loop=True,quality='high',height=585)
            with c2:
                
                choice = st.selectbox('Login/Signup',['Login','Sign up'])
                with st.container(border=True):
                    if choice == 'Sign up':
                        email = st.text_input('Email Address')
                        password = st.text_input('Password',type='password')
                        st.session_state.email_input = email
                        st.session_state.password_input = password
                        username = st.text_input("Enter  your unique username")
                        if st.button('Create my account',type='primary'):
                            user = sign_up_with_email_and_password(email=email,password=password,username=username)
                            if user:
                                st.success('Account created successfully!')
                                st.info('Please Login using your registered mail-id and password')
                                st.balloons()
                    else:
                        st.markdown(f"""
                            <style>
                            .greeting {{
                                font-size: 2em;
                                font-weight: bold;
                                color:black;
                                padding: 10px;
                                border-radius: 10px;
                                text-align: center
                            }}
                            .messages {{
                                font-weight: bold;
                                text-align: center;
                            }}
                            </style>

                            <div class='greeting'>
                                Welcome Back
                            </div>
                            <div class='messages'>
                                Enter your credentials
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.info("Please press :red-background[ENTER] once you enter the details to apply the updated values.")
                        email = st.text_input('Email Address')
                        password = st.text_input('Password',type='password')
                        st.session_state.email_input = email
                        st.session_state.password_input = password
                        st.button('Login', on_click= authentication,type='primary')
                        st.write("---")
                        with st.expander("Forgot Password",icon="❓️",expanded=False):
                            forget()
        
        

    
            
                                                                       
    if st.session_state.signout:
        # Assuming username and useremail are stored in session_state
        st.toast("Thanks for logging in ",icon="🙏")
        if 'username' in st.session_state and 'useremail' in st.session_state:
            st.markdown(
                f"""
                <style>
                .greeting {{
                    font-size: 2em;
                    font-weight: bold;
                    color:#1995ad;
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 2px 2px 12px #aaaaaa;
                    margin: 0px 0px 8px 0px;
                }}
                </style>
                <div class="greeting">
                    Account Information
                </div>
                """,
                unsafe_allow_html=True
            )              
            
            st.markdown(
                f"""
                <style>
                .information {{
                    font-size: 2em;
                    font-weight: bold;
                    color:#1995ad;
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 10px;
                    text-align:left ;
                    box-shadow: 2px 2px 12px #aaaaaa;
                    margin: 0px 0px 8px 0px;
                    display: flex;
                    justify-content: space-between
                }}
                </style>
                <div class="information">
                    <div style='color: #1995AD; font-size: large' ><b style='color: black; font-size:20px' >Name:</b> {st.session_state.username}</div>
                    <div style='color: #1995AD; font-size: large'><b style='color: black; font-size:20px' >Email id:</b> {st.session_state.useremail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
                  
        # col1, col8 = st.columns(spec=[8,5], gap="large")
        st.button('Sign Out', on_click=signout,type='primary')
        st.write("---")
        analysis()
                     
def credentials():
    return st.session_state.username


app()
