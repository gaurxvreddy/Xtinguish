import streamlit as st
import tensorflow as tf


@st.cache(suppress_st_warning=True)
def predicting(image, model):
    image = load_and_prep(image)
    image = tf.cast(tf.expand_dims(image, axis=0), tf.int16)
    preds = model.predict(image)
    pred_class = class_names[tf.round(int(preds[0]))]
    return pred_class

def load_and_prep(image, shape=224, scale=False):
    image = tf.image.decode_image(image, channels=3)
    image = tf.image.resize(image, size=([shape, shape]))
    if scale:
        image = image/255.
    return image

class_names = ['Fire', 'No Fire']

st.set_page_config(page_title="WFD : beta")

#### Main Body ####


st.title("Xtinguish `Beta`")
st.write("**Xtinguish** is an CNN Image Classfication model which helps in detecting and preventing **Wildfires**.")
st.write("To know more about this app, visit [**GitHub**](https://github.com/gauravreddy08/Xtinguish)")
file = st.file_uploader(label="Upload an image",
                        type=["jpg", "jpeg", "png"])

model = tf.keras.models.load_model("./models/baseline_model.hdf5")

if not file:
    st.warning("Please upload an image")
    st.stop()

else:
    image = file.read()
    st.image(image, use_column_width=True)
    pred_button = st.button("Predict")

if pred_button:
    pred = predicting(image, model)
    st.success(f'Prediction : {pred}')
