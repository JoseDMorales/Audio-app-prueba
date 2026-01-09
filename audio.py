import streamlit as st
import librosa
import numpy as np

st.title("Audio RMS & Duration")

if "audio_loaded" not in st.session_state:
    st.session_state.audio_loaded = False
    st.session_state.source = None

def reset_audio():
    st.session_state.audio_loaded = False
    st.session_state.source = None

if not st.session_state.audio_loaded:
    audio_input = st.audio_input("Grabar audio")
    uploaded_file = st.file_uploader("O subir archivo .wav", type=["wav"])

    source = audio_input or uploaded_file

    if source is not None:
        st.session_state.source = source
        st.session_state.audio_loaded = True
        st.rerun()

if st.session_state.audio_loaded:
    try:
        y, sr = librosa.load(st.session_state.source, sr=None, mono=True)

        if y.size == 0:
            st.error("El audio no contiene datos válidos.")
            st.stop()

        duration_seconds = len(y) / sr
        rms_energy = np.sqrt(np.mean(y ** 2))

        st.write(f"Duración (s): {duration_seconds:.3f}")
        st.write(f"Energía RMS: {rms_energy:.6f}")

        st.button("Analizar otro audio", on_click=reset_audio)

    except Exception as e:
        st.error("Error procesando el audio.")
        st.write(str(e))