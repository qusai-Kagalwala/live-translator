# 🎤 Live Translator

Real-time speech translator with voice input/output supporting 100+ languages. Speak in any language and hear the translation instantly!

## ✨ Features

- 🎤 **Real-time Speech Recognition**: Captures your voice input continuously
- 🌍 **100+ Languages**: Supports extensive language detection and translation
- 🔍 **Auto Language Detection**: Automatically identifies the spoken language
- 🔊 **Text-to-Speech Output**: Hear translations in natural-sounding voices
- 🎛️ **Customizable Settings**: Adjust timeouts, phrase limits, and preferences
- 📝 **Live Transcription**: See both original and translated text in real-time
- 🔄 **Auto-speak Mode**: Automatically speaks translations as they're generated
- 🎯 **User-friendly GUI**: Clean Tkinter interface with intuitive controls

## 🚀 Quick Start

### Prerequisites
Install the required dependencies:
```bash
pip install speech-recognition pyttsx3 langdetect requests deep-translator gtts pygame
```

### Additional System Requirements
- **Windows**: No additional setup required
- **macOS**: May need to install PortAudio: `brew install portaudio`
- **Linux**: Install ALSA development headers: `sudo apt-get install python3-dev libasound2-dev`

### Installation & Run
1. 📥 Clone this repository:
   ```bash
   git clone https://github.com/qusai-Kagalwala/live-translator.git
   cd live-translator
   ```

2. 🎤 Ensure your microphone is working and permissions are granted

3. ▶️ Run the application:
   ```bash
   python live_lang_translator.py
   ```

## 🎯 How to Use

### Basic Operation
1. 🎯 **Select Target Language**: Choose your desired translation language from the dropdown
2. ⚙️ **Adjust Settings**: Configure timeout and phrase limits if needed
3. 🎤 **Start Listening**: Click "Start Listening" to begin voice capture
4. 🗣️ **Speak Naturally**: Talk in any supported language
5. 👀 **Watch Translation**: See real-time transcription and translation
6. 🔊 **Hear Results**: Auto-speak will play the translation aloud

### Controls Explained
- **Start/Stop Listening**: Toggle voice input capture
- **Speak Translation**: Manually play the entire translation history
- **Clear**: Reset both transcription areas
- **Test Speech**: Test TTS functionality in selected language
- **Auto-speak Toggle**: Enable/disable automatic translation playback

## 🌍 Supported Languages

The app supports **100+ languages** including:

### Popular Languages
- 🇺🇸 **English** - 🇪🇸 **Spanish** - 🇫🇷 **French** - 🇩🇪 **German**
- 🇮🇹 **Italian** - 🇯🇵 **Japanese** - 🇰🇷 **Korean** - 🇨🇳 **Chinese**
- 🇷🇺 **Russian** - 🇸🇦 **Arabic** - 🇮🇳 **Hindi** - 🇵🇹 **Portuguese**

### Regional Languages
- 🇮🇳 **Gujarati, Bengali, Tamil, Telugu, Marathi, Punjabi**
- 🇹🇭 **Thai** - 🇻🇳 **Vietnamese** - 🇮🇩 **Indonesian** - 🇲🇾 **Malay**
- 🇳🇱 **Dutch** - 🇸🇪 **Swedish** - 🇳🇴 **Norwegian** - 🇩🇰 **Danish**

[View complete language list in the source code]

## ⚙️ Configuration Options

### Timing Settings
- **Listen Timeout**: How long to wait for speech (1-15 seconds)
- **Phrase Time Limit**: Maximum duration for a single phrase (1-15 seconds)

### Audio Settings
- **Auto-speak**: Toggle automatic translation playback
- **TTS Language**: Matches your selected target language
- **Volume**: Controlled by system volume settings

### Performance Tips
- 🎤 **Clear Audio**: Ensure minimal background noise for better recognition
- 🗣️ **Natural Speech**: Speak clearly at normal pace
- ⏱️ **Pause Between Phrases**: Allow time for processing between sentences
- 🔊 **Test TTS**: Use the test button to verify audio output

## 🛠️ Technical Architecture

### Core Components
- **Speech Recognition**: `speech_recognition` library with Google API
- **Language Detection**: `langdetect` for automatic language identification
- **Translation Engine**: `deep_translator` with Google Translate backend
- **Text-to-Speech**: `gtts` for natural voice synthesis + `pyttsx3` fallback
- **Audio Playback**: `pygame` for cross-platform audio support
- **GUI Framework**: `tkinter` for native desktop interface

### Processing Flow
```
Voice Input → Speech Recognition → Language Detection → Translation → TTS → Audio Output
     ↓              ↓                    ↓               ↓        ↓         ↓
 Microphone → Google Speech API → langdetect → Google Translate → gTTS → pygame
```

### Error Handling
- **Network Fallback**: MyMemory API backup for translation
- **Audio Fallback**: pyttsx3 backup for English TTS
- **Timeout Management**: Configurable timeout handling
- **Exception Recovery**: Graceful error recovery and user notifications

## 📁 Project Structure

```
live-translator/
├── live_lang_translator.py    # Main application file
├── README.md                  # This documentation
├── requirements.txt           # Dependencies (optional)
└── temp/                      # Temporary audio files (auto-created)
```

## 🔧 Troubleshooting

### Common Issues

**🎤 Microphone Not Working**
- Check system microphone permissions
- Verify microphone is not used by other applications
- Test with different USB/audio ports

**🌐 Translation Errors**
- Ensure internet connection is stable
- Try speaking more clearly or slowly
- Check if the language is properly detected

**🔊 No Audio Output**
- Verify system volume settings
- Check speaker/headphone connections
- Test with "Test Speech" button

**⚡ Performance Issues**
- Reduce timeout values for faster response
- Close other audio-intensive applications
- Ensure stable internet connection

### Debug Mode
Enable debug output by checking the console for detailed error messages and processing steps.

## 🎯 Use Cases

- 🌍 **Travel Communication**: Instant conversation with locals
- 📚 **Language Learning**: Practice pronunciation and listening
- 💼 **Business Meetings**: Real-time multilingual communication
- 👨‍⚕️ **Healthcare**: Communicate with patients in different languages
- 🎓 **Education**: Classroom translation assistance
- 👥 **Social Events**: Breaking language barriers

## 🤝 Contributing

Contributions are welcome! Here are some enhancement ideas:

### Feature Requests
- 📱 **Mobile Version**: React Native or Flutter implementation
- 💾 **Conversation History**: Save and export translation sessions
- 🎵 **Audio Recording**: Save original audio with translations
- 🤖 **AI Improvements**: Better accent recognition and context awareness
- 🎨 **UI Themes**: Dark mode and customizable interfaces
- 📊 **Analytics**: Translation accuracy and usage statistics

### Technical Improvements
- 🔄 **Offline Mode**: Local translation models
- ⚡ **Performance**: Faster processing and lower latency
- 🔐 **Privacy**: Local-only processing options
- 📱 **Cross-platform**: Mobile and web versions

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Qusai Kagalwala**
- GitHub: [@qusai-Kagalwala](https://github.com/qusai-Kagalwala)

## 🙏 Acknowledgments

- Google Speech Recognition API
- Google Translate API
- gTTS (Google Text-to-Speech)
- Deep Translator library
- LangDetect library

---

🎤 **Ready to break language barriers? Start translating now!** 🌍
