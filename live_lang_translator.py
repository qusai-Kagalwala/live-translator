import speech_recognition as sr
import pyttsx3
import threading
import time
import langdetect
from langdetect import detect
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import pygame
import sys

class LiveTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Language Translator")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()  # Keep for English fallback
        
        # Initialize pygame for playing audio
        pygame.mixer.init()
        
        # Create temp directory for audio files if it doesn't exist
        self.temp_dir = os.path.join(tempfile.gettempdir(), "live_translator")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            
        # Track if we're currently playing audio
        self.is_speaking = False
        
        # Define available languages
        self.available_languages = {
            'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar',
            'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be',
            'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca',
            'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW',
            'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da',
            'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et',
            'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl',
            'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu',
            'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'he',
            'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is',
            'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it',
            'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk',
            'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky',
            'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt',
            'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms',
            'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr',
            'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Norwegian': 'no',
            'Nyanja (Chichewa)': 'ny', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl',
            'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru',
            'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st',
            'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala (Sinhalese)': 'si', 'Slovak': 'sk',
            'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su',
            'Swahili': 'sw', 'Swedish': 'sv', 'Tagalog (Filipino)': 'tl', 'Tajik': 'tg',
            'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk',
            'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh',
            'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
        }
        
        # Set default values
        self.is_listening = False
        self.detected_language = "en"
        self.target_language = "en"
        self.listen_timeout = 5  # Default timeout
        self.phrase_time_limit = 5  # Default phrase time limit
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        title_label = ttk.Label(main_frame, text="Live Language Translator", 
                               font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)
        
        # Create status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        # Status indicators
        self.listening_label = ttk.Label(status_frame, text="Not Listening", 
                                        foreground="red")
        self.listening_label.pack(side=tk.LEFT, padx=10)
        
        self.detected_lang_label = ttk.Label(status_frame, text="Detected: None")
        self.detected_lang_label.pack(side=tk.LEFT, padx=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Target language selection
        ttk.Label(settings_frame, text="Target Language:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Sort languages alphabetically
        sorted_languages = sorted(self.available_languages.keys())
        
        self.target_lang_combo = ttk.Combobox(settings_frame, 
                                             values=sorted_languages,
                                             state="readonly",
                                             width=20)
        self.target_lang_combo.current(sorted_languages.index("English"))
        self.target_lang_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.target_lang_combo.bind("<<ComboboxSelected>>", self.update_target_language)
        
        # Timeout setting
        ttk.Label(settings_frame, text="Listen Timeout (s):").grid(row=0, column=2, padx=(20, 5), pady=5, sticky=tk.W)
        self.timeout_var = tk.StringVar(value="5")
        timeout_entry = ttk.Spinbox(settings_frame, from_=1, to=15, textvariable=self.timeout_var, width=5)
        timeout_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.timeout_var.trace_add("write", self.update_timeout)
        
        # Phrase time limit setting
        ttk.Label(settings_frame, text="Phrase Time Limit (s):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.phrase_var = tk.StringVar(value="5")
        phrase_entry = ttk.Spinbox(settings_frame, from_=1, to=15, textvariable=self.phrase_var, width=5)
        phrase_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.phrase_var.trace_add("write", self.update_phrase_limit)
        
        # Transcription area
        trans_frame = ttk.LabelFrame(main_frame, text="Transcription", padding="10")
        trans_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Source text
        source_frame = ttk.Frame(trans_frame)
        source_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        ttk.Label(source_frame, text="Source:").pack(anchor=tk.W)
        
        self.source_text = tk.Text(source_frame, height=10, width=40)
        self.source_text.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Translated text
        target_frame = ttk.Frame(trans_frame)
        target_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        ttk.Label(target_frame, text="Translation:").pack(anchor=tk.W)
        
        self.target_text = tk.Text(target_frame, height=10, width=40)
        self.target_text.pack(fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Listening", 
                                     command=self.toggle_listening)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.speak_button = ttk.Button(button_frame, text="Speak Translation", 
                                    command=self.speak_translation)
        self.speak_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear", 
                                command=self.clear_text)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Test TTS button
        test_tts_button = ttk.Button(button_frame, text="Test Speech", 
                                   command=self.test_tts)
        test_tts_button.pack(side=tk.LEFT, padx=5)
        
        # Auto-speak toggle
        self.auto_speak_var = tk.BooleanVar(value=True)
        auto_speak_check = ttk.Checkbutton(button_frame, text="Auto-speak translation", 
                                         variable=self.auto_speak_var)
        auto_speak_check.pack(side=tk.RIGHT, padx=5)
        
    def update_target_language(self, event=None):
        selected = self.target_lang_combo.get()
        self.target_language = self.available_languages[selected]
        print(f"Target language set to: {selected} ({self.target_language})")
        
    def update_timeout(self, *args):
        try:
            self.listen_timeout = int(self.timeout_var.get())
            print(f"Listen timeout set to: {self.listen_timeout}s")
        except ValueError:
            pass
            
    def update_phrase_limit(self, *args):
        try:
            self.phrase_time_limit = int(self.phrase_var.get())
            print(f"Phrase time limit set to: {self.phrase_time_limit}s")
        except ValueError:
            pass
            
    def toggle_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.listening_label.config(text="Not Listening", foreground="red")
            self.start_button.config(text="Start Listening")
        else:
            self.is_listening = True
            self.listening_label.config(text="Listening...", foreground="green")
            self.start_button.config(text="Stop Listening")
            # Start listening thread
            threading.Thread(target=self.listen_and_translate, daemon=True).start()
    
    def listen_and_translate(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    # Get current timeout values (in case they were changed)
                    timeout = self.listen_timeout
                    phrase_limit = self.phrase_time_limit
                    
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    
                    try:
                        audio = self.recognizer.listen(
                            source, 
                            timeout=timeout, 
                            phrase_time_limit=phrase_limit
                        )
                    except sr.WaitTimeoutError:
                        print("Listening timed out, restarting...")
                        continue
                    
                    try:
                        # First try to recognize without language specification for auto-detection
                        text = self.recognizer.recognize_google(audio)
                        if text:
                            # Detect language
                            try:
                                self.detected_language = detect(text)
                                # Get language name by code (reverse lookup)
                                lang_name = next((k for k, v in self.available_languages.items() 
                                                if v == self.detected_language), "Unknown")
                                
                                # Update UI
                                self.root.after(0, lambda: self.detected_lang_label.config(
                                    text=f"Detected: {lang_name}"))
                                
                                # Add text to source box
                                self.root.after(0, lambda t=text: self.append_source_text(t))
                                
                                # Translate text using deep_translator
                                try:
                                    translator = GoogleTranslator(source=self.detected_language, target=self.target_language)
                                    translation = translator.translate(text)
                                    
                                    # Add translation to target box
                                    self.root.after(0, lambda t=translation: self.append_target_text(t))
                                    
                                    # Automatically speak the translation - use a longer delay to ensure UI updates first
                                    self.root.after(500, lambda t=translation: self.auto_speak_translation(t))
                                except Exception as e:
                                    print(f"Translation error: {e}")
                                    # Fallback method using API
                                    translation = self.fallback_translate(text, self.detected_language, self.target_language)
                                    
                                    # Add translation to target box
                                    self.root.after(0, lambda t=translation: self.append_target_text(t))
                                    
                                    # Automatically speak the translation - use a longer delay
                                    self.root.after(500, lambda t=translation: self.auto_speak_translation(t))
                                
                            except langdetect.lang_detect_exception.LangDetectException as e:
                                print(f"Language detection failed: {e}")
                                # Add text to source box without translation
                                self.root.after(0, lambda t=text: self.append_source_text(t))
                                self.root.after(0, lambda: self.append_target_text("(Language detection failed)"))
                                
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                        self.root.after(0, lambda e=e: messagebox.showerror("API Error", f"Speech recognition failed: {e}"))
                
            except Exception as e:
                print(f"Error in listening: {e}")
                if not self.is_listening:
                    break
                    
                # Add small sleep to avoid tight loop if there's a persistent error
                time.sleep(0.5)
    
    def append_source_text(self, text):
        self.source_text.insert(tk.END, text + "\n")
        self.source_text.see(tk.END)
    
    def append_target_text(self, text):
        self.target_text.insert(tk.END, text + "\n")
        self.target_text.see(tk.END)
    
    def speak_translation(self):
        """Speak the entire translation history"""
        text = self.target_text.get("1.0", tk.END).strip()
        if text and not self.is_speaking:
            print(f"Speaking full translation in {self.target_language}")
            
            # Use a separate thread for TTS to avoid blocking the UI
            threading.Thread(target=self._speak_with_gtts, 
                          args=(text, self.target_language), 
                          daemon=True).start()
        elif self.is_speaking:
            messagebox.showinfo("Info", "Already speaking. Please wait.")
        else:
            messagebox.showinfo("Info", "No translation to speak")
            
    def auto_speak_translation(self, text):
        """Speak just the latest translated text automatically using gTTS"""
        # Only speak if auto-speak is enabled
        if not self.auto_speak_var.get() or not text or self.is_speaking:
            return
            
        if isinstance(text, str) and len(text) > 0:
            try:
                print(f"Auto-speaking: {text} in language {self.target_language}")
                
                # Mark that we're speaking
                self.is_speaking = True
                
                # Use a separate thread for TTS to avoid blocking the UI
                threading.Thread(target=self._speak_with_gtts, 
                               args=(text, self.target_language), 
                               daemon=True).start()
                
            except Exception as e:
                print(f"Auto-speak error: {e}")
                self.is_speaking = False
    
    def _speak_with_gtts(self, text, lang_code):
        """Helper method to perform gTTS speech in a separate thread"""
        try:
            # Generate a unique filename for this speech
            temp_file = os.path.join(self.temp_dir, f"speech_{time.time()}.mp3")
            
            # Create gTTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to temporary file
            tts.save(temp_file)
            
            # Play the audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Clean up the temp file
            try:
                os.remove(temp_file)
            except:
                pass  # Ignore if we can't remove it
                
        except Exception as e:
            print(f"gTTS error: {e}")
            
            # Fallback to pyttsx3 for English
            if lang_code == 'en':
                try:
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e2:
                    print(f"Fallback TTS error: {e2}")
        finally:
            # Mark that we're done speaking
            self.is_speaking = False
    
    def clear_text(self):
        """Clear both text areas"""
        self.source_text.delete("1.0", tk.END)
        self.target_text.delete("1.0", tk.END)
        
    def test_tts(self):
        """Test the text-to-speech functionality"""
        target_lang = self.target_language
        test_text = f"This is a test of the text-to-speech system in {self.target_lang_combo.get()}"
        
        # For non-English languages, use a simple greeting in that language
        greetings = {
            'es': "Hola, ¿cómo estás?",
            'fr': "Bonjour, comment allez-vous?",
            'de': "Hallo, wie geht es Ihnen?",
            'it': "Ciao, come stai?",
            'ja': "こんにちは、お元気ですか？",
            'ko': "안녕하세요, 어떻게 지내세요?",
            'zh-CN': "你好，你好吗？",
            'ru': "Здравствуйте, как дела?",
            'ar': "مرحبا، كيف حالك؟",
            'hi': "नमस्ते, आप कैसे हैं?",
            'pt': "Olá, como você está?",
            'gu': "નમસ્તે, તમે કેમ છો?",
            'bn': "হ্যালো, আপনি কেমন আছেন?",
            'th': "สวัสดี คุณเป็นอย่างไรบ้าง?",
        }
        
        if target_lang in greetings:
            test_text = greetings[target_lang]
        
        messagebox.showinfo("TTS Test", f"Testing speech in {self.target_lang_combo.get()}")
        self.auto_speak_translation(test_text)
        
    def fallback_translate(self, text, source_lang, target_lang):
        """Fallback translation using a free API"""
        try:
            # If text is too long, split it into manageable chunks
            if len(text) > 500:
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                translations = []
                for chunk in chunks:
                    translations.append(self._translate_chunk(chunk, source_lang, target_lang))
                return " ".join(translations)
            else:
                return self._translate_chunk(text, source_lang, target_lang)
        except Exception as e:
            return f"Fallback translation error: {str(e)}"
    
    def _translate_chunk(self, text, source_lang, target_lang):
        """Translate a single chunk of text"""
        try:
            # Use MyMemory API without authentication (free tier)
            base_url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_lang}|{target_lang}"
            
            response = requests.get(base_url)
            data = response.json()
            
            if "responseData" in data and "translatedText" in data["responseData"]:
                return data["responseData"]["translatedText"]
            else:
                return f"Translation failed: {data.get('responseStatus', 'Unknown error')}"
        except Exception as e:
            return f"API Error: {str(e)}"

if __name__ == "__main__":
    # Create Tkinter window
    root = tk.Tk()
    app = LiveTranslator(root)
    root.mainloop()