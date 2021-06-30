import streamlit as st
import pandas as pd
import numpy as np
from sklearn.externals import joblib
m1=joblib.load("/content/Random_forest.pkl")
m2=joblib.load("/content/lightgbm.pkl")
df=pd.read_csv("/content/Testing.csv")
dec=pd.read_csv("/content/symptom_Description.csv")
pre=pd.read_csv("/content/symptom_precaution.csv")
st.markdown("<h1 style='text-align: center;'>Home Doctor</h1>", unsafe_allow_html=True)
st.subheader('Always there for you')
st.markdown("<br><br>",unsafe_allow_html=True)
st.markdown("Choose the symptoms that you are suffering from")
arr=[]
with st.form("my_form"):
  for c in df.columns[:-1]:
    if c!='fluid_overload':
      arr.append(st.checkbox(c.upper()))
  st.markdown("<br><br>",unsafe_allow_html=True)
  v=st.slider("Enter the overall severity of your symptoms",0,10)
  s=st.form_submit_button("Submit")
arr=[0 if i==False else 1 for i in arr]

if(s):
  if(len(set(arr))==1):
    st.error("Please choose the symptoms")
  else:
    arr=np.array(arr).reshape(1,-1)
    if(v>=5):
      st.error("Sorry but by observing your symptoms with severity score, you should visit doctor")  
    else:
      if(m1.predict(arr)[0]==m2.predict(arr)[0]):
        p1=m1.predict(arr)[0].capitalize()
        st.success("You may suffering from "+p1)
        st.markdown("Description of "+p1)
        x=dec[dec['Disease']==p1[0]+p1[1:].lower()].to_string(columns=['Description'],header=False, index=False)
        if(dec[dec['Disease']==p1[0]+p1[1:].lower()].empty):
          st.error("Sorry but for "+p1+" ,you should visit doctor as we are unable to help you")
        else:
          st.success(x)
          st.markdown("Precaution to be taken")
          temp=pre[pre['Disease']==p1[0]+p1[1:].lower()]
          for col in temp.columns[1:]:
            st.success(temp[col].to_string(header=False, index=False))
      else:
        p1=m1.predict(arr)[0].capitalize()
        p2=m2.predict(arr)[0].capitalize()
        st.success("You may suffering from "+p1+" or "+p2)
        st.markdown("Description of "+p1)
        x=dec[dec['Disease']==p1[0]+p1[1:].lower()].to_string(columns=['Description'],header=False, index=False)

        if(dec[dec['Disease']==p1[0]+p1[1:].lower()].empty):
          st.error("Sorry but for "+p1+" ,you should visit doctor as we are unable to help you")
        else:
          st.success(x)
          st.markdown("Precaution to be taken")
          temp=pre[pre['Disease']==p1[0]+p1[1:].lower()]
          for col in temp.columns[1:]:
            st.success(temp[col].to_string(header=False, index=False))
        st.markdown("Description of "+p2)
        x=dec[dec['Disease']==p2[0]+p2[1:].lower()].to_string(columns=['Description'],header=False, index=False)
        if(dec[dec['Disease']==p2[0]+p2[1:].lower()].empty):
          st.error("Sorry but for "+p2+" ,you should visit doctor as we are unable to help you")
        else:
          st.success(x+str(len(x)))
          st.markdown("Precaution to be taken")
          temp=pre[pre['Disease']==p2[0]+p2[1:].lower()]
          for col in temp.columns[1:]:
            st.success(temp[col].to_string(header=False, index=False))
