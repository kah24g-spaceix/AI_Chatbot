from RealtimeSTT import AudioToTextRecorder

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder (
        realtime_model_type="large-v2",
        language='ko'
    )
    recorder.start()
    input("Press Enter to stop recording...")
    recorder.stop()
    print("Transcription: ", recorder.text())