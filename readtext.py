import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)


# Convert text to speech
engine.say("Hello, world!")
engine.runAndWait()
