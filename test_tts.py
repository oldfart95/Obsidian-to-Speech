from TTS.api import TTS

def test_xtts():
    # Initialize TTS with XTTS model
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v1")
    
    # Test text
    text = "This is a test of the XTTS text-to-speech system."
    
    # Generate speech
    output_path = "test_output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    print(f"Generated audio file: {output_path}")

if __name__ == "__main__":
    test_xtts()
