import streamlit as st
import warnings


warnings.filterwarnings('ignore')
st.set_page_config(page_title='HydroWatch',layout='wide', page_icon='🌊')

#Custom CSS
sidebar_custom_css = """
                        <style>
                            .st-emotion-cache-5drf04 {
                                height: 3rem;
                                max-width: 15rem;
                                margin: 0.25rem 0.5rem 0.25rem 0px;
                                z-index: 999990;
                                background: white;
                                border-radius: 50%;
                                border: 2px solid white; /* White border */
                                box-shadow: 0 0 5px white, 0 0 7px white, 0 0 9px white, 0 0 11px #1995ad;
                            }
                            
                            [data-testid="stSidebarContent"]{
                                background-color: #1995AD;
                            }
                            
                            .menu .nav-item .nav-link.active[data-v-5af006b8]{
                                background-color: #1995AD;
                            }

                            [data-v-5af006b8] {
                                background-color: #1995ad;
                            }

                           .container-xxl[data-v-5af006b8] {
                               background-color: #ffffff 
                               border-radius: .5rem;
                           }
                           
                           [data-testid="stSidebarNavItems"]{
                               font-size: 1.2rem;
                           }
                           
                           [data-testid="stIconMaterial"]{
                               font-size: 1.2rem;
                           }
                           
                           .st-emotion-cache-1rtdyuf {
                                color: black;
                                overflow: hidden;
                                white-space: nowrap;
                                text-overflow: ellipsis;
                                display: table-cell;
                            }
                            .st-emotion-cache-5k5r22 .e16edly10 {
                                color: white;
                                font-weight: 400;
                            }
                            a, a:visited {
                                color: red;
                            }
                            .st-emotion-cache-6tkfeg {
                                color: white;
                                overflow: hidden;
                                white-space: nowrap;
                                text-overflow: ellipsis;
                                display: table-cell;
                            }
                        
                            .st-emotion-cache-1f3w014 {
                                vertical-align: middle;
                                overflow: hidden;
                                # color: red;
                                fill: #1995ad;
                                background-color: white;
                                display: inline-flex;
                                -webkit-box-align: center;
                                align-items: center;
                                font-size: 1.5rem;
                                width: 1.5rem;
                                height: 1.5rem;
                                flex-shrink: 0;
                                border-radius: 50%;
                            } 
                            .st-emotion-cache-94ux81 {
                                text-decoration: none;
                                font-weight: 600;
                                display: flex;
                                flex-direction: row;
                                -webkit-box-align: center;
                                align-items: center;
                                gap: 0.5rem;
                                border-radius: 0.25rem;
                                padding-left: 0.5rem;
                                padding-right: 0.5rem;
                                margin: 0.125rem 1.5rem;
                                line-height: 2;
                                color: rgb(85, 88, 103);
                                background-color: white;
                            } 
                            img, svg {
                                vertical-align: middle;
                                border-radius: 10%;
                            }
                       </style>
                    """

st.markdown(sidebar_custom_css,unsafe_allow_html=True)

logo = "HydroWatch.png"
st.logo(logo, icon_image=logo)
st.sidebar.write("<p style='color:white; font-size:25px; text-align: center'><b>Water Quality Monitoring and prediction System</b></p>", unsafe_allow_html=True)
st.sidebar.image(logo)

homepage = st.Page('components/home_page.py', title='Home', icon=':material/home:')
database = st.Page('components/database_page.py', title='Explore Database', icon=":material/database:")
model = st.Page('components/model_page.py', title='Prediction Model' ,icon=':material/model_training:')
account = st.Page('components/account_page.py', title='Account', icon=':material/account_circle:')

pg = st.navigation([homepage,database,model,account])
pg.run()
