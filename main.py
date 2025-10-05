# PUT YOUR API KEYS IN LINES 78 and 79
import asyncio
import pygame, sys
import pygame_gui
import edge_tts_audio
import threading
import os
import google.generativeai as genai
import tempfile

############################ Utility Function for File Access ##########################
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller .exe
    """
    try:
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

############################ This part handles conversation with Gemini-2.5-flash via Gemini API ##########################
def get_gemini_response(user_prompt: str, Gemini_API_Keys: list[str]) -> str:
    """
    Takes a list of API keys and a prompt from the user.
    Tries each API key one by one until one works.
    If all fail, returns an error message.
    """
    for idx, api_key in enumerate(Gemini_API_Keys, start=1):
        try:
            # Configure the Gemini client with the current API key
            genai.configure(api_key=api_key)

            # Initialize the Gemini model (latest 2.5 Flash)
            model = genai.GenerativeModel('gemini-2.5-flash')

            print(f"\n🔑 Trying API Key {idx}/{len(Gemini_API_Keys)}...")
            print("🧠 Thinking...")

            # Send the prompt to the model
            response = model.generate_content(user_prompt)

            # Print and return the model's response
            print("\n✨ Gemini's Answer:")
            print(response.text)
            return response.text

        except Exception as e:
            # Log the error for this key and try the next one
            print(f"\n❌ Error with API Key {idx}: {e}", file=sys.stderr)

    # If no API key works
    print("\n🚫 All API keys failed. Please check your keys.", file=sys.stderr)
    return None

# Initialize conversation history globally
conversation_history = ""

def conversation(speech):
    global conversation_history
    global talking, start_time, sound_len, character, chat_response, chat_response_state

    # Append user message to history instead of overwriting
    conversation_history += f"\n<USER>: {speech}"

    # Construct prompt with history + system role
    full_prompt = (
        conversation_history
        + "\n\n[System: Continue this friendly anime-style chat as GPT-chan. "
          "Keep your response under 150 words. Stay consistent with past context. "
          "Your responses will be read out. Make it reading friendly.]"
    )

    # Generate Gemini response
    chat_response = get_gemini_response(
        full_prompt,
        [
            "YOUR API KEY 1",
            "YOUR API KEY 2",
        ],
    )

    # Add assistant’s response to the conversation history
    conversation_history += f"\n<ASSISTANT>: {chat_response}\n"

    # Mark that we got a response
    chat_response_state = 1

    # Text-to-speech (generate MP3 audio in memory)
    audio_data = asyncio.run(edge_tts_audio.generate_audio(chat_response))

    # Write in-memory MP3 to a temporary file for pygame
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_data.read())
        temp_audio.flush()
        temp_path = temp_audio.name  # path for pygame to use

    # Play voice + animation
    start_time = pygame.time.get_ticks()
    sound = pygame.mixer.Sound(temp_path)
    sound_len = sound.get_length()
    character = player2
    sound.play()

####################### Pygame Code ######################
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.attack_animation = False
        self.sprites = []

        # Load normal sprites
        lst = os.listdir(resource_path('pngFemale/normal'))
        number_files = len(lst)
        for i in range(number_files):
            self.sprites.append(pygame.image.load(resource_path(f'pngFemale/normal/{i+1}.png')))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.attack_animation = False
        self.image = self.sprites[int(self.current_sprite)]

############ 2nd Player class To animate mouth movement ############
class Player2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.attack_animation = False
        self.sprites = []

        # Load talking sprites
        lst = os.listdir(resource_path('pngFemale/talking'))
        number_files = len(lst)
        for i in range(number_files):
            self.sprites.append(pygame.image.load(resource_path(f'pngFemale/talking/{i}.png')))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.attack_animation = False
        self.image = self.sprites[int(self.current_sprite)]

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 800
screen_height = 340
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AnimeGPT")

##### Showing Text #####
font = pygame.font.SysFont(resource_path("fonts/FreeSansBold.ttf"), 20)
font2 = pygame.font.SysFont(resource_path("fonts/FreeSansBold.ttf"), 20)
text_surface = font.render("""Ask me anything in the text input box below 
and press ENTER. I Will try my best to answer. 
(Wait a little after pressing ENTER please. The program takes a while to respond)""", True, 'Purple')

manager = pygame_gui.UIManager((screen_width, screen_height))

TEXT_INPUT = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((240, 75), (500, 50)),
    manager=manager,
    object_id='#main_text_entry'
)

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player(-150, -55)
player2 = Player2(-150, -55)
character = player

####### Initializing variables ###########
start_time = 0
sound_len = 0
talking = 0
time_since_speaking = 0
t1 = threading.Thread(target=conversation)
chat_response = ""
chat_response_state = 0
moving_sprites.add(character)

while True:
    text_surface2 = font2.render("Response:\n" + chat_response, True, 'Black', wraplength=530)
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ##### When Enter is pressed #####
        if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
            print("Enter pressed. Threading start")
            t1 = threading.Thread(target=conversation, args=(event.text,))
            t1.start()

        manager.process_events(event)
    manager.update(time_delta)
    if start_time:
        time_since_speaking = (pygame.time.get_ticks() - start_time) / 1000  #### Calculates time elapsed since speaking

    if time_since_speaking >= sound_len:
        character = player

    moving_sprites.empty()
    moving_sprites.add(character)

    # Drawing
    screen.fill((255, 255, 255))
    ##### Background image ####
    image = pygame.image.load(resource_path('bg4.jpg'))
    IMAGE_SIZE = (800, 550)
    image = pygame.transform.scale(image, IMAGE_SIZE)
    DEFAULT_IMAGE_POSITION = (0, 0)
    screen.blit(image, DEFAULT_IMAGE_POSITION)

    ## Widget background
    pygame.draw.rect(screen, 'thistle2', [240, 10, 540, 530])
    moving_sprites.draw(screen)

    #### Show texts ####
    screen.blit(text_surface, (250, 30))
    screen.blit(text_surface2, (240, 125))
    moving_sprites.update(0.25)
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(60)
